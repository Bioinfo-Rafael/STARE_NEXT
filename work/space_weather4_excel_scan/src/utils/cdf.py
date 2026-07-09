from __future__ import annotations


def cdf_support_available() -> bool:
    try:
        import cdasws  # noqa: F401

        return True
    except Exception:
        return False
