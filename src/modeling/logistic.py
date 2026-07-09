from __future__ import annotations

import math
from statistics import mean


def logistic_auc(xs: list[float], ys: list[float]) -> float | None:
    labels = [1 if y > 0 else 0 for y in ys]
    if len(set(labels)) < 2:
        return None
    pairs = sorted(zip(xs, labels), key=lambda kv: kv[0])
    pos = sum(labels)
    neg = len(labels) - pos
    rank_sum = sum(i + 1 for i, (_, y) in enumerate(pairs) if y == 1)
    return (rank_sum - pos * (pos + 1) / 2) / (pos * neg)


def logistic_coefficient(xs: list[float], ys: list[float], steps: int = 300, lr: float = 0.05) -> float | None:
    labels = [1.0 if y > 0 else 0.0 for y in ys]
    if len(set(labels)) < 2:
        return None
    mx = mean(xs)
    scale = (sum((x - mx) ** 2 for x in xs) / max(len(xs) - 1, 1)) ** 0.5 or 1.0
    zs = [(x - mx) / scale for x in xs]
    b0 = 0.0
    b1 = 0.0
    for _ in range(steps):
        g0 = g1 = 0.0
        for z, y in zip(zs, labels):
            p = 1 / (1 + math.exp(-(b0 + b1 * z)))
            g0 += p - y
            g1 += (p - y) * z
        b0 -= lr * g0 / len(zs)
        b1 -= lr * g1 / len(zs)
    return b1
