from __future__ import annotations

from collections import defaultdict
from datetime import datetime
import math
from statistics import mean, pstdev

from src.utils.dates import date_range

OMNI_VARIABLES = [
    "IMF_B_total",
    "IMF_Bz",
    "proton_density",
    "solar_wind_speed",
    "flow_pressure",
    "electric_field",
    "plasma_beta",
    "alfven_mach_number",
    "sunspot_number",
    "F10_7",
    "omni_dst",
    "AE_index",
    "AL_index",
    "AU_index",
]


def _std(values: list[float]) -> float:
    return pstdev(values) if len(values) > 1 else 0.0


def _roll(values: list[float], i: int, window: int, fn) -> float:
    seq = values[max(0, i - window + 1) : i + 1]
    return fn(seq) if seq else 0.0


def _anomaly_rows(prefix: str, dates: list[str], values: list[float]) -> dict[str, list[float]]:
    doy: dict[str, list[float]] = defaultdict(list)
    month: dict[str, list[float]] = defaultdict(list)
    for date, value in zip(dates, values):
        dt = datetime.fromisoformat(date)
        doy[dt.strftime("%m-%d")].append(value)
        month[dt.strftime("%m")].append(value)
    doy_mean = {k: mean(v) for k, v in doy.items()}
    month_mean = {k: mean(v) for k, v in month.items()}
    out = {f"{prefix}_ma7_anomaly": [], f"{prefix}_ma30_anomaly": [], f"{prefix}_doy_anomaly": [], f"{prefix}_month_residual": []}
    for i, (date, value) in enumerate(zip(dates, values)):
        dt = datetime.fromisoformat(date)
        out[f"{prefix}_ma7_anomaly"].append(value - _roll(values, i, 7, mean))
        out[f"{prefix}_ma30_anomaly"].append(value - _roll(values, i, 30, mean))
        out[f"{prefix}_doy_anomaly"].append(value - doy_mean[dt.strftime("%m-%d")])
        out[f"{prefix}_month_residual"].append(value - month_mean[dt.strftime("%m")])
    return out


def build_omni_features(omni_rows: list[dict], start_date: str, end_date: str) -> list[dict]:
    dates = date_range(start_date, end_date)
    by_date: dict[str, list[dict]] = defaultdict(list)
    for row in omni_rows:
        by_date[row["date"]].append(row)

    series: dict[str, list[float]] = defaultdict(list)
    missing: dict[str, list[float]] = defaultdict(list)
    valid: dict[str, list[int]] = defaultdict(list)
    for date in dates:
        rows = by_date.get(date, [])
        for var in OMNI_VARIABLES:
            vals = [float(r[var]) for r in rows if r.get(var) is not None]
            denom = max(len(rows), 1)
            missing_ratio = 1.0 - len(vals) / denom if rows else 1.0
            valid_count = len(vals)
            if vals:
                series[f"{var}_daily_mean"].append(mean(vals))
                series[f"{var}_daily_max"].append(max(vals))
                series[f"{var}_daily_min"].append(min(vals))
                series[f"{var}_daily_std"].append(_std(vals))
                series[f"{var}_daily_range"].append(max(vals) - min(vals))
                series[f"{var}_daily_abs_max"].append(max(abs(v) for v in vals))
            else:
                for suffix in ["daily_mean", "daily_max", "daily_min", "daily_std", "daily_range", "daily_abs_max"]:
                    series[f"{var}_{suffix}"].append(0.0)
            missing[var].append(missing_ratio)
            valid[var].append(valid_count)

    for var in OMNI_VARIABLES:
        base = series[f"{var}_daily_mean"]
        daily_max = series[f"{var}_daily_max"]
        for i, value in enumerate(base):
            series[f"{var}_diff_1d"].append(value - (base[i - 1] if i >= 1 else value))
            series[f"{var}_diff_3d"].append(value - (base[i - 3] if i >= 3 else value))
            for w in [3, 7, 14]:
                series[f"{var}_rolling_mean_{w}d"].append(_roll(base, i, w, mean))
            for w in [3, 7]:
                series[f"{var}_rolling_max_{w}d"].append(_roll(daily_max, i, w, max))
            series[f"{var}_missing_ratio"].append(missing[var][i])
            series[f"{var}_valid_count"].append(float(valid[var][i]))
        for key, vals in _anomaly_rows(var, dates, base).items():
            series[key] = vals

    bz_min = series["IMF_Bz_daily_min"]
    bz_mean = series["IMF_Bz_daily_mean"]
    speed_max = series["solar_wind_speed_daily_max"]
    pressure_mean = series["flow_pressure_daily_mean"]
    for i, date in enumerate(dates):
        day_rows = by_date.get(date, [])
        bz_vals = [float(r["IMF_Bz"]) for r in day_rows if r.get("IMF_Bz") is not None]
        series["bz_min_daily"].append(bz_min[i])
        series["bz_negative_sum"].append(sum(abs(v) for v in bz_vals if v < 0))
        series["bz_negative_hours"].append(sum(1 for v in bz_vals if v < 0))
        series["bz_southward_flag"].append(1.0 if bz_min[i] <= -5 else 0.0)
        series["pressure_jump_1d"].append(pressure_mean[i] - (pressure_mean[i - 1] if i >= 1 else pressure_mean[i]))
        series["speed_ge_500"].append(1.0 if speed_max[i] >= 500 else 0.0)
        series["speed_ge_600"].append(1.0 if speed_max[i] >= 600 else 0.0)
        series["speed_ge_700"].append(1.0 if speed_max[i] >= 700 else 0.0)
        series["IMF_clock_angle_proxy"].append(math.atan2(abs(bz_mean[i]), max(series["IMF_B_total_daily_mean"][i], 1e-9)))

    rows: list[dict] = []
    for feature, values in series.items():
        adjustment = "raw" if any(feature.endswith(s) for s in ["daily_mean", "daily_max", "daily_min", "daily_std", "daily_range", "daily_abs_max"]) else "derived"
        if "anomaly" in feature or "residual" in feature:
            adjustment = "seasonal_adjusted"
        if feature.endswith("missing_ratio") or feature.endswith("valid_count"):
            adjustment = "quality"
        base_feature = feature
        for marker in ["_daily_", "_diff_", "_rolling_", "_ma7_", "_ma30_", "_doy_", "_month_"]:
            if marker in base_feature:
                base_feature = base_feature.split(marker)[0]
                break
        for date, value in zip(dates, values):
            rows.append(
                {
                    "date": date,
                    "external_source_group": "omni",
                    "external_feature_name": feature,
                    "base_feature_name": base_feature,
                    "feature_adjustment": adjustment,
                    "value": float(value),
                    "missing_ratio": 0.0,
                    "valid_count": 1,
                }
            )
    return rows
