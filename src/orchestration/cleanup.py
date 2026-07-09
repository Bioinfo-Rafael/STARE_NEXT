from __future__ import annotations

import shutil
from pathlib import Path


def cleanup_tmp(tmp_dir: str | Path = "tmp") -> None:
    p = Path(tmp_dir)
    if p.exists():
        for child in p.iterdir():
            if child.is_dir():
                shutil.rmtree(child, ignore_errors=True)
            else:
                child.unlink(missing_ok=True)
