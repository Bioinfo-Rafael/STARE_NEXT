from __future__ import annotations

import random

from src.modeling.correlations import pearson


def time_shuffle_correlation(xs: list[float], ys: list[float]) -> float | None:
    y = ys[:]
    random.Random(42).shuffle(y)
    return pearson(xs, y)


def block_shuffle_by_month_correlation(xs: list[float], ys: list[float], dates: list[str]) -> float | None:
    groups: dict[str, list[int]] = {}
    for i, date in enumerate(dates):
        groups.setdefault(date[:7], []).append(i)
    month_keys = list(groups)
    random.Random(43).shuffle(month_keys)
    shuffled = []
    for key in month_keys:
        shuffled.extend(ys[i] for i in groups[key])
    return pearson(xs[: len(shuffled)], shuffled)


def year_within_doy_shuffle_correlation(xs: list[float], ys: list[float], dates: list[str]) -> float | None:
    by_doy: dict[str, list[float]] = {}
    for y, date in zip(ys, dates):
        by_doy.setdefault(date[5:], []).append(y)
    shuffled = []
    rng = random.Random(44)
    for date in dates:
        vals = by_doy.get(date[5:], [0.0])
        shuffled.append(rng.choice(vals))
    return pearson(xs, shuffled)


def circular_shift_correlation(xs: list[float], ys: list[float]) -> float | None:
    if len(ys) < 3:
        return None
    shift = max(1, len(ys) // 3)
    shifted = ys[shift:] + ys[:shift]
    return pearson(xs, shifted)


def combined_negative_control(xs: list[float], ys: list[float], dates: list[str]) -> tuple[float | None, bool]:
    vals = [v for v in [time_shuffle_correlation(xs, ys), block_shuffle_by_month_correlation(xs, ys, dates), year_within_doy_shuffle_correlation(xs, ys, dates), circular_shift_correlation(xs, ys)] if v is not None]
    neg = max(vals, key=lambda v: abs(v)) if vals else None
    obs = pearson(xs, ys)
    return neg, bool(obs is not None and neg is not None and abs(obs) > abs(neg))
