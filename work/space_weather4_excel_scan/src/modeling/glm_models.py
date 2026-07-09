from __future__ import annotations

import math


def ols_coef(xs: list[float], ys: list[float]) -> tuple[float | None, float | None]:
    if len(xs) < 2 or len(set(xs)) < 2:
        return None, None
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    if not denom:
        return None, None
    coef = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom
    yhat = [my + coef * (x - mx) for x in xs]
    rss = sum((y - yh) ** 2 for y, yh in zip(ys, yhat))
    if len(xs) <= 2:
        return coef, None
    sigma2 = rss / (len(xs) - 2)
    se = math.sqrt(max(sigma2, 0.0) / denom) if denom else 0.0
    if se <= 0:
        return coef, 0.0
    t = abs(coef / se)
    p_approx = math.erfc(t / math.sqrt(2))
    return coef, max(0.0, min(1.0, p_approx))
