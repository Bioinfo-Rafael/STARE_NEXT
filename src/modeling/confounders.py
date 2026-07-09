from __future__ import annotations

from datetime import datetime
from statistics import mean


FIXED_JP_HOLIDAYS = {
    "01-01",
    "02-11",
    "02-23",
    "04-29",
    "05-03",
    "05-04",
    "05-05",
    "08-11",
    "11-03",
    "11-23",
}


def is_weekend_or_holiday(date: str) -> int:
    dt = datetime.fromisoformat(date)
    if dt.weekday() >= 5:
        return 1
    if dt.strftime("%m-%d") in FIXED_JP_HOLIDAYS:
        return 1
    return 0


def residualize(values: list[float], dates: list[str]) -> list[float]:
    """Remove month, day-of-week, weekend/holiday, and linear year trend effects."""
    residuals = values[:]
    for _ in range(2):
        for key_fn in (
            lambda d: f"month:{datetime.fromisoformat(d).month}",
            lambda d: f"dow:{datetime.fromisoformat(d).weekday()}",
            lambda d: f"holiday:{is_weekend_or_holiday(d)}",
        ):
            groups: dict[str, list[int]] = {}
            for i, date in enumerate(dates):
                groups.setdefault(key_fn(date), []).append(i)
            for idxs in groups.values():
                m = mean(residuals[i] for i in idxs)
                for i in idxs:
                    residuals[i] -= m
        if len(residuals) >= 2:
            ts = [datetime.fromisoformat(d).toordinal() for d in dates]
            mt, mr = mean(ts), mean(residuals)
            denom = sum((t - mt) ** 2 for t in ts)
            if denom:
                slope = sum((t - mt) * (r - mr) for t, r in zip(ts, residuals)) / denom
                for i, t in enumerate(ts):
                    residuals[i] -= slope * (t - mt)
    return residuals


CONFOUNDERS_APPLIED = "month,day_of_week,weekend_or_holiday,year_trend"
