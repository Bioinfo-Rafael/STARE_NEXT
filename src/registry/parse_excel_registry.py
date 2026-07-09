from __future__ import annotations

import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from src.registry.dataset_registry import DatasetRecord
from src.utils.io import ensure_dir, write_csv, write_json

NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def _colnum(ref: str) -> int:
    m = re.match(r"([A-Z]+)", ref)
    if not m:
        return 0
    n = 0
    for ch in m.group(1):
        n = n * 26 + ord(ch) - 64
    return n - 1


def _text(cell: str) -> str:
    return re.sub(r"\s+", " ", str(cell or "")).strip()


def _slug(text: str, fallback: str) -> str:
    text = re.sub(r"https?://", "", text)
    text = re.sub(r"[^0-9A-Za-zぁ-んァ-ヶ一-龠ー]+", "_", text).strip("_").lower()
    return text[:80] or fallback


def read_xlsx_rows(path: str | Path) -> dict[str, list[list[str]]]:
    """Read visible cell text from an xlsx file using only the standard library."""
    path = Path(path)
    with zipfile.ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("a:si", NS):
                parts = [t.text or "" for t in si.iter(f"{{{NS['a']}}}t")]
                shared.append("".join(parts))

        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rid_to_target = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
        out: dict[str, list[list[str]]] = {}
        for sh in wb.find("a:sheets", NS) or []:
            name = sh.attrib["name"]
            rid = sh.attrib[f"{{{NS['r']}}}id"]
            target = rid_to_target[rid]
            sheet_path = "xl/" + target if not target.startswith("/") else target[1:]
            root = ET.fromstring(z.read(sheet_path))
            rows: list[list[str]] = []
            for row in root.findall(".//a:sheetData/a:row", NS):
                cells: list[tuple[int, str]] = []
                maxc = -1
                for c in row.findall("a:c", NS):
                    idx = _colnum(c.attrib.get("r", "A1"))
                    value = ""
                    if c.attrib.get("t") == "inlineStr":
                        value = "".join(t.text or "" for t in c.iter(f"{{{NS['a']}}}t"))
                    else:
                        v = c.find("a:v", NS)
                        if v is not None:
                            raw = v.text or ""
                            value = shared[int(raw)] if c.attrib.get("t") == "s" and raw.isdigit() else raw
                    cells.append((idx, _text(value)))
                    maxc = max(maxc, idx)
                vals = [""] * (maxc + 1)
                for idx, value in cells:
                    vals[idx] = value
                rows.append(vals)
            out[name] = rows
        return out


def inspect_workbook(path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    rows_by_sheet = read_xlsx_rows(path)
    summary: dict[str, Any] = {"workbook": str(path), "sheets": []}
    for sheet, rows in rows_by_sheet.items():
        max_cols = max((len(r) for r in rows[:12]), default=0)
        summary["sheets"].append(
            {
                "sheet_name": sheet,
                "n_rows_seen": len(rows),
                "n_cols_first_12": max_cols,
                "first_10_rows": [r[:max_cols] for r in rows[:10]],
            }
        )
    write_json(Path(output_dir) / "metadata" / "excel_inspection.json", summary)
    return summary


def _find_header_row(rows: list[list[str]]) -> int:
    best_idx = 0
    best_score = -1
    keywords = ["URL", "データ名", "分類", "所管", "概要", "データ"]
    for i, row in enumerate(rows[:20]):
        joined = " ".join(row)
        score = sum(1 for kw in keywords if kw in joined) + sum(1 for v in row if v)
        if score > best_score and ("URL" in joined or "データ名" in joined or "分類" in joined):
            best_idx = i
            best_score = score
    return best_idx


def _headers(rows: list[list[str]], header_idx: int) -> list[str]:
    header = rows[header_idx] if header_idx < len(rows) else []
    sub = rows[header_idx + 1] if header_idx + 1 < len(rows) else []
    width = max(len(header), len(sub))
    out: list[str] = []
    last = ""
    for i in range(width):
        h = _text(header[i] if i < len(header) else "")
        s = _text(sub[i] if i < len(sub) else "")
        if h:
            last = h
        name = h or last or f"col_{i+1}"
        if s and s not in name:
            name = f"{name}_{s}"
        out.append(name)
    return out


def _pick(row: dict[str, str], patterns: list[str]) -> str:
    for pat in patterns:
        rx = re.compile(pat)
        for key, value in row.items():
            if rx.search(key) and value:
                return value
    return ""


def _status(row: dict[str, str], url: str, access: str, notes: str) -> str:
    blob = " ".join([url, access, notes, " ".join(row.values())])
    if not url:
        return "no_url"
    if re.search(r"登録|ログイン|申請|審査|API.?key|認証|アカウント", blob, re.I):
        return "requires_registration_or_key"
    if "停止" in blob or "不可" in blob:
        return "maybe_unavailable"
    return "candidate"


def parse_excel_registry(path: str | Path, output_dir: str | Path = "results") -> list[DatasetRecord]:
    rows_by_sheet = read_xlsx_rows(path)
    records: list[DatasetRecord] = []
    for sheet, rows in rows_by_sheet.items():
        if not rows:
            continue
        header_idx = _find_header_row(rows)
        headers = _headers(rows, header_idx)
        start_idx = header_idx + 1
        if start_idx < len(rows) and sum(1 for v in rows[start_idx] if v) < 4:
            start_idx += 1
        for rnum, vals in enumerate(rows[start_idx:], start=start_idx + 1):
            if not any(vals):
                continue
            row = {headers[i] if i < len(headers) else f"col_{i+1}": vals[i] for i in range(len(vals))}
            url = _pick(row, [r"URL"])
            name = _pick(row, [r"データ名", r"データベース", r"サイト", r"情報"])
            category = _pick(row, [r"分類"])
            provider = _pick(row, [r"所管", r"提供", r"機関"])
            desc = _pick(row, [r"概要", r"説明"])
            access = _pick(row, [r"取得", r"公開状況", r"アクセス"])
            notes = _pick(row, [r"備考", r"形式"])
            if not name and not url:
                nonempty = [v for v in vals if v]
                if len(nonempty) >= 2:
                    provider, name = nonempty[0], nonempty[1]
                elif nonempty:
                    name = nonempty[0]
            if not name:
                continue
            dataset_id = _slug(f"{provider}_{name}", f"{sheet}_{rnum}")
            records.append(
                DatasetRecord(
                    dataset_id=dataset_id,
                    name=name,
                    category=category,
                    provider=provider,
                    description=desc,
                    url=url,
                    access_type=access,
                    notes=notes,
                    usable_status=_status(row, url, access, notes),
                    sheet_name=sheet,
                    source_row=rnum,
                )
            )

    out_dir = ensure_dir(Path(output_dir) / "metadata")
    fieldnames = list(DatasetRecord("", "").as_dict().keys())
    write_csv(out_dir / "dataset_registry.csv", [r.as_dict() for r in records], fieldnames)
    inspect_workbook(path, output_dir)
    return records


def load_registry_csv(path: str | Path) -> list[DatasetRecord]:
    import csv

    records: list[DatasetRecord] = []
    with Path(path).open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            records.append(DatasetRecord(**{k: row.get(k, "") for k in DatasetRecord("", "").as_dict().keys()}))
    return records
