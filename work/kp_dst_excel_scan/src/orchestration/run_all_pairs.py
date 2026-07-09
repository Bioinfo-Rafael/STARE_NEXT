from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

from src.excel_adapters import adapter_for
from src.excel_adapters.base import SkipDataset
from src.features.lag_features import pair_by_lag
from src.features.static_interactions import static_interaction_placeholder
from src.features.time_features import previous_target_vectors, residualize_controls
from src.modeling.correlations import pearson, spearman
from src.modeling.evaluation import candidate_filter
from src.modeling.glm_models import ols_coef
from src.modeling.logistic import auc_score, average_precision, logistic_fit
from src.modeling.multiple_testing import benjamini_hochberg
from src.modeling.negative_controls import combined_negative_control
from src.modeling.poisson import poisson_log_rate_ratio
from src.registry.dataset_registry import DatasetRecord
from src.utils.dates import lag_direction
from src.utils.io import append_jsonl, cleanup_dir, ensure_dir, write_csv, write_json
from src.utils.schema import KP_DST_METRIC_FIELDS

STATUS_FIELDS = ["excel_dataset_id", "probe_status", "fetch_status", "aggregate_status", "modeled_status", "n_fetch_rows", "n_aggregate_rows", "n_metric_rows", "reason"]


def _group(rows: list[dict], key: str) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        out[str(row[key])].append(row)
    return dict(out)


def _dedupe_records(records: list[DatasetRecord]) -> list[DatasetRecord]:
    seen: set[str] = set()
    out: list[DatasetRecord] = []
    for record in records:
        key = record.excel_dataset_id
        if key in seen:
            continue
        seen.add(key)
        out.append(record)
    return out


def _split_period(dates: list[str], start_date: str, end_date: str) -> tuple[str, str]:
    if not dates:
        return "", ""
    if dates[0] <= "2023-06-30" and dates[-1] >= "2023-07-01":
        train_end = min("2023-06-30", dates[-1])
        test_start = max("2023-07-01", dates[0])
    else:
        split = max(1, int(len(dates) * 0.7))
        train_end = dates[split - 1]
        test_start = dates[min(split, len(dates) - 1)]
    assert dates[0] <= train_end <= test_start <= dates[-1]
    return f"{dates[0]}..{train_end}", f"{test_start}..{dates[-1]}"


def _score_feature_target(
    feature_rows: list[dict],
    target_rows: list[dict],
    record: DatasetRecord,
    lags: list[str],
    spatial_unit: str,
    min_samples: int,
) -> list[dict]:
    metrics: list[dict] = []
    feature_groups = _group(feature_rows, "kp_dst_feature_name")
    target_groups = _group(target_rows, "target_name")
    target_types = {target: rows[0].get("target_type", record.inferred_temporal_type) for target, rows in target_groups.items() if rows}
    target_by_name_date = {target: {r["date"]: float(r["value"]) for r in rows} for target, rows in target_groups.items()}
    feature_lag_cache: dict[tuple[str, str], tuple[list[str], list[float], list[float], dict]] = {}
    target_lag_cache: dict[tuple[str, str], tuple[list[float], list[float], dict[str, list[float]]]] = {}
    for feature_name, frows in feature_groups.items():
        meta = frows[0]
        for lag in lags:
            cache_key = (feature_name, lag)
            if cache_key not in feature_lag_cache:
                any_target_rows = next(iter(target_groups.values()))
                paired = sorted(pair_by_lag(frows, any_target_rows, lag), key=lambda r: r["date"])
                dates = [p["date"] for p in paired]
                xs_raw = [float(p["x"]) for p in paired]
                xs = residualize_controls(xs_raw, dates) if len(xs_raw) >= min_samples else xs_raw
                feature_lag_cache[cache_key] = (dates, xs_raw, xs, meta)
            dates, xs_raw, xs, meta = feature_lag_cache[cache_key]
            for target_name, trows in target_groups.items():
                target_cache_key = (target_name, lag)
                if target_cache_key not in target_lag_cache:
                    target_by_date = target_by_name_date[target_name]
                    ys_raw_cached = [float(target_by_date.get(d, 0.0)) for d in dates]
                    prev_cached = previous_target_vectors(target_by_date, dates)
                    ys_cached = residualize_controls(ys_raw_cached, dates, prev_cached) if len(ys_raw_cached) >= min_samples else ys_raw_cached
                    target_lag_cache[target_cache_key] = (ys_raw_cached, ys_cached, prev_cached)
                ys_raw, ys, _prev = target_lag_cache[target_cache_key]
                base: dict[str, Any] = {
                    "kp_dst_feature_name": feature_name,
                    "base_feature_name": meta.get("base_feature_name", feature_name),
                    "feature_adjustment": meta.get("feature_adjustment", ""),
                    "excel_dataset_id": record.excel_dataset_id,
                    "excel_dataset_name": record.name,
                    "excel_category": record.category,
                    "target_name": target_name,
                    "target_type": target_types.get(target_name, record.inferred_temporal_type),
                    "spatial_unit": spatial_unit,
                    "region": "national",
                    "lag": lag,
                    "lag_direction": lag_direction(lag),
                    "n_samples": len(xs_raw),
                }
                if len(xs_raw) < min_samples:
                    metrics.append({**base, "status": "insufficient_data", "error_message": f"n_samples<{min_samples}"})
                    continue
                corr = pearson(xs, ys)
                sp = spearman(xs, ys)
                neg_corr, neg_pass = combined_negative_control(xs, ys, dates)
                ols, ols_p = ols_coef(xs, ys)
                is_flag = target_name.endswith("_flag")
                is_count = target_name.endswith("count") or target_name == "count"
                log_coef = odds = auc = ap = None
                if is_flag:
                    log_coef, odds = logistic_fit(xs, ys_raw)
                    auc = auc_score(xs, ys_raw)
                    ap = average_precision(xs, ys_raw)
                pois_coef = pois_rr = None
                if is_count:
                    pois_coef, pois_rr = poisson_log_rate_ratio(xs, ys_raw)
                train_period, test_period = _split_period(dates, dates[0], dates[-1])
                metrics.append(
                    {
                        **base,
                        "model_type": "calendar_autocorrelation_adjusted",
                        "correlation": corr,
                        "spearman": sp,
                        "partial_correlation": corr,
                        "ols_coefficient": ols,
                        "ols_p_value": ols_p,
                        "logistic_coefficient": log_coef,
                        "logistic_odds_ratio": odds,
                        "AUC": auc,
                        "average_precision": ap,
                        "poisson_coefficient": pois_coef,
                        "poisson_rate_ratio": pois_rr,
                        "poisson_p_value": "",
                        "negative_control_correlation": neg_corr,
                        "negative_control_pass": neg_pass,
                        "train_period": train_period,
                        "test_period": test_period,
                        "status": "ok",
                        "error_message": "",
                    }
                )
    return metrics


def _top_markdown(metrics: list[dict], candidates: list[dict], post_rows: list[dict], static_rows: list[dict], status_rows: list[dict]) -> str:
    def strength(row: dict) -> float:
        auc = row.get("AUC")
        if auc not in {"", None}:
            try:
                return abs(float(auc) - 0.5) * 2
            except Exception:
                pass
        try:
            return abs(float(row.get("correlation") or 0))
        except Exception:
            return 0.0

    def is_earthquake_catalog(row: dict) -> bool:
        blob = f"{row.get('target_type')} {row.get('excel_dataset_name')} {row.get('excel_category')} {row.get('target_name')}"
        return row.get("target_type") == "event_catalog" or any(k in blob for k in ["地震月報", "震源", "震度", "カタログ", "Hi-net", "F-net"])

    def unique_rows(rows: list[dict]) -> list[dict]:
        seen: set[tuple] = set()
        out: list[dict] = []
        for row in rows:
            key = (
                row.get("kp_dst_feature_name"),
                row.get("excel_dataset_id"),
                row.get("target_name"),
                row.get("lag"),
                row.get("lag_direction"),
            )
            if key in seen:
                continue
            seen.add(key)
            out.append(row)
        return out

    def section(title: str, rows: list[dict], limit: int = 10) -> list[str]:
        lines = [f"# {title}", ""]
        rows = unique_rows(rows)
        if not rows:
            return lines + ["No rows matched this section.", ""]
        for i, row in enumerate(sorted(rows, key=strength, reverse=True)[:limit], 1):
            lines += [
                f"## {i}. {row.get('kp_dst_feature_name')} × {row.get('excel_dataset_name')}:{row.get('target_name')}",
                f"- lag: {row.get('lag')} ({row.get('lag_direction')})",
                f"- adjustment: {row.get('feature_adjustment')}",
                f"- n: {row.get('n_samples')}",
                f"- corr / partial: {row.get('correlation')} / {row.get('partial_correlation')}",
                f"- AUC / AP: {row.get('AUC')} / {row.get('average_precision')}",
                f"- poisson_rate_ratio: {row.get('poisson_rate_ratio')}",
                f"- negative control: {row.get('negative_control_correlation')} pass={row.get('negative_control_pass')}",
                f"- FDR: {row.get('fdr_q_value')}",
                "",
            ]
        return lines

    ok = [r for r in metrics if r.get("status") == "ok"]
    lines = [
        "# Executive Summary",
        "",
        "This Kp/Dst-only scan is exploratory. It ranks associations after calendar/autocorrelation controls and negative controls, but does not imply earthquake prediction or causality.",
        f"- Metric rows: {len(metrics)}",
        f"- Candidate precursor rows: {len(candidates)}",
        "",
    ]
    lines += section("Best Candidate Precursors", candidates)
    lines += section("Kp/Dst vs Earthquake Catalogs", [r for r in ok if is_earthquake_catalog(r)])
    lines += section("Kp/Dst vs Intensity Data", [r for r in ok if "intensity" in str(r.get("target_name", "")) or "震度" in str(r.get("excel_dataset_name", ""))])
    lines += section("Kp/Dst vs GNSS / Geodetic Data", [r for r in ok if any(k in str(r.get("excel_dataset_name", "")) for k in ["GNSS", "GEONET", "測地", "地殻"])])
    lines += section("Kp/Dst vs Groundwater / Tide / Ocean Data", [r for r in ok if any(k in str(r.get("excel_dataset_name", "")) for k in ["地下水", "潮位", "NOWPHAS", "験潮", "海洋"])])
    lines += section("Kp/Dst vs Geomagnetic Observatory Data", [r for r in ok if "地磁気" in str(r.get("excel_dataset_name", ""))])
    lines += ["# Static Spatial Interaction Results", ""]
    lines += [f"- {r.get('excel_dataset_name')}: {r.get('status')} ({r.get('reason')})" for r in static_rows[:30]] or ["No static spatial records detected."]
    lines += [""] + section("Post-Earthquake / Reverse-Lag Signals", post_rows)
    lines += ["# Failed or Skipped Excel Datasets", ""]
    lines += [f"- {r['excel_dataset_id']}: {r.get('modeled_status')} {r.get('reason')}" for r in status_rows if r.get("modeled_status") != "modeled_ok"][:80]
    lines += [
        "",
        "# Interpretation Notes",
        "",
        "- external_precedes_target means Kp/Dst leads the Excel target by the lag.",
        "- target_precedes_external is reverse-lag/post-reaction comparison.",
        "- All tests are multiple-comparison exploratory screens.",
        "",
        "# What to Verify Next",
        "",
        "- Confirm Dst parser coverage for months with final/provisional data.",
        "- Add implemented parsers for GNSS, tide, groundwater, intensity, and geomagnetic observatory datasets.",
        "- Refit promising rows with statsmodels GLM/HAC standard errors.",
    ]
    return "\n".join(lines)


def run_all_pairs(records: list[DatasetRecord], feature_rows: list[dict], output_dir: str | Path, raw_dir: str | Path, start_date: str, end_date: str, lags: list[str], dataset: str, spatial_unit: str, keep_raw: bool, force: bool, min_samples: int = 365) -> list[dict]:
    output_dir = Path(output_dir)
    raw_dir = Path(raw_dir)
    ensure_dir(output_dir)
    selected = records if dataset == "all" else [r for r in records if r.excel_dataset_id == dataset or r.name == dataset]
    selected = _dedupe_records(selected)
    metrics: list[dict] = []
    status_rows: list[dict] = []
    for record in selected:
        adapter = adapter_for(record, output_dir, raw_dir, keep_raw)
        status = {"excel_dataset_id": record.excel_dataset_id, "probe_status": "", "fetch_status": "", "aggregate_status": "", "modeled_status": "", "n_fetch_rows": 0, "n_aggregate_rows": 0, "n_metric_rows": 0, "reason": ""}
        probe = adapter.probe(record)
        status["probe_status"] = "probe_ok" if probe.get("status") == "ok" else str(probe.get("status"))
        if record.inferred_temporal_type in {"static_spatial", "static_metadata"}:
            status.update({"fetch_status": "static_only", "aggregate_status": "static_only", "modeled_status": "static_only", "reason": "static data recorded for future interaction analysis"})
            status_rows.append(status)
            continue
        try:
            fetched = adapter.fetch(record, start_date, end_date)
            status["fetch_status"] = "fetch_ok"
            status["n_fetch_rows"] = len(fetched)
            agg = adapter.aggregate(record, fetched, start_date, end_date, spatial_unit)
            status["aggregate_status"] = "aggregate_ok"
            status["n_aggregate_rows"] = len(agg)
            if not agg:
                raise SkipDataset("no aggregate rows")
            rec_metrics = _score_feature_target(feature_rows, agg, record, lags, spatial_unit, min_samples)
            status["n_metric_rows"] = len(rec_metrics)
            status["modeled_status"] = "modeled_ok" if any(r.get("status") == "ok" for r in rec_metrics) else "modeled_insufficient_data"
            metrics.extend(rec_metrics)
        except SkipDataset as exc:
            status.update({"fetch_status": status["fetch_status"] or "fetch_skip", "aggregate_status": status["aggregate_status"] or "aggregate_not_reached", "modeled_status": "modeled_not_reached", "reason": str(exc)})
        except Exception as exc:
            status.update({"fetch_status": status["fetch_status"] or "fetch_error", "aggregate_status": status["aggregate_status"] or "aggregate_not_reached", "modeled_status": "modeled_not_reached", "reason": f"{type(exc).__name__}: {exc}"})
            append_jsonl(output_dir / "kp_dst_failures.jsonl", {"excel_dataset_id": record.excel_dataset_id, "status": "error", "error_type": type(exc).__name__, "error_message": str(exc)})
        status_rows.append(status)
    metrics = benjamini_hochberg(metrics)
    candidates = [r for r in metrics if candidate_filter(r)]
    post_rows = [r for r in metrics if r.get("lag_direction") == "target_precedes_external"]
    static_rows = static_interaction_placeholder(records)
    write_csv(output_dir / "kp_dst_pipeline_status.csv", status_rows, STATUS_FIELDS)
    write_csv(output_dir / "kp_dst_per_pair_metrics.csv", metrics)
    write_csv(output_dir / "kp_dst_summary.csv", metrics)
    write_csv(output_dir / "kp_dst_candidate_precursors.csv", candidates)
    write_csv(output_dir / "kp_dst_post_reaction.csv", post_rows)
    write_csv(output_dir / "kp_dst_static_interactions.csv", static_rows)
    write_csv(output_dir / "kp_dst_negative_controls.csv", metrics)
    (output_dir / "kp_dst_top_findings.md").write_text(_top_markdown(metrics, candidates, post_rows, static_rows, status_rows), encoding="utf-8")
    _write_figures(output_dir, metrics)
    write_json(output_dir / "metadata" / "run_summary.json", {"n_metrics": len(metrics), "n_candidates": len(candidates), "start_date": start_date, "end_date": end_date})
    if not keep_raw:
        cleanup_dir(raw_dir)
    return metrics


def _write_figures(output_dir: Path, metrics: list[dict]) -> None:
    fig = ensure_dir(output_dir / "figures")
    ok = [r for r in metrics if r.get("status") == "ok"]
    by_dataset: dict[tuple[str, str], float] = {}
    for r in ok:
        try:
            val = abs(float(r.get("correlation") or 0))
        except Exception:
            val = 0.0
        key = (str(r.get("kp_dst_feature_name")), str(r.get("excel_dataset_name")))
        by_dataset[key] = max(by_dataset.get(key, 0.0), val)
    bars = "".join(f'<rect x="{20+i*6}" y="{180-v*150}" width="4" height="{v*150}" fill="#277da1"/>' for i, v in enumerate(list(by_dataset.values())[:100]))
    (fig / "heatmap_feature_dataset_max_abs_correlation.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="220">{bars}<text x="20" y="205">Kp/Dst feature x Excel dataset max |correlation|</text></svg>', encoding="utf-8")
    auc_vals = []
    for r in ok:
        try:
            auc_vals.append(abs(float(r.get("AUC")) - 0.5) * 2)
        except Exception:
            pass
    bars = "".join(f'<rect x="{20+i*6}" y="{180-v*150}" width="4" height="{v*150}" fill="#f9844a"/>' for i, v in enumerate(auc_vals[:100]))
    (fig / "heatmap_feature_target_max_auc.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="220">{bars}<text x="20" y="205">Kp/Dst feature x target AUC strength</text></svg>', encoding="utf-8")
    for name in ["lag_profile_top_candidates.svg", "kp_dst_vs_target_timeseries.svg", "negative_control_comparison.svg", "candidate_precursor_map.svg"]:
        (fig / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="120"><text x="20" y="45">{name}: generated placeholder for MVP; CSV contains plotted values.</text></svg>', encoding="utf-8")
