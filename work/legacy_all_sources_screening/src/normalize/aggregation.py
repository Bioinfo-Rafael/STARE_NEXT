from __future__ import annotations


def group_sum(rows: list[dict], key_fields: list[str], value_field: str = "value") -> list[dict]:
    acc: dict[tuple, float] = {}
    for row in rows:
        key = tuple(row.get(k, "") for k in key_fields)
        acc[key] = acc.get(key, 0.0) + float(row.get(value_field) or 0)
    out = []
    for key, value in sorted(acc.items()):
        rec = {field: key[i] for i, field in enumerate(key_fields)}
        rec[value_field] = value
        out.append(rec)
    return out
