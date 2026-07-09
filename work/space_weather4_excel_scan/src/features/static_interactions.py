from __future__ import annotations


def static_interaction_placeholder(records: list) -> list[dict]:
    rows = []
    for record in records:
        if record.inferred_temporal_type == "static_spatial":
            rows.append(
                {
                    "excel_dataset_id": record.excel_dataset_id,
                    "excel_dataset_name": record.name,
                    "status": "static_only",
                    "reason": "Static spatial layer can be used for regional stratification/interactions after a region feature extractor is implemented.",
                }
            )
    return rows
