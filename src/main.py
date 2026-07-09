from __future__ import annotations

import argparse
from pathlib import Path

from src.adapters import EXTERNAL_ADAPTERS
from src.adapters.excel_dataset_adapter import ExcelDatasetAdapter
from src.orchestration.cleanup import cleanup_tmp
from src.orchestration.run_all_pairs import run_all_pairs
from src.registry.parse_excel_registry import parse_excel_registry
from src.utils.env import load_dotenv
from src.utils.io import ensure_dir


DEFAULT_LAGS = "-14D,-7D,-3D,-1D,-12H,-6H,-1H,1H,6H,12H,1D,3D,7D,14D"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="STARE_NEXT public data exploratory screening pipeline")
    parser.add_argument("--excel", default="資料3_地震・測地データの一覧.xlsx")
    parser.add_argument("--start-date", default="2020-01-01")
    parser.add_argument("--end-date", default="2024-12-31")
    parser.add_argument("--spatial-unit", default="prefecture")
    parser.add_argument("--time-freq", default="1D")
    parser.add_argument("--lags", default=DEFAULT_LAGS)
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--external-source", default="all", help="one source id or all")
    parser.add_argument("--excel-dataset", default="auto", help="dataset_id, name, auto, or all")
    parser.add_argument("--probe-only", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--keep-raw", action="store_true")
    parser.add_argument("--cleanup-raw", default="true")
    parser.add_argument("--min-samples", type=int, default=8)
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir / "metadata" / "probe_reports")
    ensure_dir(output_dir / "figures")
    ensure_dir("tmp")
    records = parse_excel_registry(args.excel, output_dir)
    source_ids = list(EXTERNAL_ADAPTERS.keys()) if args.external_source == "all" else [args.external_source]
    if args.probe_only:
        excel_adapter = ExcelDatasetAdapter(records, output_dir=output_dir, keep_raw=args.keep_raw)
        excel_adapter.probe()
        for source_id in source_ids:
            adapter = EXTERNAL_ADAPTERS[source_id](output_dir=output_dir, keep_raw=args.keep_raw)
            adapter.probe()
            adapter.cleanup()
        return
    lags = [x.strip() for x in args.lags.split(",") if x.strip()]
    excel_dataset_id = "all" if args.excel_dataset == "all" else args.excel_dataset
    if excel_dataset_id == "auto":
        excel_dataset_id = "auto"
    run_all_pairs(
        records=records,
        external_source_ids=source_ids,
        excel_dataset_id=excel_dataset_id,
        start_date=args.start_date,
        end_date=args.end_date,
        lags=lags,
        output_dir=output_dir,
        keep_raw=args.keep_raw,
        force=args.force,
        min_samples=args.min_samples,
    )
    if str(args.cleanup_raw).lower() in {"true", "1", "yes"} and not args.keep_raw:
        cleanup_tmp("tmp")


if __name__ == "__main__":
    main()
