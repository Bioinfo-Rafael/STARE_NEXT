from __future__ import annotations

import re

from src.utils.http import get
from src.utils.io import write_json

INTERMAGNET_SERVICES = "https://imag-data.bgs.ac.uk/GIN_V1/GINServices"


def probe_intermagnet(output_dir: str) -> dict:
    response, sample = get(INTERMAGNET_SERVICES, timeout=30)
    text = response.text if response else ""
    codes = re.findall(r"<Code>([^<]+)</Code>", text)
    east_asia = [c for c in codes if c in {"KAK", "MMB", "KNY", "CBI", "KNY", "KAK"}]
    report = {
        "source": "intermagnet",
        "source_group": "intermagnet",
        "status": "ok" if response is not None and response.status_code == 200 else "error",
        "sample_http": sample.as_dict(),
        "observatory_codes_sample": codes[:60],
        "japan_codes_detected": east_asia,
        "parser_status": "probe_only",
        "reason": "IAGA/CDF data URL construction is recorded for follow-up; MVP does not bulk download observatory minute data.",
    }
    write_json(f"{output_dir}/metadata/probe_reports/intermagnet_probe.json", report)
    return report


def fetch_intermagnet(start_date: str, end_date: str, output_dir: str) -> list[dict]:
    return []
