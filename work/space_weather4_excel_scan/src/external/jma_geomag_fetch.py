from __future__ import annotations

import re

from src.utils.http import get
from src.utils.io import write_json

JMA_GEOMAG_METADATA = "https://www.kakioka-jma.go.jp/obsdata/metadata/en/products/list/mag/kak"


def probe_jma_geomag(output_dir: str) -> dict:
    response, sample = get(JMA_GEOMAG_METADATA, timeout=30)
    links = re.findall(r'href="([^"]+)"', response.text if response else "")
    report = {
        "source": "jma_geomag",
        "source_group": "jma_geomag",
        "status": "ok" if response is not None and response.status_code == 200 else "error",
        "sample_http": sample.as_dict(),
        "available_links_sample": links[:60],
        "parser_status": "probe_only",
        "reason": "Kakioka metadata is reachable; data file selection appears form/JS driven, so MVP records probe status without scraping.",
    }
    write_json(f"{output_dir}/metadata/probe_reports/jma_geomag_probe.json", report)
    return report


def fetch_jma_geomag(start_date: str, end_date: str, output_dir: str) -> list[dict]:
    return []
