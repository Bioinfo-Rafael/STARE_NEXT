from __future__ import annotations

from statistics import mean


def pseudo_poisson_effect(xs: list[float], ys: list[float]) -> float | None:
    if not xs or len(xs) != len(ys):
        return None
    mx = mean(xs)
    high = [y for x, y in zip(xs, ys) if x >= mx]
    low = [y for x, y in zip(xs, ys) if x < mx]
    if not high or not low:
        return None
    return (mean(high) + 1e-9) / (mean(low) + 1e-9)
