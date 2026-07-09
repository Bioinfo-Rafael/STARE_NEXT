from __future__ import annotations

from datetime import datetime

from src.utils.dates import lag_direction, parse_lag


def pair_by_lag(feature_rows: list[dict], target_rows: list[dict], lag: str) -> list[dict]:
    delta = parse_lag(lag)
    target_index = {str(r["date"]): float(r.get("value") or 0) for r in target_rows}
    paired: list[dict] = []
    for row in sorted(feature_rows, key=lambda r: r["date"]):
        target_date = (datetime.fromisoformat(str(row["date"])) + delta).date().isoformat()
        if target_date in target_index:
            paired.append({"date": target_date, "feature_date": row["date"], "x": float(row["value"]), "y": target_index[target_date], "lag_direction": lag_direction(lag)})
    return paired
