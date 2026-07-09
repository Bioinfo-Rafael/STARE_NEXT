from __future__ import annotations

import math
from statistics import mean


def poisson_log_rate_ratio(xs: list[float], ys: list[float]) -> tuple[float | None, float | None]:
    if len(xs) < 2 or len(set(xs)) < 2:
        return None, None
    mx = mean(xs)
    high = [y for x, y in zip(xs, ys) if x >= mx]
    low = [y for x, y in zip(xs, ys) if x < mx]
    if not high or not low:
        return None, None
    coef = math.log((mean(high) + 1e-9) / (mean(low) + 1e-9))
    return coef, math.exp(coef)
