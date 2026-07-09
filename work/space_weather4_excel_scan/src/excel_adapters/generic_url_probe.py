from __future__ import annotations

from src.excel_adapters.base import BaseExcelAdapter, SkipDataset
from src.registry.dataset_registry import DatasetRecord


class GenericUrlProbeAdapter(BaseExcelAdapter):
    adapter_name = "generic_url_probe"

    def can_handle(self, record: DatasetRecord) -> bool:
        return True

    def fetch(self, record: DatasetRecord, start_date: str, end_date: str) -> list[dict]:
        raise SkipDataset(f"probe_only: no implemented parser for temporal_type={record.inferred_temporal_type}, usable_status={record.usable_status}")
