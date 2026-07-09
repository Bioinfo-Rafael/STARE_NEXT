from src.excel_adapters.generic_url_probe import GenericUrlProbeAdapter
from src.excel_adapters.jma_catalog import JmaCatalogAdapter


def adapter_for(record, output_dir, raw_dir, keep_raw=False):
    adapters = [JmaCatalogAdapter(output_dir, raw_dir, keep_raw), GenericUrlProbeAdapter(output_dir, raw_dir, keep_raw)]
    for adapter in adapters:
        if adapter.can_handle(record):
            return adapter
    return adapters[-1]
