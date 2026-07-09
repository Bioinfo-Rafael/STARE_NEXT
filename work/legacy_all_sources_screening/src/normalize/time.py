from __future__ import annotations

from datetime import timedelta
import re


def parse_lag(value: str) -> timedelta:
    m = re.fullmatch(r"\s*([+-]?\d+)\s*([DH])\s*", value, flags=re.I)
    if not m:
        raise ValueError(f"Unsupported lag format: {value}")
    n = int(m.group(1))
    unit = m.group(2).upper()
    return timedelta(days=n) if unit == "D" else timedelta(hours=n)


def lag_direction(value: str) -> str:
    td = parse_lag(value)
    if td.total_seconds() > 0:
        return "external_precedes_target"
    if td.total_seconds() < 0:
        return "target_precedes_external"
    return "same_time"
