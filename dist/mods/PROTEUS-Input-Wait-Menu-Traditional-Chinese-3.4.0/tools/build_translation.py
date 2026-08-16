#!/usr/bin/env python3
"""Build the PROTEUS Input Wait Menu game asset from reviewable UTF-8 TSV."""

from __future__ import annotations

import codecs
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "Interface" / "translations" / "Input Wait Menu_english.txt"
EXPECTED_ROWS = 80


def load_rows() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for number, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines(), start=1):
        if line.count("\t") != 1:
            raise SystemExit(f"line {number}: expected exactly one tab")
        key, value = line.split("\t")
        if not key.startswith("$") or not value:
            raise SystemExit(f"line {number}: expected non-empty $key and translation")
        rows.append((key, value))
    if len(rows) != EXPECTED_ROWS or len({key for key, _ in rows}) != EXPECTED_ROWS:
        raise SystemExit(f"expected {EXPECTED_ROWS} unique keys")
    return rows


def main() -> None:
    # Match PROTEUS 3.4.0: UTF-16LE BOM, CRLF between records, no final newline.
    text = "\r\n".join(f"{key}\t{value}" for key, value in load_rows())
    payload = codecs.BOM_UTF16_LE + text.encode("utf-16le")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(payload)
    print(f"wrote {TARGET.relative_to(ROOT)} ({len(payload)} bytes, sha256={hashlib.sha256(payload).hexdigest()})")


if __name__ == "__main__":
    main()
