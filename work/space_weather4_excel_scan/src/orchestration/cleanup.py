from __future__ import annotations

from pathlib import Path

from src.utils.io import cleanup_dir


def cleanup_raw(raw_dir: str | Path, keep_raw: bool) -> None:
    if not keep_raw:
        cleanup_dir(raw_dir)
