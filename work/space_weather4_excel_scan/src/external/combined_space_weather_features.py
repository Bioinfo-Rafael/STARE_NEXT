from __future__ import annotations

from collections import defaultdict
from statistics import mean, pstdev


def _zscore_by_feature(rows: list[dict]) -> dict[tuple[str, str], float]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        grouped[row["external_feature_name"]].append(float(row["value"]))
    stats = {}
    for feature, values in grouped.items():
        mu = mean(values) if values else 0.0
        sd = pstdev(values) if len(values) > 1 else 1.0
        stats[feature] = (mu, sd or 1.0)
    return {(row["external_feature_name"], row["date"]): (float(row["value"]) - stats[row["external_feature_name"]][0]) / stats[row["external_feature_name"]][1] for row in rows}


def build_combined_features(feature_rows: list[dict]) -> list[dict]:
    wanted = {
        "kp_mean_daily",
        "dst_negative_peak_abs",
        "geomagnetic_activity_score",
        "IMF_B_total_daily_mean",
        "IMF_Bz_daily_abs_max",
        "solar_wind_speed_daily_mean",
        "flow_pressure_daily_mean",
        "F10_7_daily_mean",
    }
    base_rows = [r for r in feature_rows if r.get("external_feature_name") in wanted]
    if not base_rows:
        return []
    z = _zscore_by_feature(base_rows)
    by_date: dict[str, list[float]] = defaultdict(list)
    by_group_date: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in base_rows:
        value = z[(row["external_feature_name"], row["date"])]
        by_date[row["date"]].append(value)
        by_group_date[(row.get("external_source_group", ""), row["date"])].append(value)
    out = []
    for date, vals in sorted(by_date.items()):
        kp_dst = mean(by_group_date.get(("kp_dst", date), [0.0]))
        omni = mean(by_group_date.get(("omni", date), [0.0]))
        features = {
            "space_weather_activity_pc1_proxy": mean(vals),
            "solarwind_minus_geomag_proxy": omni - kp_dst,
            "combined_abs_activity_score": mean(abs(v) for v in vals),
        }
        for name, value in features.items():
            out.append(
                {
                    "date": date,
                    "external_source_group": "combined",
                    "external_feature_name": name,
                    "base_feature_name": name,
                    "feature_adjustment": "derived",
                    "value": float(value),
                    "missing_ratio": 0.0,
                    "valid_count": len(vals),
                }
            )
    return out
