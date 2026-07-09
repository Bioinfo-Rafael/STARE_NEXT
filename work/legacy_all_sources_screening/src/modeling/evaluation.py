from __future__ import annotations


def benjamini_hochberg(rows: list[dict], p_field: str = "p_value", out_field: str = "fdr_q_value") -> list[dict]:
    indexed = []
    for i, row in enumerate(rows):
        try:
            p = float(row.get(p_field))
        except Exception:
            continue
        if p == p and 0 <= p <= 1:
            indexed.append((i, p))
    m = len(indexed)
    if not m:
        for row in rows:
            row[out_field] = ""
        return rows
    prev = 1.0
    for rank, (i, p) in enumerate(sorted(indexed, key=lambda x: x[1], reverse=True), start=1):
        original_rank = m - rank + 1
        q = min(prev, p * m / original_rank)
        prev = q
        rows[i][out_field] = q
    for row in rows:
        row.setdefault(out_field, "")
    return rows
