from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Mapping, Sequence


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_json(path: str | Path, payload: object) -> None:
    p = Path(path)
    ensure_dir(p.parent)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def append_jsonl(path: str | Path, payload: Mapping[str, object]) -> None:
    p = Path(path)
    ensure_dir(p.parent)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")


def read_jsonl_keys(path: str | Path, key_fields: Sequence[str]) -> set[tuple[str, ...]]:
    p = Path(path)
    if not p.exists():
        return set()
    out: set[tuple[str, ...]] = set()
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        out.add(tuple(str(obj.get(k, "")) for k in key_fields))
    return out


def write_csv(path: str | Path, rows: Iterable[Mapping[str, object]], fieldnames: Sequence[str] | None = None) -> None:
    rows = list(rows)
    if fieldnames is None:
        keys: list[str] = []
        for row in rows:
            for key in row.keys():
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    p = Path(path)
    ensure_dir(p.parent)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def write_parquet_if_available(path: str | Path, rows: Iterable[Mapping[str, object]]) -> bool:
    rows = list(rows)
    if not rows:
        return False
    try:
        import pandas as pd  # type: ignore
    except Exception:
        return False
    p = Path(path)
    ensure_dir(p.parent)
    pd.DataFrame(rows).to_parquet(p, index=False)
    return True
