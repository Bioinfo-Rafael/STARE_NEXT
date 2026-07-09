from __future__ import annotations

import re

from src.utils.http import get
from src.utils.io import write_json

GLOTEC_INDEX = "https://services.swpc.noaa.gov/products/glotec/"
GLOTEC_PRODUCT = "https://www.spaceweather.gov/products/glotec"


def probe_glotec(output_dir: str) -> dict:
    response, sample = get(GLOTEC_INDEX, timeout=30)
    names = re.findall(r'href="([^"]+)"', response.text if response else "")
    report = {
        "source": "glotec",
        "source_group": "glotec",
        "status": "ok" if response is not None and response.status_code == 200 else "error",
        "sample_http": sample.as_dict(),
        "guessed_format": "NOAA SWPC directory with NetCDF/JSON products",
        "available_links_sample": names[:40],
        "coverage_note": "Operational global GloTEC is public from 2025-present; 2020-2024 scans are marked insufficient_coverage unless an archive endpoint is configured.",
        "product_page": GLOTEC_PRODUCT,
    }
    write_json(f"{output_dir}/metadata/probe_reports/glotec_probe.json", report)
    return report


def fetch_glotec(start_date: str, end_date: str, output_dir: str) -> list[dict]:
    return []
