from __future__ import annotations

from datetime import datetime

from src.normalize.time import parse_lag


def pair_by_lag(external_rows: list[dict], target_rows: list[dict], lag: str) -> list[dict]:
    delta = parse_lag(lag)
    target_index: dict[tuple[str, str], float] = {}
    for row in target_rows:
        target_index[(str(row["date"]), str(row["target_name"]))] = float(row.get("value") or 0)
    paired: list[dict] = []
    for x in external_rows:
        try:
            target_date = (datetime.fromisoformat(str(x["date"])) + delta).date().isoformat()
        except ValueError:
            continue
        for (date, target_name), y in target_index.items():
            if date == target_date:
                paired.append(
                    {
                        "date": target_date,
                        "x_date": x["date"],
                        "external_feature_name": x["feature_name"],
                        "target_name": target_name,
                        "x": float(x.get("value") or 0),
                        "y": y,
                    }
                )
    return paired
