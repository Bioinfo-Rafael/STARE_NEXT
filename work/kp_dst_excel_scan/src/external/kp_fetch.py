from __future__ import annotations

from src.utils.http import get, json_or_none
from src.utils.io import write_json


GFZ_KP_URL = "https://kp.gfz.de/app/json/"


def probe_kp(output_dir: str) -> dict:
    response, sample = get(GFZ_KP_URL, params={"start": "2020-01-01T00:00:00Z", "end": "2020-01-03T23:59:59Z", "index": "Kp", "status": "all"}, timeout=20)
    data = json_or_none(response)
    report = {
        "source": "kp",
        "status": "ok" if isinstance(data, dict) and data.get("Kp") else "error",
        "sample_http": sample.as_dict(),
        "sample_keys": list(data.keys()) if isinstance(data, dict) else [],
    }
    write_json(f"{output_dir}/metadata/probe_reports/kp_probe.json", report)
    return report


def fetch_kp(start_date: str, end_date: str) -> list[dict]:
    response, sample = get(
        GFZ_KP_URL,
        params={"start": f"{start_date}T00:00:00Z", "end": f"{end_date}T23:59:59Z", "index": "Kp", "status": "all"},
        timeout=60,
    )
    data = json_or_none(response)
    if not isinstance(data, dict) or not data.get("Kp") or not data.get("datetime"):
        raise RuntimeError(f"GFZ Kp fetch failed: {sample.as_dict()}")
    rows: list[dict] = []
    for dt, kp in zip(data["datetime"], data["Kp"]):
        date = str(dt)[:10]
        if start_date <= date <= end_date:
            rows.append({"datetime": dt, "date": date, "kp": float(kp), "source": "GFZ"})
    return rows
