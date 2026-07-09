from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
import math

FeatureRows = list[dict]


def _date_range(start: str, end: str) -> list[str]:
    day = datetime.fromisoformat(start)
    last = datetime.fromisoformat(end)
    out: list[str] = []
    while day <= last:
        out.append(day.date().isoformat())
        day += timedelta(days=1)
    return out


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def add_anomaly_features(rows: FeatureRows, start_date: str, end_date: str) -> FeatureRows:
    """Expand raw daily feature rows into raw and seasonally adjusted anomaly variants."""
    by_feature: dict[str, dict[str, float]] = defaultdict(dict)
    source_by_feature: dict[str, str] = {}
    for row in rows:
        feature = str(row["feature_name"])
        source_by_feature[feature] = str(row.get("source_id", ""))
        by_feature[feature][str(row["date"])] = float(row.get("value") or 0)

    dates = _date_range(start_date, end_date)
    date_set = set(dates)
    expanded: FeatureRows = []
    for feature, values_by_date in by_feature.items():
        if not (set(values_by_date) & date_set):
            continue
        values = [values_by_date.get(d, 0.0) for d in dates]
        source_id = source_by_feature.get(feature, "")
        doy_values: dict[str, list[float]] = defaultdict(list)
        month_values: dict[str, list[float]] = defaultdict(list)
        for date, value in zip(dates, values):
            dt = datetime.fromisoformat(date)
            doy_values[dt.strftime("%m-%d")].append(value)
            month_values[dt.strftime("%m")].append(value)
        doy_mean = {k: _mean(v) for k, v in doy_values.items()}
        month_mean = {k: _mean(v) for k, v in month_values.items()}

        prev_log = None
        for i, (date, value) in enumerate(zip(dates, values)):
            dt = datetime.fromisoformat(date)
            ma7 = _mean(values[max(0, i - 6) : i + 1])
            ma30 = _mean(values[max(0, i - 29) : i + 1])
            log_value = math.log1p(max(value, 0.0))
            log_diff = 0.0 if prev_log is None else log_value - prev_log
            prev_log = log_value
            variants = {
                "raw_count": value,
                "ma7_anomaly": value - ma7,
                "ma30_anomaly": value - ma30,
                "doy_anomaly": value - doy_mean[dt.strftime("%m-%d")],
                "month_residual": value - month_mean[dt.strftime("%m")],
                "log1p_diff": log_diff,
            }
            for adjustment, adjusted_value in variants.items():
                expanded.append(
                    {
                        "date": date,
                        "source_id": source_id,
                        "feature_name": f"{feature}__{adjustment}",
                        "base_feature_name": feature,
                        "feature_adjustment": adjustment,
                        "value": adjusted_value,
                        "raw_value": value,
                    }
                )
    return expanded
