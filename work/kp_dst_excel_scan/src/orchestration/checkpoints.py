from __future__ import annotations

from pathlib import Path


def checkpoint_done(path: str | Path, key: str) -> bool:
    p = Path(path)
    return p.exists() and key in set(p.read_text(encoding="utf-8").splitlines())


def mark_checkpoint(path: str | Path, key: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(key + "\n")
