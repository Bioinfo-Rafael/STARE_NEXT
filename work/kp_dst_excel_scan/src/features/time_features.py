from __future__ import annotations

from datetime import datetime
from functools import lru_cache


FIXED_HOLIDAYS = {"01-01", "02-11", "02-23", "04-29", "05-03", "05-04", "05-05", "08-11", "11-03", "11-23"}


def is_weekend_or_holiday(date: str) -> int:
    _month, dow, mmdd = date_parts(date)
    return int(dow >= 5 or mmdd in FIXED_HOLIDAYS)


@lru_cache(maxsize=20000)
def date_parts(date: str) -> tuple[int, int, str]:
    dt = datetime.fromisoformat(date)
    return dt.month, dt.weekday(), dt.strftime("%m-%d")


@lru_cache(maxsize=20000)
def ordinal(date: str) -> int:
    return datetime.fromisoformat(date).toordinal()


def residualize_controls(values: list[float], dates: list[str], previous_targets: dict[str, list[float]] | None = None) -> list[float]:
    residuals = values[:]
    for _ in range(1):
        for key_fn in (
            lambda d: f"month:{date_parts(d)[0]}",
            lambda d: f"dow:{date_parts(d)[1]}",
            lambda d: f"holiday:{is_weekend_or_holiday(d)}",
        ):
            groups: dict[str, list[int]] = {}
            for i, d in enumerate(dates):
                groups.setdefault(key_fn(d), []).append(i)
            for idxs in groups.values():
                m = sum(residuals[i] for i in idxs) / len(idxs)
                for i in idxs:
                    residuals[i] -= m
        ts = [ordinal(d) for d in dates]
        mt, mr = sum(ts) / len(ts), sum(residuals) / len(residuals)
        denom = sum((t - mt) ** 2 for t in ts)
        if denom:
            slope = sum((t - mt) * (r - mr) for t, r in zip(ts, residuals)) / denom
            for i, t in enumerate(ts):
                residuals[i] -= slope * (t - mt)
        if previous_targets:
            for lag_values in previous_targets.values():
                if len(lag_values) != len(residuals):
                    continue
                mx, mr = sum(lag_values) / len(lag_values), sum(residuals) / len(residuals)
                denom = sum((x - mx) ** 2 for x in lag_values)
                if denom:
                    coef = sum((x - mx) * (r - mr) for x, r in zip(lag_values, residuals)) / denom
                    for i, x in enumerate(lag_values):
                        residuals[i] -= coef * (x - mx)
    return residuals


def previous_target_vectors(target_by_date: dict[str, float], dates: list[str]) -> dict[str, list[float]]:
    from datetime import timedelta

    out = {"previous_target_1d": [], "previous_target_7d": [], "previous_target_30d": []}
    for date in dates:
        dt = datetime.fromisoformat(date)
        for d in [1, 7, 30]:
            out[f"previous_target_{d}d"].append(float(target_by_date.get((dt - timedelta(days=d)).date().isoformat(), 0.0)))
    return out
