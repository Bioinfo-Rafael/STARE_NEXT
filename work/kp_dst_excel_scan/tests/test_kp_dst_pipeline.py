from __future__ import annotations

import unittest

from src.modeling.multiple_testing import benjamini_hochberg
from src.modeling.poisson import poisson_log_rate_ratio
from src.orchestration.run_all_pairs import _dedupe_records, _score_feature_target
from src.registry.dataset_registry import DatasetRecord


class KpDstPipelineTests(unittest.TestCase):
    def test_dedupes_excel_records_by_dataset_id(self) -> None:
        records = [
            DatasetRecord(excel_dataset_id="jma_catalog", name="地震月報"),
            DatasetRecord(excel_dataset_id="jma_catalog", name="地震月報 duplicate"),
            DatasetRecord(excel_dataset_id="gnss", name="GEONET"),
        ]
        deduped = _dedupe_records(records)
        self.assertEqual([r.excel_dataset_id for r in deduped], ["jma_catalog", "gnss"])

    def test_aggregate_target_type_overrides_registry_guess(self) -> None:
        feature_rows = []
        target_rows = []
        for day in range(1, 11):
            date = f"2020-01-{day:02d}"
            feature_rows.append(
                {
                    "date": date,
                    "kp_dst_feature_name": "kp_mean_daily",
                    "base_feature_name": "kp_mean_daily",
                    "feature_adjustment": "raw",
                    "value": float(day),
                }
            )
            target_rows.append(
                {
                    "date": date,
                    "target_name": "count",
                    "target_type": "event_catalog",
                    "spatial_unit": "national",
                    "region": "national",
                    "value": float(day % 3),
                }
            )
        record = DatasetRecord(excel_dataset_id="jma_catalog", name="地震月報", inferred_temporal_type="time_series")
        rows = _score_feature_target(feature_rows, target_rows, record, ["0D"], "national", min_samples=5)
        self.assertEqual(rows[0]["target_type"], "event_catalog")

    def test_poisson_rate_ratio_is_exponentiated_and_non_negative(self) -> None:
        coef, rate_ratio = poisson_log_rate_ratio([0, 0, 1, 1], [5, 6, 1, 2])
        self.assertIsNotNone(coef)
        self.assertIsNotNone(rate_ratio)
        self.assertGreaterEqual(rate_ratio, 0)

    def test_bh_adds_q_values(self) -> None:
        rows = [{"ols_p_value": 0.01}, {"ols_p_value": 0.04}, {"ols_p_value": ""}]
        out = benjamini_hochberg(rows)
        self.assertIn("fdr_q_value", out[0])
        self.assertIn("fdr_q_value", out[1])
        self.assertEqual(out[2]["fdr_q_value"], "")


if __name__ == "__main__":
    unittest.main()
