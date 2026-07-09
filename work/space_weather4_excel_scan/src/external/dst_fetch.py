from __future__ import annotations

import re

from src.utils.dates import month_iter
from src.utils.http import get
from src.utils.io import append_jsonl, write_json


KYOTO_DST_URLS = [
    ("final", "https://wdc.kugi.kyoto-u.ac.jp/dst_final/{yyyymm}/index.html"),
    ("provisional", "https://wdc.kugi.kyoto-u.ac.jp/dst_provisional/{yyyymm}/index.html"),
]


def probe_dst(output_dir: str) -> dict:
    url = KYOTO_DST_URLS[0][1].format(yyyymm="202001")
    response, sample = get(url, timeout=20)
    ok = response is not None and response.status_code == 200 and "Dst" in response.text
    report = {
        "source": "dst",
        "status": "ok" if ok else "error",
        "sample_http": sample.as_dict(),
        "guessed_format": "Kyoto WDC monthly HTML table",
    }
    write_json(f"{output_dir}/metadata/probe_reports/dst_probe.json", report)
    return report


def _parse_month_html(yyyymm: str, html: str) -> list[dict]:
    text = re.sub(r"<[^>]+>", " ", html)
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    rows: list[dict] = []
    year = int(yyyymm[:4])
    month = int(yyyymm[4:])
    for line in lines:
        nums = re.findall(r"-?\d+", line)
        if len(nums) < 25:
            continue
        day = int(nums[0])
        if not (1 <= day <= 31):
            continue
        hourly = [int(x) for x in nums[1:25]]
        for hour, dst in enumerate(hourly):
            rows.append({"datetime": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:00:00Z", "date": f"{year:04d}-{month:02d}-{day:02d}", "dst": float(dst), "source": "KyotoWDC"})
    return rows


def fetch_dst(start_date: str, end_date: str, output_dir: str) -> list[dict]:
    all_rows: list[dict] = []
    for yyyymm in month_iter(start_date, end_date):
        response = None
        sample = None
        product = ""
        for candidate_product, template in KYOTO_DST_URLS:
            url = template.format(yyyymm=yyyymm)
            response, sample = get(url, timeout=30)
            if response is not None and response.status_code == 200:
                product = candidate_product
                break
        if response is None or response.status_code != 200:
            append_jsonl(f"{output_dir}/space_weather4_failures.jsonl", {"source": "dst", "month": yyyymm, "status": "fetch_error", "sample_http": sample.as_dict() if sample else {}})
            continue
        rows = _parse_month_html(yyyymm, response.text)
        if not rows:
            append_jsonl(f"{output_dir}/space_weather4_failures.jsonl", {"source": "dst", "month": yyyymm, "status": "parse_empty", "sample_http": sample.as_dict() if sample else {}, "dst_product": product})
            continue
        for row in rows:
            row["dst_product"] = product
        all_rows.extend(row for row in rows if start_date <= row["date"] <= end_date)
    return all_rows
