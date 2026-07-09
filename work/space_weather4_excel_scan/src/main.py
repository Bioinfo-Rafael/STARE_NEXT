from __future__ import annotations

import argparse
from pathlib import Path

from src.excel_adapters import adapter_for
from src.external.combined_space_weather_features import build_combined_features
from src.external.dst_fetch import fetch_dst, probe_dst
from src.external.geomag_features import build_geomag_features
from src.external.glotec_features import build_glotec_features
from src.external.glotec_fetch import fetch_glotec, probe_glotec
from src.external.intermagnet_fetch import fetch_intermagnet, probe_intermagnet
from src.external.jma_geomag_fetch import fetch_jma_geomag, probe_jma_geomag
from src.external.kp_dst_features import build_kp_dst_features
from src.external.kp_fetch import fetch_kp, probe_kp
from src.external.omni_features import build_omni_features
from src.external.omni_fetch import fetch_omni, probe_omni
from src.orchestration.run_all_pairs import run_all_pairs
from src.registry.parse_excel_registry import parse_excel_registry
from src.utils.io import ensure_dir, write_csv, write_json

DEFAULT_LAGS = "-30D,-14D,-7D,-3D,-1D,0D,1D,3D,7D,14D,30D"
VALID_SOURCES = {"kp_dst", "glotec", "omni", "intermagnet", "jma_geomag", "combined", "all"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Four-source space-weather scan against Excel-listed earthquake/geodetic datasets")
    parser.add_argument("--excel", default="../../資料3_地震・測地データの一覧.xlsx")
    parser.add_argument("--start-date", default="2020-01-01")
    parser.add_argument("--end-date", default="2024-12-31")
    parser.add_argument("--spatial-unit", default="national")
    parser.add_argument("--lags", default=DEFAULT_LAGS)
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--dataset", default="all")
    parser.add_argument("--source", default="all", choices=sorted(VALID_SOURCES))
    parser.add_argument("--probe-only", action="store_true")
    parser.add_argument("--combined-models", action="store_true")
    parser.add_argument("--kp-only", action="store_true")
    parser.add_argument("--include-dst", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--keep-raw", action="store_true")
    parser.add_argument("--cleanup-raw", default="true")
    parser.add_argument("--min-samples", type=int, default=365)
    return parser.parse_args()


def _coverage(rows: list[dict]) -> tuple[str, str, int]:
    dates = sorted({str(r.get("date", "")) for r in rows if r.get("date")})
    return (dates[0], dates[-1], len(dates)) if dates else ("", "", 0)


def _source_enabled(args: argparse.Namespace, source: str) -> bool:
    return args.source in {"all", source} or (args.source == "combined" and source in {"kp_dst", "glotec", "omni", "intermagnet", "jma_geomag"})


def _status(source_id: str, source_group: str, probe_status: str, fetch_status: str, aggregate_status: str, modeled_status: str, rows: list[dict], n_fetch_rows: int, reason: str = "") -> dict:
    start, end, days = _coverage(rows)
    return {
        "source_id": source_id,
        "source_group": source_group,
        "dataset_id": "",
        "probe_status": probe_status,
        "fetch_status": fetch_status,
        "aggregate_status": aggregate_status,
        "modeled_status": modeled_status,
        "coverage_start": start,
        "coverage_end": end,
        "coverage_days": days,
        "n_fetch_rows": n_fetch_rows,
        "n_aggregate_rows": len(rows),
        "n_metric_rows": 0,
        "reason": reason,
    }


def _build_external_features(args: argparse.Namespace, output_dir: Path) -> tuple[list[dict], list[dict], dict]:
    features: list[dict] = []
    status_rows: list[dict] = []
    probes: dict = {}

    if _source_enabled(args, "kp_dst"):
        kp_probe = probe_kp(str(output_dir))
        dst_probe = probe_dst(str(output_dir))
        probes["kp"] = kp_probe
        probes["dst"] = dst_probe
        kp_rows = fetch_kp(args.start_date, args.end_date)
        dst_rows = []
        if not args.kp_only:
            dst_rows = fetch_dst(args.start_date, args.end_date, str(output_dir))
        kp_dst_features = build_kp_dst_features(kp_rows, dst_rows, args.start_date, args.end_date)
        features.extend(kp_dst_features)
        status_rows.append(_status("gfz_kp_kyoto_dst", "kp_dst", "probe_ok" if kp_probe.get("status") == "ok" else "probe_error", "fetch_ok", "aggregate_ok", "features_ok", kp_dst_features, len(kp_rows) + len(dst_rows), "Dst included" if dst_rows else "Kp only or Dst not requested"))

    if _source_enabled(args, "omni"):
        omni_probe = probe_omni(str(output_dir))
        probes["omni"] = omni_probe
        omni_rows = fetch_omni(args.start_date, args.end_date, str(output_dir))
        omni_features = build_omni_features(omni_rows, args.start_date, args.end_date)
        features.extend(omni_features)
        status_rows.append(_status("nasa_cdaweb_omni2_h0_mrg1hr", "omni", "probe_ok" if omni_probe.get("status") == "ok" else "probe_error", "fetch_ok" if omni_rows else "fetch_empty", "aggregate_ok" if omni_features else "aggregate_empty", "features_ok" if omni_features else "insufficient_coverage", omni_features, len(omni_rows)))

    if _source_enabled(args, "glotec"):
        glotec_probe = probe_glotec(str(output_dir))
        probes["glotec"] = glotec_probe
        glotec_rows = fetch_glotec(args.start_date, args.end_date, str(output_dir))
        glotec_features = build_glotec_features(glotec_rows, args.start_date, args.end_date)
        features.extend(glotec_features)
        status_rows.append(_status("noaa_swpc_glotec", "glotec", "probe_ok" if glotec_probe.get("status") == "ok" else "probe_error", "insufficient_coverage" if not glotec_rows else "fetch_ok", "aggregate_empty" if not glotec_features else "aggregate_ok", "modeled_not_reached", glotec_features, len(glotec_rows), "Global GloTEC public coverage starts in 2025; requested period has insufficient coverage."))

    if _source_enabled(args, "intermagnet"):
        intermagnet_probe = probe_intermagnet(str(output_dir))
        probes["intermagnet"] = intermagnet_probe
        intermagnet_rows = fetch_intermagnet(args.start_date, args.end_date, str(output_dir))
        intermagnet_features = build_geomag_features(intermagnet_rows, args.start_date, args.end_date)
        features.extend(intermagnet_features)
        status_rows.append(_status("intermagnet_gin", "intermagnet", "probe_ok" if intermagnet_probe.get("status") == "ok" else "probe_error", "probe_only", "aggregate_not_reached", "modeled_not_reached", intermagnet_features, len(intermagnet_rows), "Probe implemented; bulk IAGA/CDF parser deferred."))

    if _source_enabled(args, "jma_geomag"):
        jma_probe = probe_jma_geomag(str(output_dir))
        probes["jma_geomag"] = jma_probe
        jma_rows = fetch_jma_geomag(args.start_date, args.end_date, str(output_dir))
        jma_features = build_geomag_features(jma_rows, args.start_date, args.end_date)
        features.extend(jma_features)
        status_rows.append(_status("jma_kakioka_geomag", "jma_geomag", "probe_ok" if jma_probe.get("status") == "ok" else "probe_error", "probe_only", "aggregate_not_reached", "modeled_not_reached", jma_features, len(jma_rows), "Metadata reachable; file-selection parser deferred."))

    if args.source in {"all", "combined"}:
        combined = build_combined_features(features)
        features.extend(combined)
        status_rows.append(_status("combined_space_weather_features", "combined", "probe_ok", "fetch_not_applicable", "aggregate_ok" if combined else "aggregate_empty", "features_ok" if combined else "modeled_not_reached", combined, 0, "PCA-like proxy features from overlapping fetched source features."))

    return features, status_rows, probes


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    raw_dir = output_dir / "tmp" / "raw"
    ensure_dir(output_dir / "metadata" / "probe_reports")
    ensure_dir(output_dir / "figures")
    ensure_dir(raw_dir)

    records = parse_excel_registry(args.excel, output_dir)

    if args.probe_only:
        features, source_status_rows, probes = _build_external_features(argparse.Namespace(**{**vars(args), "start_date": args.start_date, "end_date": args.start_date}), output_dir)
        status_rows = source_status_rows
        for record in records:
            adapter = adapter_for(record, output_dir, raw_dir, args.keep_raw)
            report = adapter.probe(record)
            status_rows.append(
                {
                    "source_id": "excel_adapter",
                    "source_group": "excel",
                    "dataset_id": record.excel_dataset_id,
                    "probe_status": "probe_ok" if report.get("status") == "ok" else report.get("status", "unknown"),
                    "fetch_status": "not_run",
                    "aggregate_status": "not_run",
                    "modeled_status": "not_run",
                    "coverage_start": "",
                    "coverage_end": "",
                    "coverage_days": 0,
                    "n_fetch_rows": 0,
                    "n_aggregate_rows": 0,
                    "n_metric_rows": 0,
                    "reason": report.get("reason_if_skipped", ""),
                }
            )
        write_csv(output_dir / "space_weather4_pipeline_status.csv", status_rows)
        write_json(output_dir / "metadata" / "probe_summary.json", {"external_probes": probes, "n_excel_records": len(records), "n_probe_features": len(features)})
        return

    features, source_status_rows, probes = _build_external_features(args, output_dir)
    write_csv(output_dir / "metadata" / "space_weather4_features_sample.csv", features[:500])
    write_json(output_dir / "metadata" / "probe_summary.json", {"external_probes": probes, "n_excel_records": len(records), "n_features": len(features)})
    lags = [lag.strip() for lag in args.lags.split(",") if lag.strip()]
    run_all_pairs(
        records=records,
        feature_rows=features,
        output_dir=output_dir,
        raw_dir=raw_dir,
        start_date=args.start_date,
        end_date=args.end_date,
        lags=lags,
        dataset=args.dataset,
        spatial_unit=args.spatial_unit,
        keep_raw=args.keep_raw,
        force=args.force,
        min_samples=args.min_samples,
        source_status_rows=source_status_rows,
    )


if __name__ == "__main__":
    main()
