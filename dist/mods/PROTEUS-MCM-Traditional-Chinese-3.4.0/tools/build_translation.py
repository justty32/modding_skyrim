#!/usr/bin/env python3
"""Build the PROTEUS MCM UTF-16LE translation asset from the review TSV."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "tools" / "translation-source.tsv"
OUTPUT = ROOT / "Interface" / "Translations" / "PROTEUS_english.txt"


def read_rows() -> list[dict[str, str]]:
    with TSV.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows or set(rows[0]) != {"key", "source", "target"}:
        raise AssertionError("unexpected TSV columns")
    if len(rows) != 34 or len({row["key"] for row in rows}) != 34:
        raise AssertionError("expected 34 unique MCM keys")
    for row in rows:
        if not row["key"].startswith("$PROTEUS_MCM_") or not row["target"].strip():
            raise AssertionError(f"invalid translation row: {row!r}")
    return rows


def main() -> None:
    rows = read_rows()
    text = "\r\n".join(f'{row["key"]}\t{row["target"]}' for row in rows) + "\r\n"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(b"\xff\xfe" + text.encode("utf-16-le"))
    print(f"built {OUTPUT.relative_to(ROOT)}: {len(rows)} keys")


if __name__ == "__main__":
    main()
