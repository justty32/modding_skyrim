#!/usr/bin/env python3
"""Build the NFF 2.8.6b game-facing translation from the reviewable TSV."""

from __future__ import annotations

import codecs
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "Interface" / "Translations" / "nwsFollowerFramework_english.txt"
EXPECTED_ROWS = 1398


def load_rows() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for number, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines(), start=1):
        if line.count("\t") != 1:
            raise SystemExit(f"line {number}: expected exactly one tab")
        key, value = line.split("\t")
        if not key.startswith("$") or not value:
            raise SystemExit(f"line {number}: invalid key or empty value")
        rows.append((key, value))
    if len(rows) != EXPECTED_ROWS or len({key for key, _ in rows}) != len(rows):
        raise SystemExit(f"expected {EXPECTED_ROWS} unique NFF 2.8.6b keys")
    return rows


def main() -> None:
    text = "\r\n".join(f"{key}\t{value}" for key, value in load_rows()) + "\r\n"
    payload = codecs.BOM_UTF16_LE + text.encode("utf-16-le")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(payload)
    print(
        f"wrote {TARGET.relative_to(ROOT)} ({len(payload)} bytes, "
        f"sha256={hashlib.sha256(payload).hexdigest()})"
    )


if __name__ == "__main__":
    main()
