from __future__ import annotations


def netcdf_support_available() -> bool:
    try:
        import netCDF4  # noqa: F401
        import xarray  # noqa: F401

        return True
    except Exception:
        return False
