from __future__ import annotations

from pathlib import Path
from typing import Any

from src.registry.dataset_registry import DatasetRecord
from src.utils.http import get
from src.utils.io import append_jsonl, write_json


class SkipDataset(RuntimeError):
    pass


class BaseExcelAdapter:
    adapter_name = "base"

    def __init__(self, output_dir: str | Path, raw_dir: str | Path, keep_raw: bool = False):
        self.output_dir = Path(output_dir)
        self.raw_dir = Path(raw_dir)
        self.keep_raw = keep_raw

    def can_handle(self, record: DatasetRecord) -> bool:
        return False

    def probe(self, record: DatasetRecord) -> dict[str, Any]:
        if not record.url:
            report = self._report(record, "skip", reason="no_url", parser_status="not_applicable")
        else:
            response, sample = get(record.url, timeout=20)
            text = sample.text_head.lower()
            requires = any(x in text for x in ["login", "ログイン", "登録", "申請", "forbidden"]) or sample.status_code in {401, 403}
            guessed = "html"
            if "csv" in (sample.content_type or "").lower() or record.url.lower().endswith(".csv"):
                guessed = "csv"
            elif "zip" in (sample.content_type or "").lower() or record.url.lower().endswith(".zip"):
                guessed = "zip"
            report = self._report(
                record,
                "ok" if response is not None and response.status_code and response.status_code < 400 and not requires else "skip",
                sample_http=sample.as_dict(),
                guessed_format=guessed,
                requires_login_or_manual_download=requires,
                parser_status="probe_only",
                reason="requires_login_or_manual_download" if requires else "",
            )
        write_json(self.output_dir / "metadata" / "probe_reports" / f"{record.excel_dataset_id}.json", report)
        return report

    def fetch(self, record: DatasetRecord, start_date: str, end_date: str) -> list[dict]:
        raise SkipDataset("adapter_not_implemented")

    def aggregate(self, record: DatasetRecord, rows: list[dict], start_date: str, end_date: str, spatial_unit: str) -> list[dict]:
        return rows

    def _report(self, record: DatasetRecord, status: str, **extra: Any) -> dict[str, Any]:
        return {
            "excel_dataset_id": record.excel_dataset_id,
            "name": record.name,
            "url": record.url,
            "adapter": self.adapter_name,
            "status": status,
            "final_url": extra.get("sample_http", {}).get("final_url", ""),
            "status_code": extra.get("sample_http", {}).get("status_code", ""),
            "content_type": extra.get("sample_http", {}).get("content_type", ""),
            "text_head": extra.get("sample_http", {}).get("text_head", ""),
            "guessed_format": extra.get("guessed_format", ""),
            "requires_login_or_manual_download": extra.get("requires_login_or_manual_download", False),
            "parser_status": extra.get("parser_status", ""),
            "reason_if_skipped": extra.get("reason", ""),
        }

    def failure(self, payload: dict[str, Any]) -> None:
        append_jsonl(self.output_dir / "space_weather4_failures.jsonl", payload)
