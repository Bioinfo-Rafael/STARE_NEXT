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


if __name__ == "__main__":
    unittest.main()
