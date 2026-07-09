from __future__ import annotations


def lag_asymmetry_rows(metrics: list[dict]) -> list[dict]:
    rows = []
    groups: dict[tuple, list[dict]] = {}
    for row in metrics:
        key = (row.get("external_source_group"), row.get("external_feature_name"), row.get("excel_dataset_id"), row.get("target_name"))
        groups.setdefault(key, []).append(row)
    for key, vals in groups.items():
        pre = max((abs(float(v.get("correlation") or 0)) for v in vals if v.get("lag_direction") == "external_precedes_target"), default=0.0)
        rev = max((abs(float(v.get("correlation") or 0)) for v in vals if v.get("lag_direction") == "target_precedes_external"), default=0.0)
        rows.append(
            {
                "external_source_group": key[0],
                "external_feature_name": key[1],
                "excel_dataset_id": key[2],
                "target_name": key[3],
                "best_precursor_score": pre,
                "best_reverse_lag_score": rev,
                "precursor_minus_reverse_score": pre - rev,
            }
        )
    return rows
