from __future__ import annotations

from statistics import mean


def ols_coef(xs: list[float], ys: list[float]) -> tuple[float | None, float | None]:
    if len(xs) < 2 or len(set(xs)) < 2:
        return None, None
    mx, my = mean(xs), mean(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    if not denom:
        return None, None
    coef = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom
    return coef, None
