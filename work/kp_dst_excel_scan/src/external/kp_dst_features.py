from __future__ import annotations

from collections import defaultdict
from datetime import datetime
import math
from statistics import mean, pstdev

from src.utils.dates import date_range


def _std(values: list[float]) -> float:
    return pstdev(values) if len(values) > 1 else 0.0


def _roll(values: list[float], i: int, window: int, fn) -> float:
    seq = values[max(0, i - window + 1) : i + 1]
    return fn(seq) if seq else 0.0


def _anomalies(prefix: str, dates: list[str], values: list[float]) -> dict[str, list[float]]:
    doy: dict[str, list[float]] = defaultdict(list)
    month: dict[str, list[float]] = defaultdict(list)
    for date, value in zip(dates, values):
        dt = datetime.fromisoformat(date)
        doy[dt.strftime("%m-%d")].append(value)
        month[dt.strftime("%m")].append(value)
    doy_mean = {k: mean(v) for k, v in doy.items()}
    month_mean = {k: mean(v) for k, v in month.items()}
    out = {
        f"{prefix}_doy_anomaly": [],
        f"{prefix}_month_residual": [],
        f"{prefix}_ma7_anomaly": [],
        f"{prefix}_ma30_anomaly": [],
    }
    prev_log = None
    if prefix == "kp":
        out["kp_log1p_diff"] = []
    for i, (date, value) in enumerate(zip(dates, values)):
        dt = datetime.fromisoformat(date)
        out[f"{prefix}_doy_anomaly"].append(value - doy_mean[dt.strftime("%m-%d")])
        out[f"{prefix}_month_residual"].append(value - month_mean[dt.strftime("%m")])
        out[f"{prefix}_ma7_anomaly"].append(value - _roll(values, i, 7, mean))
        out[f"{prefix}_ma30_anomaly"].append(value - _roll(values, i, 30, mean))
        if prefix == "kp":
            lv = math.log1p(max(value, 0.0))
            out["kp_log1p_diff"].append(0.0 if prev_log is None else lv - prev_log)
            prev_log = lv
    return out


def build_kp_dst_features(kp_rows: list[dict], dst_rows: list[dict], start_date: str, end_date: str) -> list[dict]:
    dates = date_range(start_date, end_date)
    kp_by_date: dict[str, list[float]] = defaultdict(list)
    for row in kp_rows:
        kp_by_date[row["date"]].append(float(row["kp"]))
    dst_by_date: dict[str, list[float]] = defaultdict(list)
    for row in dst_rows:
        dst_by_date[row["date"]].append(float(row["dst"]))

    series: dict[str, list[float]] = defaultdict(list)
    for date in dates:
        kp = kp_by_date.get(date, [])
        dst = dst_by_date.get(date, [])
        if kp:
            series["kp_mean_daily"].append(mean(kp))
            series["kp_max_daily"].append(max(kp))
            series["kp_min_daily"].append(min(kp))
            series["kp_std_daily"].append(_std(kp))
            series["kp_sum_daily"].append(sum(kp))
            series["kp_range_daily"].append(max(kp) - min(kp))
            series["storm_flag_kp_ge_4"].append(1.0 if max(kp) >= 4 else 0.0)
            series["storm_flag_kp_ge_5"].append(1.0 if max(kp) >= 5 else 0.0)
            series["storm_flag_kp_ge_6"].append(1.0 if max(kp) >= 6 else 0.0)
        else:
            for key in ["kp_mean_daily", "kp_max_daily", "kp_min_daily", "kp_std_daily", "kp_sum_daily", "kp_range_daily", "storm_flag_kp_ge_4", "storm_flag_kp_ge_5", "storm_flag_kp_ge_6"]:
                series[key].append(0.0)
        if dst:
            series["dst_mean_daily"].append(mean(dst))
            series["dst_min_daily"].append(min(dst))
            series["dst_max_daily"].append(max(dst))
            series["dst_std_daily"].append(_std(dst))
            series["dst_range_daily"].append(max(dst) - min(dst))
            series["dst_negative_peak_abs"].append(abs(min(dst)))
            series["storm_flag_dst_le_minus30"].append(1.0 if min(dst) <= -30 else 0.0)
            series["storm_flag_dst_le_minus50"].append(1.0 if min(dst) <= -50 else 0.0)
            series["storm_flag_dst_le_minus100"].append(1.0 if min(dst) <= -100 else 0.0)
        else:
            for key in ["dst_mean_daily", "dst_min_daily", "dst_max_daily", "dst_std_daily", "dst_range_daily", "dst_negative_peak_abs", "storm_flag_dst_le_minus30", "storm_flag_dst_le_minus50", "storm_flag_dst_le_minus100"]:
                series[key].append(0.0)

    kp_mean = series["kp_mean_daily"]
    kp_max = series["kp_max_daily"]
    dst_mean = series["dst_mean_daily"]
    dst_min = series["dst_min_daily"]
    for i in range(len(dates)):
        series["kp_diff_1d"].append(kp_mean[i] - (kp_mean[i - 1] if i >= 1 else kp_mean[i]))
        series["kp_diff_3d"].append(kp_mean[i] - (kp_mean[i - 3] if i >= 3 else kp_mean[i]))
        for w in [3, 7, 14]:
            series[f"kp_rolling_mean_{w}d"].append(_roll(kp_mean, i, w, mean))
            series[f"kp_rolling_max_{w}d"].append(_roll(kp_max, i, w, max))
        series["dst_diff_1d"].append(dst_mean[i] - (dst_mean[i - 1] if i >= 1 else dst_mean[i]))
        series["dst_diff_3d"].append(dst_mean[i] - (dst_mean[i - 3] if i >= 3 else dst_mean[i]))
        for w in [3, 7]:
            series[f"dst_rolling_mean_{w}d"].append(_roll(dst_mean, i, w, mean))
            series[f"dst_rolling_min_{w}d"].append(_roll(dst_min, i, w, min))
        series["kp_dst_interaction"].append(kp_mean[i] * abs(dst_mean[i]))
        series["storm_joint_flag"].append(1.0 if series["storm_flag_kp_ge_5"][i] and series["storm_flag_dst_le_minus50"][i] else 0.0)
        series["kp_minus_dst_scaled"].append(kp_mean[i] - abs(dst_mean[i]) / 10.0)
        series["geomagnetic_activity_score"].append((kp_mean[i] / 9.0 + abs(dst_min[i]) / 100.0) / 2.0)
        series["kp_dst_pc1_proxy"].append((kp_mean[i] / 9.0 + abs(dst_mean[i]) / 100.0) / 2.0)

    for key, vals in _anomalies("kp", dates, kp_mean).items():
        series[key] = vals
    for key, vals in _anomalies("dst", dates, dst_mean).items():
        series[key] = vals

    rows: list[dict] = []
    raw_features = {"kp_mean_daily", "kp_max_daily", "kp_min_daily", "kp_std_daily", "kp_sum_daily", "kp_range_daily", "dst_mean_daily", "dst_min_daily", "dst_max_daily", "dst_std_daily", "dst_range_daily"}
    for feature, values in series.items():
        adjustment = "raw" if feature in raw_features or feature.startswith("storm_") else "derived"
        if "anomaly" in feature or "residual" in feature:
            adjustment = "seasonal_adjusted"
        for date, value in zip(dates, values):
            rows.append({"date": date, "kp_dst_feature_name": feature, "base_feature_name": feature.split("_doy_")[0].split("_month_")[0].split("_ma")[0], "feature_adjustment": adjustment, "value": float(value)})
    return rows
