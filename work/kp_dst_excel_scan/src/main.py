from __future__ import annotations

import argparse
from pathlib import Path

from src.excel_adapters import adapter_for
from src.external.dst_fetch import fetch_dst, probe_dst
from src.external.kp_dst_features import build_kp_dst_features
from src.external.kp_fetch import fetch_kp, probe_kp
from src.orchestration.run_all_pairs import run_all_pairs
from src.registry.parse_excel_registry import parse_excel_registry
from src.utils.io import ensure_dir, write_csv, write_json

DEFAULT_LAGS = "-30D,-14D,-7D,-3D,-1D,0D,1D,3D,7D,14D,30D"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Focused Kp/Dst scan against Excel-listed earthquake/geodetic datasets")
    parser.add_argument("--excel", default="../../資料3_地震・測地データの一覧.xlsx")
    parser.add_argument("--start-date", default="2020-01-01")
    parser.add_argument("--end-date", default="2024-12-31")
    parser.add_argument("--spatial-unit", default="national")
    parser.add_argument("--lags", default=DEFAULT_LAGS)
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--dataset", default="all")
    parser.add_argument("--probe-only", action="store_true")
    parser.add_argument("--kp-only", action="store_true")
    parser.add_argument("--include-dst", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--keep-raw", action="store_true")
    parser.add_argument("--cleanup-raw", default="true")
    parser.add_argument("--min-samples", type=int, default=365)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    raw_dir = output_dir / "tmp" / "raw"
    ensure_dir(output_dir / "metadata" / "probe_reports")
    ensure_dir(output_dir / "figures")
    ensure_dir(raw_dir)

    records = parse_excel_registry(args.excel, output_dir)
    kp_probe = probe_kp(str(output_dir))
    dst_probe = probe_dst(str(output_dir))

    if args.probe_only:
        status_rows = []
        for record in records:
            adapter = adapter_for(record, output_dir, raw_dir, args.keep_raw)
            report = adapter.probe(record)
            status_rows.append(
                {
                    "excel_dataset_id": record.excel_dataset_id,
                    "probe_status": "probe_ok" if report.get("status") == "ok" else report.get("status", "unknown"),
                    "fetch_status": "not_run",
                    "aggregate_status": "not_run",
                    "modeled_status": "not_run",
                    "n_fetch_rows": 0,
                    "n_aggregate_rows": 0,
                    "n_metric_rows": 0,
                    "reason": report.get("reason_if_skipped", ""),
                }
            )
        write_csv(output_dir / "kp_dst_pipeline_status.csv", status_rows)
        write_json(output_dir / "metadata" / "probe_summary.json", {"kp": kp_probe, "dst": dst_probe, "n_excel_records": len(records)})
        return

    kp_rows = fetch_kp(args.start_date, args.end_date)
    dst_rows = []
    if args.include_dst and not args.kp_only:
        dst_rows = fetch_dst(args.start_date, args.end_date, str(output_dir))
    features = build_kp_dst_features(kp_rows, dst_rows, args.start_date, args.end_date)
    write_csv(output_dir / "metadata" / "kp_dst_features_sample.csv", features[:200])
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
    )


if __name__ == "__main__":
    main()
