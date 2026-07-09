from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import random
from typing import Any

from src.excel_adapters import adapter_for
from src.excel_adapters.base import SkipDataset
from src.features.lag_features import pair_by_lag
from src.features.static_interactions import static_interaction_placeholder
from src.features.time_features import previous_target_vectors, residualize_controls
from src.modeling.correlations import pearson
from src.modeling.evaluation import candidate_filter, near_miss_filter, reject_reasons
from src.modeling.glm_models import ols_coef
from src.modeling.lag_asymmetry import lag_asymmetry_rows
from src.modeling.logistic import auc_score, average_precision, brier_score, logistic_fit
from src.modeling.multiple_testing import benjamini_hochberg
from src.modeling.poisson import poisson_log_rate_ratio
from src.registry.dataset_registry import DatasetRecord
from src.utils.dates import lag_direction
from src.utils.io import append_jsonl, cleanup_dir, ensure_dir, write_csv, write_json
from src.utils.schema import SPACE_WEATHER4_METRIC_FIELDS

STATUS_FIELDS = [
    "source_id",
    "source_group",
    "dataset_id",
    "probe_status",
    "fetch_status",
    "aggregate_status",
    "modeled_status",
    "coverage_start",
    "coverage_end",
    "coverage_days",
    "n_fetch_rows",
    "n_aggregate_rows",
    "n_metric_rows",
    "reason",
]


def _group(rows: list[dict], key: str) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        out[str(row[key])].append(row)
    return dict(out)


def _dedupe_records(records: list[DatasetRecord]) -> list[DatasetRecord]:
    seen: set[str] = set()
    out: list[DatasetRecord] = []
    for record in records:
        if record.excel_dataset_id in seen:
            continue
        seen.add(record.excel_dataset_id)
        out.append(record)
    return out


def _split_period(dates: list[str]) -> tuple[str, str]:
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


def _coverage(rows: list[dict]) -> tuple[str, str, int]:
    dates = sorted({str(r.get("date", "")) for r in rows if r.get("date")})
    return (dates[0], dates[-1], len(dates)) if dates else ("", "", 0)


def _ranks(values: list[float]) -> list[float]:
    ordered = sorted(enumerate(values), key=lambda kv: kv[1])
    out = [0.0] * len(values)
    i = 0
    while i < len(ordered):
        j = i
        while j + 1 < len(ordered) and ordered[j + 1][1] == ordered[i][1]:
            j += 1
        rank = (i + j + 2) / 2
        for k in range(i, j + 1):
            out[ordered[k][0]] = rank
        i = j + 1
    return out


def _negative_control_vectors(ys: list[float], dates: list[str]) -> list[list[float]]:
    out: list[list[float]] = []
    shuffled = ys[:]
    random.Random(42).shuffle(shuffled)
    out.append(shuffled)
    groups: dict[str, list[int]] = {}
    for i, date in enumerate(dates):
        groups.setdefault(date[:7], []).append(i)
    month_keys = list(groups)
    random.Random(43).shuffle(month_keys)
    month_shuffled: list[float] = []
    for key in month_keys:
        month_shuffled.extend(ys[i] for i in groups[key])
    out.append(month_shuffled[: len(ys)])
    by_doy: dict[str, list[float]] = {}
    for y, date in zip(ys, dates):
        by_doy.setdefault(date[5:], []).append(y)
    rng = random.Random(44)
    out.append([rng.choice(by_doy.get(date[5:], [0.0])) for date in dates])
    if len(ys) >= 3:
        shift = max(1, len(ys) // 3)
        out.append(ys[shift:] + ys[:shift])
    return out


def _score_feature_target(feature_rows: list[dict], target_rows: list[dict], record: DatasetRecord, lags: list[str], spatial_unit: str, min_samples: int) -> list[dict]:
    metrics: list[dict] = []
    feature_groups = _group(feature_rows, "external_feature_name")
    target_groups = _group(target_rows, "target_name")
    target_types = {target: rows[0].get("target_type", record.inferred_temporal_type) for target, rows in target_groups.items() if rows}
    target_by_name_date = {target: {r["date"]: float(r["value"]) for r in rows} for target, rows in target_groups.items()}
    feature_lag_cache: dict[tuple[str, str], tuple[list[str], list[float], list[float], list[float], dict]] = {}
    target_lag_cache: dict[tuple[str, str, str, str, int], tuple[list[float], list[float], list[float], list[list[float]]]] = {}

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
                xs_rank = _ranks(xs) if len(xs_raw) >= min_samples else []
                feature_lag_cache[cache_key] = (dates, xs_raw, xs, xs_rank, meta)
            dates, xs_raw, xs, xs_rank, meta = feature_lag_cache[cache_key]
            if not dates:
                continue
            for target_name in target_groups:
                target_cache_key = (target_name, lag, dates[0], dates[-1], len(dates))
                if target_cache_key not in target_lag_cache:
                    target_by_date = target_by_name_date[target_name]
                    ys_raw_cached = [float(target_by_date.get(d, 0.0)) for d in dates]
                    prev_cached = previous_target_vectors(target_by_date, dates)
                    ys_cached = residualize_controls(ys_raw_cached, dates, prev_cached) if len(ys_raw_cached) >= min_samples else ys_raw_cached
                    ys_rank = _ranks(ys_cached) if len(ys_raw_cached) >= min_samples else []
                    neg_vectors = _negative_control_vectors(ys_cached, dates) if len(ys_raw_cached) >= min_samples else []
                    target_lag_cache[target_cache_key] = (ys_raw_cached, ys_cached, ys_rank, neg_vectors)
                ys_raw, ys, ys_rank, neg_vectors = target_lag_cache[target_cache_key]
                base: dict[str, Any] = {
                    "external_source_group": meta.get("external_source_group", "unknown"),
                    "external_feature_name": feature_name,
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
                sp = pearson(xs_rank, ys_rank)
                neg_vals = [v for v in (pearson(xs, neg_y) for neg_y in neg_vectors) if v is not None]
                neg_corr = max(neg_vals, key=lambda v: abs(v)) if neg_vals else None
                neg_pass = bool(corr is not None and neg_corr is not None and abs(corr) > abs(neg_corr))
                neg_auc = None
                ols, ols_p = ols_coef(xs, ys)
                is_flag = target_name.endswith("_flag")
                is_count = target_name.endswith("count") or target_name == "count"
                log_coef = odds = auc = ap = brier = None
                if is_flag:
                    log_coef, odds = logistic_fit(xs, ys_raw)
                    auc = auc_score(xs, ys_raw)
                    ap = average_precision(xs, ys_raw)
                    brier = brier_score(xs, ys_raw)
                    neg_auc = auc_score(xs, list(reversed(ys_raw)))
                pois_coef = pois_rr = None
                if is_count:
                    pois_coef, pois_rr = poisson_log_rate_ratio(xs, ys_raw)
                train_period, test_period = _split_period(dates)
                metrics.append(
                    {
                        **base,
                        "model_type": "univariate_calendar_autocorrelation_adjusted",
                        "correlation": corr,
                        "spearman": sp,
                        "partial_correlation": corr,
                        "ols_coefficient": ols,
                        "ols_p_value": ols_p,
                        "logistic_coefficient": log_coef,
                        "logistic_odds_ratio": odds,
                        "AUC": auc,
                        "average_precision": ap,
                        "brier_score": brier,
                        "poisson_coefficient": pois_coef,
                        "poisson_rate_ratio": pois_rr,
                        "poisson_p_value": "",
                        "negative_control_correlation": neg_corr,
                        "negative_control_auc": neg_auc,
                        "negative_control_pass": neg_pass,
                        "best_reverse_lag_score": "",
                        "precursor_minus_reverse_score": "",
                        "train_period": train_period,
                        "test_period": test_period,
                        "status": "ok",
                        "error_message": "",
                    }
                )
    return metrics


def _annotate_reverse_lag(metrics: list[dict]) -> list[dict]:
    reverse_best: dict[tuple, float] = defaultdict(float)
    precursor_best: dict[tuple, float] = defaultdict(float)
    for row in metrics:
        if row.get("status") != "ok":
            continue
        key = (row.get("external_source_group"), row.get("external_feature_name"), row.get("excel_dataset_id"), row.get("target_name"))
        try:
            score = abs(float(row.get("correlation") or 0))
        except Exception:
            score = 0.0
        if row.get("lag_direction") == "target_precedes_external":
            reverse_best[key] = max(reverse_best[key], score)
        if row.get("lag_direction") == "external_precedes_target":
            precursor_best[key] = max(precursor_best[key], score)
    for row in metrics:
        key = (row.get("external_source_group"), row.get("external_feature_name"), row.get("excel_dataset_id"), row.get("target_name"))
        rev = reverse_best.get(key, 0.0)
        pre = precursor_best.get(key, 0.0)
        row["best_reverse_lag_score"] = rev
        row["precursor_minus_reverse_score"] = pre - rev
    return metrics


def _add_reject_reasons(metrics: list[dict]) -> list[dict]:
    for row in metrics:
        row["reject_reasons"] = ";".join(reject_reasons(row, strict=True))
    return metrics


def _top_markdown(metrics: list[dict], candidates: list[dict], near_miss: list[dict], post_rows: list[dict], status_rows: list[dict]) -> str:
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

    def section(title: str, rows: list[dict], limit: int = 10) -> list[str]:
        lines = [f"# {title}", ""]
        if not rows:
            return lines + ["No rows matched this section.", ""]
        for i, row in enumerate(sorted(rows, key=strength, reverse=True)[:limit], 1):
            lines += [
                f"## {i}. {row.get('external_source_group')}:{row.get('external_feature_name')} x {row.get('excel_dataset_name')}:{row.get('target_name')}",
                f"- lag: {row.get('lag')} ({row.get('lag_direction')})",
                f"- adjustment: {row.get('feature_adjustment')}",
                f"- n: {row.get('n_samples')}",
                f"- corr / partial: {row.get('correlation')} / {row.get('partial_correlation')}",
                f"- AUC / AP / Brier: {row.get('AUC')} / {row.get('average_precision')} / {row.get('brier_score')}",
                f"- poisson_rate_ratio: {row.get('poisson_rate_ratio')}",
                f"- negative control: {row.get('negative_control_correlation')} pass={row.get('negative_control_pass')}",
                f"- reverse best / pre-minus-reverse: {row.get('best_reverse_lag_score')} / {row.get('precursor_minus_reverse_score')}",
                f"- FDR: {row.get('fdr_q_value')}",
                "",
            ]
        return lines

    ok = [r for r in metrics if r.get("status") == "ok"]
    by_group = defaultdict(int)
    for row in ok:
        by_group[row.get("external_source_group")] += 1
    lines = [
        "# Executive Summary",
        "",
        "This four-source space-weather scan is exploratory. It ranks lagged associations after calendar/autocorrelation controls, negative controls, FDR, and reverse-lag comparison. It does not imply earthquake prediction or causality.",
        f"- Metric rows: {len(metrics)}",
        f"- Strict candidate rows: {len(candidates)}",
        f"- Near-miss rows: {len(near_miss)}",
        f"- Modeled rows by source group: {dict(by_group)}",
        "",
        "# Data Coverage",
        "",
    ]
    for row in status_rows:
        lines.append(f"- {row.get('source_group')} / {row.get('dataset_id') or row.get('source_id')}: {row.get('coverage_start')}..{row.get('coverage_end')} days={row.get('coverage_days')} status={row.get('modeled_status') or row.get('fetch_status')} {row.get('reason')}")
    lines += [""]
    lines += section("Strict Candidate Precursors", candidates)
    lines += section("Near-Miss Candidate Precursors", near_miss)
    lines += section("Kp/Dst Results", [r for r in ok if r.get("external_source_group") == "kp_dst"])
    lines += section("NOAA GloTEC / TEC Results", [r for r in ok if r.get("external_source_group") == "glotec"])
    lines += section("NASA OMNI / CDAWeb Results", [r for r in ok if r.get("external_source_group") == "omni"])
    lines += section("INTERMAGNET / JMA Geomagnetic Results", [r for r in ok if r.get("external_source_group") in {"intermagnet", "jma_geomag", "geomag_observatory"}])
    lines += section("Combined Space Weather Feature Results", [r for r in ok if r.get("external_source_group") == "combined"])
    lines += section("Results by Excel Dataset Category", ok)
    lines += section("Reverse-Lag / Post-Reaction Signals", post_rows)
    lines += ["# Failed or Skipped Datasets", ""]
    skipped = [r for r in status_rows if r.get("modeled_status") not in {"modeled_ok", ""} or r.get("fetch_status") in {"insufficient_coverage", "probe_only", "fetch_skip"}]
    lines += [f"- {r.get('source_group')} / {r.get('dataset_id') or r.get('source_id')}: {r.get('modeled_status')} {r.get('reason')}" for r in skipped[:100]] or ["No failed/skipped rows recorded."]
    lines += [
        "",
        "# Interpretation Notes",
        "",
        "- external_precedes_target means the external space-weather feature leads the Excel target by the lag.",
        "- target_precedes_external is a reverse-lag/post-reaction comparison.",
        "- Candidate rows are strict filters over a broad multiple-comparison screen; absence of candidates is not a pipeline failure.",
        "",
        "# What to Verify Next",
        "",
        "- Implement archival GloTEC/US-TEC access for periods before global GloTEC coverage.",
        "- Add robust IAGA/CDF parsing for INTERMAGNET and JMA Kakioka observatory files.",
        "- Add multivariate Ridge/GLM source-group models after univariate coverage is stable.",
    ]
    return "\n".join(lines)


def run_all_pairs(records: list[DatasetRecord], feature_rows: list[dict], output_dir: str | Path, raw_dir: str | Path, start_date: str, end_date: str, lags: list[str], dataset: str, spatial_unit: str, keep_raw: bool, force: bool, min_samples: int = 365, source_status_rows: list[dict] | None = None) -> list[dict]:
    output_dir = Path(output_dir)
    raw_dir = Path(raw_dir)
    ensure_dir(output_dir)
    selected = records if dataset == "all" else [r for r in records if r.excel_dataset_id == dataset or r.name == dataset]
    selected = _dedupe_records(selected)
    metrics: list[dict] = []
    status_rows: list[dict] = list(source_status_rows or [])
    feat_start, feat_end, feat_days = _coverage(feature_rows)

    for record in selected:
        adapter = adapter_for(record, output_dir, raw_dir, keep_raw)
        status = {"source_id": "excel_adapter", "source_group": "excel", "dataset_id": record.excel_dataset_id, "probe_status": "", "fetch_status": "", "aggregate_status": "", "modeled_status": "", "coverage_start": "", "coverage_end": "", "coverage_days": 0, "n_fetch_rows": 0, "n_aggregate_rows": 0, "n_metric_rows": 0, "reason": ""}
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
            a_start, a_end, a_days = _coverage(agg)
            status.update({"aggregate_status": "aggregate_ok", "n_aggregate_rows": len(agg), "coverage_start": a_start, "coverage_end": a_end, "coverage_days": a_days})
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
            append_jsonl(output_dir / "space_weather4_failures.jsonl", {"dataset_id": record.excel_dataset_id, "status": "error", "error_type": type(exc).__name__, "error_message": str(exc)})
        status_rows.append(status)

    metrics = _annotate_reverse_lag(benjamini_hochberg(metrics))
    metrics = _add_reject_reasons(metrics)
    candidates = [r for r in metrics if candidate_filter(r)]
    near_miss = [r for r in metrics if near_miss_filter(r)]
    post_rows = [r for r in metrics if r.get("lag_direction") == "target_precedes_external"]
    asymmetry = lag_asymmetry_rows(metrics)

    write_csv(output_dir / "space_weather4_pipeline_status.csv", status_rows, STATUS_FIELDS)
    write_csv(output_dir / "space_weather4_per_pair_metrics.csv", metrics, SPACE_WEATHER4_METRIC_FIELDS)
    write_csv(output_dir / "space_weather4_candidate_precursors.csv", candidates, SPACE_WEATHER4_METRIC_FIELDS)
    write_csv(output_dir / "space_weather4_near_miss_candidates.csv", near_miss, SPACE_WEATHER4_METRIC_FIELDS)
    write_csv(output_dir / "space_weather4_post_reaction.csv", post_rows, SPACE_WEATHER4_METRIC_FIELDS)
    write_csv(output_dir / "space_weather4_lag_asymmetry.csv", asymmetry)
    write_csv(output_dir / "space_weather4_negative_controls.csv", metrics, SPACE_WEATHER4_METRIC_FIELDS)
    write_csv(output_dir / "space_weather4_combined_model_metrics.csv", [{"status": "not_implemented_mvp", "reason": "univariate screening implemented first"}])
    (output_dir / "space_weather4_top_findings.md").write_text(_top_markdown(metrics, candidates, near_miss, post_rows, status_rows), encoding="utf-8")
    _write_figures(output_dir, metrics, status_rows)
    write_json(output_dir / "metadata" / "run_summary.json", {"n_metrics": len(metrics), "n_candidates": len(candidates), "n_near_miss": len(near_miss), "feature_coverage_start": feat_start, "feature_coverage_end": feat_end, "feature_coverage_days": feat_days, "start_date": start_date, "end_date": end_date})
    if not keep_raw:
        cleanup_dir(raw_dir)
    return metrics


def _write_figures(output_dir: Path, metrics: list[dict], status_rows: list[dict]) -> None:
    fig = ensure_dir(output_dir / "figures")
    ok = [r for r in metrics if r.get("status") == "ok"]
    vals = []
    for row in ok[:160]:
        try:
            vals.append(abs(float(row.get("correlation") or 0)))
        except Exception:
            vals.append(0.0)
    bars = "".join(f'<rect x="{20+i*4}" y="{180-v*150}" width="3" height="{v*150}" fill="#277da1"/>' for i, v in enumerate(vals))
    (fig / "heatmap_external_feature_target_max_abs_correlation.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="220">{bars}<text x="20" y="205">external feature x target max |correlation|</text></svg>', encoding="utf-8")
    group_counts = defaultdict(int)
    for row in ok:
        group_counts[row.get("external_source_group")] += 1
    bars = "".join(f'<rect x="{40+i*80}" y="{180-min(v,1000)/1000*140}" width="50" height="{min(v,1000)/1000*140}" fill="#4d908e"/><text x="{40+i*80}" y="200">{k}</text>' for i, (k, v) in enumerate(group_counts.items()))
    (fig / "heatmap_source_group_excel_dataset_max_score.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="230">{bars}</svg>', encoding="utf-8")
    for name in ["source_group_candidate_counts.svg", "lag_profile_plots.svg", "top_candidate_time_series.svg", "reverse_lag_comparison.svg", "data_coverage_calendar.svg", "missing_ratio_heatmap.svg", "combined_model_feature_importance.svg"]:
        (fig / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="120"><text x="20" y="45">{name}: MVP placeholder; CSV outputs contain plotted values.</text></svg>', encoding="utf-8")
