from __future__ import annotations

import csv
from pathlib import Path
import unittest


class SummarySourceTests(unittest.TestCase):
    def test_summary_contains_non_wikimedia_source(self) -> None:
        path = Path("results/summary.csv")
        self.assertTrue(path.exists(), "Run the pipeline before checking summary sources")
        with path.open(newline="", encoding="utf-8") as f:
            sources = {row["external_source_id"] for row in csv.DictReader(f) if row.get("external_source_id")}
        self.assertTrue(sources - {"wikimedia"}, f"summary.csv only contains wikimedia: {sorted(sources)}")

    def test_source_pipeline_status_has_stage_columns(self) -> None:
        path = Path("results/source_pipeline_status.csv")
        self.assertTrue(path.exists(), "source_pipeline_status.csv was not written")
        with path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertTrue(rows, "source_pipeline_status.csv is empty")
        required = {"external_source_id", "probe_status", "fetch_status", "aggregate_status", "modeled_status", "reason"}
        self.assertLessEqual(required, set(rows[0]))

    def test_summary_has_anomaly_and_no_subdaily_daily_lags(self) -> None:
        path = Path("results/summary.csv")
        with path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        adjustments = {row.get("feature_adjustment") for row in rows}
        self.assertIn("raw_count", adjustments)
        self.assertTrue({"ma7_anomaly", "ma30_anomaly", "doy_anomaly", "month_residual", "log1p_diff"} & adjustments)
        lags = {row["lag"] for row in rows if row.get("status") == "ok"}
        self.assertFalse({lag for lag in lags if lag.endswith("H")}, f"sub-daily lags leaked into daily summary: {lags}")

    def test_train_test_periods_are_sorted(self) -> None:
        path = Path("results/summary.csv")
        with path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if not row.get("train_period") or not row.get("test_period"):
                    continue
                train_start, train_end = row["train_period"].split("..")
                test_start, test_end = row["test_period"].split("..")
                self.assertLessEqual(train_start, train_end)
                self.assertLessEqual(train_end, test_start)
                self.assertLessEqual(test_start, test_end)


if __name__ == "__main__":
    unittest.main()
