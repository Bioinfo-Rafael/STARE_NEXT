from __future__ import annotations

import math
from statistics import mean


def auc_score(xs: list[float], ys: list[float]) -> float | None:
    labels = [1 if y > 0 else 0 for y in ys]
    if len(set(labels)) < 2 or len(set(xs)) < 2:
        return None
    pairs = sorted(zip(xs, labels), key=lambda kv: kv[0])
    pos = sum(labels)
    neg = len(labels) - pos
    rank_sum = sum(i + 1 for i, (_, y) in enumerate(pairs) if y == 1)
    return (rank_sum - pos * (pos + 1) / 2) / (pos * neg)


def average_precision(xs: list[float], ys: list[float]) -> float | None:
    labels = [1 if y > 0 else 0 for y in ys]
    total_pos = sum(labels)
    if total_pos == 0:
        return None
    ordered = sorted(zip(xs, labels), key=lambda kv: kv[0], reverse=True)
    hits = 0
    precisions = []
    for i, (_, y) in enumerate(ordered, start=1):
        if y:
            hits += 1
            precisions.append(hits / i)
    return sum(precisions) / total_pos if precisions else None


def logistic_fit(xs: list[float], ys: list[float], steps: int = 100, lr: float = 0.05) -> tuple[float | None, float | None]:
    labels = [1.0 if y > 0 else 0.0 for y in ys]
    if len(set(labels)) < 2 or len(set(xs)) < 2:
        return None, None
    mx = mean(xs)
    scale = (sum((x - mx) ** 2 for x in xs) / max(len(xs) - 1, 1)) ** 0.5 or 1.0
    zs = [(x - mx) / scale for x in xs]
    b0 = 0.0
    b1 = 0.0
    for _ in range(steps):
        g0 = g1 = 0.0
        for z, y in zip(zs, labels):
            eta = max(min(b0 + b1 * z, 35), -35)
            p = 1 / (1 + math.exp(-eta))
            g0 += p - y
            g1 += (p - y) * z
        b0 -= lr * g0 / len(zs)
        b1 -= lr * g1 / len(zs)
    return b1, math.exp(max(min(b1, 35), -35))
