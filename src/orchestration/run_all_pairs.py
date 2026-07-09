from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from src.adapters.base import SkipAdapter
from src.adapters.excel_dataset_adapter import ExcelDatasetAdapter
from src.features.anomaly import add_anomaly_features
from src.features.external_features import create_external_adapter
from src.features.lag_features import pair_by_lag
from src.modeling.baselines import ols_slope, pearson, permutation_pvalue, spearman
from src.modeling.confounders import CONFOUNDERS_APPLIED, residualize
from src.modeling.evaluation import benjamini_hochberg
from src.modeling.logistic import logistic_auc, logistic_coefficient
from src.modeling.poisson import pseudo_poisson_effect
from src.normalize.geo import JAPAN_BBOX
from src.normalize.time import lag_direction
from src.orchestration.logging import log_event
from src.registry.dataset_registry import DatasetRecord
from src.utils.io import append_jsonl, ensure_dir, read_jsonl_keys, write_csv, write_json, write_parquet_if_available

METRIC_FIELDS = [
    "external_source_id",
    "external_feature_name",
    "base_feature_name",
    "feature_adjustment",
    "excel_dataset_id",
    "target_name",
    "lag",
    "lag_direction",
    "n_samples",
    "model_type",
    "coefficient",
    "p_value",
    "fdr_q_value",
    "standardized_effect_size",
    "correlation",
    "spearman",
    "AUC",
    "average_precision",
    "RMSE",
    "MAE",
    "pseudo_R2",
    "poisson_rate_ratio",
    "negative_control_correlation",
    "negative_control_pass",
    "confounders",
    "train_period",
    "test_period",
    "status",
    "error_message",
]

SOURCE_STATUS_FIELDS = [
    "external_source_id",
    "probe_status",
    "fetch_status",
    "aggregate_status",
    "modeled_status",
    "n_fetch_rows",
    "n_aggregate_rows",
    "n_metric_rows",
    "n_ok_metric_rows",
    "reason",
]


def _by_feature(rows: list[dict], feature_key: str) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        out[str(row[feature_key])].append(row)
    return dict(out)


def _is_subdaily_lag(lag: str) -> bool:
    return lag.upper().endswith("H")


def _is_daily_rows(rows: list[dict]) -> bool:
    return all(len(str(row.get("date", ""))) == 10 for row in rows[:50])


def _is_daily_enabled_lag(lag: str) -> bool:
    return lag.lstrip("+-") in {"1D", "3D", "7D", "14D"}


def _negative_control_corr(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3:
        return None
    shifted = ys[len(ys) // 2 :] + ys[: len(ys) // 2]
    return pearson(xs, shifted)


def _split_period(paired: list[dict]) -> tuple[str, str]:
    paired = sorted(paired, key=lambda p: (p["date"], p["x_date"]))
    split = max(1, int(len(paired) * 0.7))
    if split >= len(paired):
        split = len(paired) - 1
    train_start = paired[0]["date"]
    train_end = paired[split - 1]["date"]
    test_start = paired[split]["date"]
    test_end = paired[-1]["date"]
    assert train_start <= train_end <= test_start <= test_end
    return f"{train_start}..{train_end}", f"{test_start}..{test_end}"


def _score_pairs(external_rows: list[dict], target_rows: list[dict], lags: list[str], min_samples: int = 8) -> list[dict]:
    metrics: list[dict] = []
    external_groups = _by_feature(external_rows, "feature_name")
    target_groups = _by_feature(target_rows, "target_name")
    daily_external = _is_daily_rows(external_rows)
    for external_feature, erows in external_groups.items():
        for target_name, trows in target_groups.items():
            for lag in lags:
                if daily_external and not _is_daily_enabled_lag(lag):
                    continue
                paired = pair_by_lag(erows, trows, lag)
                paired = sorted(paired, key=lambda p: (p["date"], p["x_date"]))
                xs_raw = [float(p["x"]) for p in paired]
                ys_raw = [float(p["y"]) for p in paired]
                dates = [str(p["date"]) for p in paired]
                xs = residualize(xs_raw, dates) if len(xs_raw) >= min_samples else xs_raw
                ys = residualize(ys_raw, dates) if len(ys_raw) >= min_samples else ys_raw
                train_period = test_period = ""
                if len(paired) >= 2:
                    train_period, test_period = _split_period(paired)
                feature_meta = erows[0] if erows else {}
                row: dict[str, Any] = {
                    "external_feature_name": external_feature,
                    "base_feature_name": feature_meta.get("base_feature_name", external_feature),
                    "feature_adjustment": feature_meta.get("feature_adjustment", "raw_count"),
                    "target_name": target_name,
                    "lag": lag,
                    "lag_direction": lag_direction(lag),
                    "n_samples": len(xs),
                    "train_period": train_period,
                    "test_period": test_period,
                    "confounders": CONFOUNDERS_APPLIED,
                }
                if len(xs) < min_samples:
                    row.update({"status": "insufficient_data", "error_message": f"n_samples<{min_samples}"})
                    metrics.append(row)
                    continue
                corr = pearson(xs, ys)
                sp = spearman(xs, ys)
                p = permutation_pvalue(xs, ys, rounds=50)
                slope = ols_slope(xs, ys)
                is_binary_target = str(target_name).endswith("_flag")
                auc = logistic_auc(xs, ys_raw) if is_binary_target else None
                logcoef = logistic_coefficient(xs, ys_raw) if is_binary_target else None
                neg_corr = _negative_control_corr(xs, ys)
                neg_pass = bool(corr is not None and neg_corr is not None and abs(corr) > abs(neg_corr))
                row.update(
                    {
                        "model_type": "calendar_adjusted_correlation+ols+logistic_probe",
                        "coefficient": logcoef if logcoef is not None else slope,
                        "p_value": p,
                        "standardized_effect_size": corr,
                        "correlation": corr,
                        "spearman": sp,
                        "AUC": auc,
                        "average_precision": "",
                        "RMSE": "",
                        "MAE": "",
                        "pseudo_R2": "",
                        "poisson_rate_ratio": pseudo_poisson_effect(xs, ys),
                        "negative_control_correlation": neg_corr,
                        "negative_control_pass": neg_pass,
                        "status": "ok",
                        "error_message": "",
                    }
                )
                metrics.append(row)
    return metrics


def _row_strength(row: dict) -> float:
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


def _rank(rows: list[dict], *, exclude_target: str | None = None) -> list[dict]:
    filtered = [r for r in rows if r.get("status") == "ok"]
    if exclude_target:
        filtered = [r for r in filtered if r.get("target_name") != exclude_target]
    by_target: dict[str, list[dict]] = defaultdict(list)
    for row in filtered:
        by_target[str(row.get("target_name", ""))].append(row)
    for target, target_rows in list(by_target.items()):
        by_target[target] = sorted(target_rows, key=lambda r: (_row_strength(r), str(r.get("fdr_q_value", ""))), reverse=True)
    ranked: list[dict] = []
    while len(ranked) < 10 and any(by_target.values()):
        for target in sorted(by_target):
            if by_target[target]:
                ranked.append(by_target[target].pop(0))
                if len(ranked) >= 10:
                    break
    return ranked


def _format_finding(row: dict, i: int) -> list[str]:
    return [
        f"## {i}. {row.get('external_source_id')}:{row.get('external_feature_name')} × {row.get('excel_dataset_id')}:{row.get('target_name')}",
        f"- ラグ: {row.get('lag')} ({row.get('lag_direction')})",
        f"- 特徴量調整: {row.get('feature_adjustment')}",
        f"- 交絡調整: {row.get('confounders')}",
        f"- モデル: {row.get('model_type')}",
        f"- 効果量: correlation={row.get('correlation')}, coefficient={row.get('coefficient')}",
        f"- p値/FDR: p={row.get('p_value')}, q={row.get('fdr_q_value')}",
        f"- 検証性能: AUC={row.get('AUC')}, rate_ratio={row.get('poisson_rate_ratio')}",
        f"- Negative control: corr={row.get('negative_control_correlation')}, pass={row.get('negative_control_pass')}",
        "- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。",
        "- 注意点: 季節性、曜日、休日、投稿量バイアス、地震後反応の混入に注意。",
        "- データ取得状況: status=ok",
        "",
    ]


def _write_top_findings(output_dir: Path, rows: list[dict], failures_path: Path) -> None:
    ok = [r for r in rows if r.get("status") == "ok"]
    lines = [
        "# Top Findings",
        "",
        "探索結果は仮説生成用です。地震予測を断定するものではありません。正のラグは外部信号が先、負のラグは地震側が先の反応方向です。",
        "",
    ]
    sections = [
        ("Raw Count Strong Signals", [r for r in ok if r.get("feature_adjustment") == "raw_count"]),
        ("Seasonal Adjusted Anomaly Strong Signals", [r for r in ok if r.get("feature_adjustment") != "raw_count"]),
        ("Signals Beating Negative Control", [r for r in ok if str(r.get("negative_control_pass")).lower() == "true"]),
        ("Precursor Direction Only", [r for r in ok if r.get("lag_direction") == "external_precedes_target"]),
        ("Post-Earthquake Reaction Stronger", [r for r in ok if r.get("lag_direction") == "target_precedes_external"]),
        ("Non-Max-Magnitude Ranking", [r for r in ok if r.get("target_name") != "max_magnitude"]),
    ]
    wiki_auc_rows = [
        r
        for r in ok
        if r.get("external_source_id") == "wikimedia"
        and r.get("target_name") in {"m4_flag", "m5_flag"}
        and r.get("AUC") not in {"", None}
        and any(term in str(r.get("base_feature_name", r.get("external_feature_name", ""))) for term in ["防災", "耳鳴り", "地震雲", "南海トラフ巨大地震"])
    ]
    sections.append(("Wikimedia M4/M5 AUC: 防災・耳鳴り・地震雲・南海トラフ巨大地震", wiki_auc_rows))

    if not ok:
        lines += ["有効サンプル数を満たす組み合わせはまだありません。期間を最近にするか、取得可能なExcel側カタログAdapterを追加してください。", ""]
    for title, section_rows in sections:
        lines += [f"# {title}", ""]
        ranked = _rank(section_rows)
        if not ranked:
            lines += ["該当する結果はありません。", ""]
            continue
        for i, row in enumerate(ranked, start=1):
            lines += _format_finding(row, i)
    lines += ["# Failed or Skipped Sources", ""]
    if failures_path.exists():
        failures = failures_path.read_text(encoding="utf-8").splitlines()[-50:]
        for item in failures:
            lines.append(f"- {item}")
    else:
        lines.append("- なし")
    (output_dir / "top_findings.md").write_text("\n".join(lines), encoding="utf-8")


def _write_svg_figures(output_dir: Path, rows: list[dict]) -> None:
    fig_dir = ensure_dir(output_dir / "figures")
    ok = [r for r in rows if r.get("status") == "ok"]
    status_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        status_counts[str(row.get("status", "unknown"))] += 1
    bars = "".join(
        f'<text x="20" y="{30+i*24}" font-size="12">{k}: {v}</text><rect x="180" y="{18+i*24}" width="{min(v, 500)}" height="14" fill="#277da1" />'
        for i, (k, v) in enumerate(sorted(status_counts.items()))
    )
    (fig_dir / "success_matrix.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="240">{bars}</svg>', encoding="utf-8")
    vals = []
    for r in ok[:80]:
        try:
            vals.append(abs(float(r.get("correlation") or 0)))
        except Exception:
            pass
    bars = "".join(f'<rect x="{20+i*8}" y="{180-v*150:.1f}" width="6" height="{v*150:.1f}" fill="#f9844a" />' for i, v in enumerate(vals))
    (fig_dir / "max_score_heatmap.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="220">{bars}<text x="20" y="205" font-size="12">absolute correlation samples</text></svg>', encoding="utf-8")
    (fig_dir / "pvalue_distribution.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="120"><text x="20" y="40" font-size="12">p-value/FDR distribution is available in per_pair_metrics.csv; install matplotlib for richer plots.</text></svg>',
        encoding="utf-8",
    )
    (fig_dir / "negative_control_comparison.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="120"><text x="20" y="40" font-size="12">Permutation p-values act as a lightweight time-shuffle negative control in this MVP.</text></svg>',
        encoding="utf-8",
    )
    (fig_dir / "lag_score_heatmap.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="120"><text x="20" y="40" font-size="12">Lag score heatmap placeholder; values are in per_pair_metrics.csv.</text></svg>',
        encoding="utf-8",
    )
    (fig_dir / "top_timeseries.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="120"><text x="20" y="40" font-size="12">Top time series plot requires a successful top finding and optional plotting dependencies.</text></svg>',
        encoding="utf-8",
    )


def run_all_pairs(
    records: list[DatasetRecord],
    external_source_ids: list[str],
    excel_dataset_id: str,
    start_date: str,
    end_date: str,
    lags: list[str],
    output_dir: str | Path,
    keep_raw: bool = False,
    force: bool = False,
    min_samples: int = 8,
) -> list[dict]:
    output_dir = Path(output_dir)
    ensure_dir(output_dir)
    failures_path = output_dir / "failures.jsonl"
    done = set() if force else read_jsonl_keys(output_dir / "run_log.jsonl", ["event", "external_source_id", "excel_dataset_id"])
    region = JAPAN_BBOX.copy()
    excel_adapter = ExcelDatasetAdapter(records, output_dir=output_dir, keep_raw=keep_raw)
    selected_records = records if excel_dataset_id == "all" else [r for r in records if r.dataset_id == excel_dataset_id or r.name == excel_dataset_id]
    if not selected_records:
        selected_records = [r for r in records if "気象庁" in r.provider and ("地震月報" in r.name or "カタログ" in r.name)][:1]
    if not selected_records:
        selected_records = [r for r in records if "気象庁" in r.provider and ("最近の地震活動" in r.name or "震源" in r.name)][:1]
    all_metrics: list[dict] = []
    source_status_rows: list[dict] = []
    target_cache: dict[str, list[dict]] = {}
    for external_source_id in external_source_ids:
        status_row: dict[str, Any] = {
            "external_source_id": external_source_id,
            "probe_status": "",
            "fetch_status": "",
            "aggregate_status": "",
            "modeled_status": "",
            "n_fetch_rows": 0,
            "n_aggregate_rows": 0,
            "n_metric_rows": 0,
            "n_ok_metric_rows": 0,
            "reason": "",
        }
        adapter = create_external_adapter(external_source_id, output_dir=output_dir, keep_raw=keep_raw)
        probe_report = adapter.probe()
        status_row["probe_status"] = "probe_ok" if probe_report.get("status") in {"ok", "available"} else str(probe_report.get("status") or "probe_error")
        if status_row["probe_status"] != "probe_ok":
            status_row["reason"] = str(probe_report.get("reason") or probe_report.get("note") or "probe did not return ok")
            if probe_report.get("status") in {"skip"}:
                status_row["fetch_status"] = "fetch_not_reached"
                status_row["aggregate_status"] = "aggregate_not_reached"
                status_row["modeled_status"] = "modeled_not_reached"
                source_status_rows.append(status_row)
                append_jsonl(failures_path, {"external_source_id": external_source_id, "status": probe_report.get("status"), "error_message": status_row["reason"]})
                adapter.cleanup()
                continue
        try:
            fetched_rows = adapter.fetch(start_date, end_date, region)
            status_row["fetch_status"] = "fetch_ok"
            status_row["n_fetch_rows"] = len(fetched_rows)
            external_rows = add_anomaly_features(adapter.aggregate(fetched_rows), start_date, end_date)
            status_row["aggregate_status"] = "aggregate_ok"
            status_row["n_aggregate_rows"] = len(external_rows)
        except SkipAdapter as exc:
            status_row["fetch_status"] = status_row["fetch_status"] or "fetch_skip"
            status_row["aggregate_status"] = "aggregate_not_reached"
            status_row["modeled_status"] = "modeled_not_reached"
            status_row["reason"] = str(exc)
            source_status_rows.append(status_row)
            append_jsonl(failures_path, {"external_source_id": external_source_id, "status": "skip", "error_message": str(exc)})
            adapter.cleanup()
            continue
        except Exception as exc:
            status_row["fetch_status"] = status_row["fetch_status"] or "fetch_error"
            status_row["aggregate_status"] = "aggregate_not_reached"
            status_row["modeled_status"] = "modeled_not_reached"
            status_row["reason"] = f"{type(exc).__name__}: {exc}"
            source_status_rows.append(status_row)
            append_jsonl(failures_path, {"external_source_id": external_source_id, "status": "error", "error_type": type(exc).__name__, "error_message": str(exc)})
            adapter.cleanup()
            continue
        source_metrics_before = len(all_metrics)
        for record in selected_records:
            key = ("pair_done", external_source_id, record.dataset_id)
            if key in done:
                continue
            excel_adapter.probe_dataset(record)
            try:
                if record.dataset_id not in target_cache:
                    target_cache[record.dataset_id] = excel_adapter.fetch_dataset(record, start_date, end_date, region)
                target_rows = target_cache[record.dataset_id]
            except SkipAdapter as exc:
                append_jsonl(failures_path, {"external_source_id": external_source_id, "excel_dataset_id": record.dataset_id, "status": "skip", "error_message": str(exc)})
                continue
            except Exception as exc:
                append_jsonl(failures_path, {"external_source_id": external_source_id, "excel_dataset_id": record.dataset_id, "status": "error", "error_type": type(exc).__name__, "error_message": str(exc)})
                continue
            metrics = _score_pairs(external_rows, target_rows, lags, min_samples=min_samples)
            for row in metrics:
                row["external_source_id"] = external_source_id
                row["excel_dataset_id"] = record.dataset_id
            all_metrics.extend(metrics)
            log_event(output_dir, "pair_done", external_source_id=external_source_id, excel_dataset_id=record.dataset_id, n_metrics=len(metrics))
        source_metrics = all_metrics[source_metrics_before:]
        status_row["n_metric_rows"] = len(source_metrics)
        status_row["n_ok_metric_rows"] = sum(1 for row in source_metrics if row.get("status") == "ok")
        if status_row["n_ok_metric_rows"]:
            status_row["modeled_status"] = "modeled_ok"
            status_row["reason"] = ""
        elif source_metrics:
            status_row["modeled_status"] = "modeled_insufficient_data"
            if not status_row["reason"]:
                max_samples = max((int(row.get("n_samples") or 0) for row in source_metrics), default=0)
                status_row["reason"] = (
                    "features reached modeling but no temporal overlap with target period"
                    if max_samples == 0
                    else "features reached modeling but no metric met min_samples or variation requirements"
                )
        else:
            status_row["modeled_status"] = "modeled_not_reached"
            if not status_row["reason"]:
                status_row["reason"] = (
                    "no external feature rows overlap requested target period"
                    if int(status_row.get("n_aggregate_rows") or 0) == 0
                    else "no target dataset fetched or no feature/target pairs were generated"
                )
        source_status_rows.append(status_row)
        adapter.cleanup()
    all_metrics = benjamini_hochberg(all_metrics)
    write_csv(output_dir / "per_pair_metrics.csv", all_metrics, METRIC_FIELDS)
    write_csv(output_dir / "summary.csv", all_metrics, METRIC_FIELDS)
    write_csv(output_dir / "source_pipeline_status.csv", source_status_rows, SOURCE_STATUS_FIELDS)
    write_parquet_if_available(output_dir / "per_pair_metrics.parquet", all_metrics)
    write_parquet_if_available(output_dir / "summary.parquet", all_metrics)
    _write_top_findings(output_dir, all_metrics, failures_path)
    _write_svg_figures(output_dir, all_metrics)
    excel_adapter.cleanup()
    write_json(
        output_dir / "metadata" / "run_summary.json",
        {
            "n_metric_rows": len(all_metrics),
            "external_sources": external_source_ids,
            "modeled_sources": sorted({row.get("external_source_id") for row in all_metrics}),
            "start_date": start_date,
            "end_date": end_date,
        },
    )
    return all_metrics
