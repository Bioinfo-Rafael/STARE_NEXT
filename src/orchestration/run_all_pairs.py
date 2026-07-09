from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from src.adapters.base import SkipAdapter
from src.adapters.excel_dataset_adapter import ExcelDatasetAdapter
from src.features.external_features import create_external_adapter
from src.features.lag_features import pair_by_lag
from src.modeling.baselines import ols_slope, pearson, permutation_pvalue, spearman
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


def _score_pairs(external_rows: list[dict], target_rows: list[dict], lags: list[str], min_samples: int = 8) -> list[dict]:
    metrics: list[dict] = []
    external_groups = _by_feature(external_rows, "feature_name")
    target_groups = _by_feature(target_rows, "target_name")
    for external_feature, erows in external_groups.items():
        for target_name, trows in target_groups.items():
            for lag in lags:
                paired = pair_by_lag(erows, trows, lag)
                xs = [float(p["x"]) for p in paired]
                ys = [float(p["y"]) for p in paired]
                row: dict[str, Any] = {
                    "external_feature_name": external_feature,
                    "target_name": target_name,
                    "lag": lag,
                    "lag_direction": lag_direction(lag),
                    "n_samples": len(xs),
                    "train_period": f"{paired[0]['date']}..{paired[max(0, int(len(paired)*0.7)-1)]['date']}" if paired else "",
                    "test_period": f"{paired[int(len(paired)*0.7)]['date']}..{paired[-1]['date']}" if len(paired) >= 2 else "",
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
                auc = logistic_auc(xs, ys) if is_binary_target else None
                logcoef = logistic_coefficient(xs, ys) if is_binary_target else None
                row.update(
                    {
                        "model_type": "correlation+ols+logistic_probe",
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
                        "status": "ok",
                        "error_message": "",
                    }
                )
                metrics.append(row)
    return metrics


def _write_top_findings(output_dir: Path, rows: list[dict], failures_path: Path) -> None:
    ok = [r for r in rows if r.get("status") == "ok"]
    def score(row: dict) -> float:
        try:
            q = float(row.get("fdr_q_value") or 1)
        except Exception:
            q = 1
        try:
            c = abs(float(row.get("correlation") or 0))
        except Exception:
            c = 0
        lead_bonus = 0.1 if row.get("lag_direction") == "external_precedes_target" else 0
        return c + lead_bonus - q
    top = sorted(ok, key=score, reverse=True)[:10]
    lines = [
        "# Top Findings",
        "",
        "探索結果は仮説生成用です。地震予測を断定するものではありません。正のラグは外部信号が先、負のラグは地震側が先の反応方向です。",
        "",
    ]
    if not top:
        lines += ["有効サンプル数を満たす組み合わせはまだありません。期間を最近にするか、取得可能なExcel側カタログAdapterを追加してください。", ""]
    for i, row in enumerate(top, start=1):
        lines += [
            f"## {i}. {row.get('external_source_id')}:{row.get('external_feature_name')} × {row.get('excel_dataset_id')}:{row.get('target_name')}",
            f"- ラグ: {row.get('lag')} ({row.get('lag_direction')})",
            f"- モデル: {row.get('model_type')}",
            f"- 効果量: correlation={row.get('correlation')}, coefficient={row.get('coefficient')}",
            f"- p値/FDR: p={row.get('p_value')}, q={row.get('fdr_q_value')}",
            f"- 検証性能: AUC={row.get('AUC')}, rate_ratio={row.get('poisson_rate_ratio')}",
            "- 解釈: 多重検定込みの探索的シグナル。前兆方向か反応方向かを必ず確認してください。",
            "- 注意点: 公開APIの取得範囲、欠測、報道量・投稿量バイアス、地震後反応の混入に注意。",
            "- データ取得状況: status=ok",
            "",
        ]
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
            if probe_report.get("status") in {"skip", "rate_limited"}:
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
            external_rows = adapter.aggregate(fetched_rows)
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
                status_row["reason"] = "no target dataset fetched or no feature/target pairs were generated"
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
