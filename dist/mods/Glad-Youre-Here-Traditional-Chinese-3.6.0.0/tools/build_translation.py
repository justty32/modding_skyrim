#!/usr/bin/env python3
"""Build the game-facing translation from the reviewable UTF-8 TSV."""

from __future__ import annotations

import codecs
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "interface" / "translations" / "ImGladYoureHere_english.txt"


def load_rows() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for number, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines(), start=1):
        if line.count("\t") != 1:
            raise SystemExit(f"line {number}: expected exactly one tab")
        key, value = line.split("\t")
        if not key or not value:
            raise SystemExit(f"line {number}: key and value must be non-empty")
        rows.append((key, value))
    if len(rows) != 213 or len({key for key, _ in rows}) != len(rows):
        raise SystemExit("expected 213 unique Glad You're Here 3.6.0.0 keys")
    return rows


def main() -> None:
    # Skyrim-facing output deliberately uses CRLF after every record, including the last.
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
