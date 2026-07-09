from __future__ import annotations

from datetime import datetime, timedelta
import re


def date_range(start: str, end: str) -> list[str]:
    day = datetime.fromisoformat(start)
    last = datetime.fromisoformat(end)
    out: list[str] = []
    while day <= last:
        out.append(day.date().isoformat())
        day += timedelta(days=1)
    return out


def parse_lag(lag: str) -> timedelta:
    m = re.fullmatch(r"\s*([+-]?\d+)\s*([DH])\s*", lag, flags=re.I)
    if not m:
        raise ValueError(f"Unsupported lag: {lag}")
    n = int(m.group(1))
    return timedelta(days=n) if m.group(2).upper() == "D" else timedelta(hours=n)


def lag_direction(lag: str) -> str:
    seconds = parse_lag(lag).total_seconds()
    if seconds > 0:
        return "external_precedes_target"
    if seconds < 0:
        return "target_precedes_external"
    return "same_day"


def month_iter(start: str, end: str) -> list[str]:
    y, m = int(start[:4]), int(start[5:7])
    ey, em = int(end[:4]), int(end[5:7])
    out: list[str] = []
    while (y, m) <= (ey, em):
        out.append(f"{y:04d}{m:02d}")
        m += 1
        if m == 13:
            y += 1
            m = 1
    return out


def year_iter(start: str, end: str) -> list[int]:
    return list(range(int(start[:4]), int(end[:4]) + 1))
