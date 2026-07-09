from __future__ import annotations

import json
from urllib.parse import quote

from src.utils.dates import year_iter
from src.utils.http import get, json_or_none
from src.utils.io import append_jsonl, write_json

HAPI_BASE = "https://cdaweb.gsfc.nasa.gov/hapi"
OMNI_DATASET = "OMNI2_H0_MRG1HR"
OMNI_PARAMS = [
    "Time",
    "ABS_B1800",
    "BZ_GSM1800",
    "N1800",
    "V1800",
    "Pressure1800",
    "E1800",
    "Beta1800",
    "Mach_num1800",
    "R1800",
    "F10_INDEX1800",
    "DST1800",
    "AE1800",
    "AL_INDEX1800",
    "AU_INDEX1800",
]

NAME_MAP = {
    "ABS_B1800": "IMF_B_total",
    "BZ_GSM1800": "IMF_Bz",
    "N1800": "proton_density",
    "V1800": "solar_wind_speed",
    "Pressure1800": "flow_pressure",
    "E1800": "electric_field",
    "Beta1800": "plasma_beta",
    "Mach_num1800": "alfven_mach_number",
    "R1800": "sunspot_number",
    "F10_INDEX1800": "F10_7",
    "DST1800": "omni_dst",
    "AE1800": "AE_index",
    "AL_INDEX1800": "AL_index",
    "AU_INDEX1800": "AU_index",
}


def probe_omni(output_dir: str) -> dict:
    response, sample = get(f"{HAPI_BASE}/info", params={"id": OMNI_DATASET}, timeout=30)
    data = json_or_none(response)
    params = [p.get("name") for p in data.get("parameters", [])] if isinstance(data, dict) else []
    ok = response is not None and response.status_code == 200 and all(p in params for p in OMNI_PARAMS[:5])
    report = {
        "source": "omni",
        "source_group": "omni",
        "dataset": OMNI_DATASET,
        "status": "ok" if ok else "error",
        "sample_http": sample.as_dict(),
        "available_parameters_sample": params[:80],
        "selected_parameters": OMNI_PARAMS,
    }
    write_json(f"{output_dir}/metadata/probe_reports/omni_probe.json", report)
    return report


def _hapi_data_url(start: str, end: str) -> str:
    encoded_params = ",".join(quote(p, safe="") for p in OMNI_PARAMS)
    return (
        f"{HAPI_BASE}/data?id={OMNI_DATASET}&parameters={encoded_params}"
        f"&time.min={start}T00:00:00Z&time.max={end}T23:59:59Z&format=json"
    )


def _clean_value(name: str, value) -> float | None:
    try:
        x = float(value)
    except Exception:
        return None
    fill_values = {
        "ABS_B1800": 999.9,
        "BZ_GSM1800": 999.9,
        "N1800": 999.9,
        "V1800": 9999.0,
        "Pressure1800": 99.99,
        "E1800": 999.99,
        "Beta1800": 999.99,
        "Mach_num1800": 999.9,
        "R1800": 999,
        "F10_INDEX1800": 999.9,
        "DST1800": 99999,
        "AE1800": 99999,
        "AL_INDEX1800": 99999,
        "AU_INDEX1800": 99999,
    }
    fill = fill_values.get(name)
    if fill is not None and abs(x - fill) < 1e-9:
        return None
    return x


def fetch_omni(start_date: str, end_date: str, output_dir: str) -> list[dict]:
    rows: list[dict] = []
    for year in year_iter(start_date, end_date):
        chunk_start = max(start_date, f"{year}-01-01")
        chunk_end = min(end_date, f"{year}-12-31")
        response, sample = get(_hapi_data_url(chunk_start, chunk_end), timeout=90)
        data = json_or_none(response)
        if not isinstance(data, dict) or data.get("status", {}).get("code") != 1200:
            append_jsonl(f"{output_dir}/space_weather4_failures.jsonl", {"source": "omni", "year": year, "status": "fetch_error", "sample_http": sample.as_dict(), "body_head": response.text[:500] if response else ""})
            continue
        parameters = [p.get("name") for p in data.get("parameters", [])]
        for values in data.get("data", []):
            if not values:
                continue
            row = {"datetime": values[0], "date": str(values[0])[:10], "source": "NASA_CDAWeb_HAPI", "dataset": OMNI_DATASET}
            for name, value in zip(parameters[1:], values[1:]):
                row[NAME_MAP.get(name, name)] = _clean_value(name, value)
            if start_date <= row["date"] <= end_date:
                rows.append(row)
    return rows
