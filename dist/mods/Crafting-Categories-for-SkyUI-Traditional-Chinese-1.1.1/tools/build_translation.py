#!/usr/bin/env python3
"""Build the game-facing UTF-16 LE asset from the reviewable UTF-8 TSV."""

from __future__ import annotations

import codecs
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "Interface" / "Translations" / "CraftingCategories_ENGLISH.txt"
EXPECTED_KEYS = (
    "$CLOTHING", "$FOOD", "$JEWELRY", "$MISC", "$WEAPONS & ARMOR", "$Amber",
    "$Ancient Nord", "$Building Materials", "$Containers", "$Dragon", "$Exterior",
    "$Furniture", "$House", "$Madness", "$Ordinator", "$Shelves", "$Weapon Racks",
)


def load_rows() -> list[str]:
    rows = SOURCE.read_text(encoding="utf-8").splitlines()
    keys: list[str] = []
    for number, row in enumerate(rows, start=1):
        if row.count("\t") != 1:
            raise SystemExit(f"line {number}: expected exactly one tab")
        key, value = row.split("\t")
        if not key or not value:
            raise SystemExit(f"line {number}: key and value must be non-empty")
        keys.append(key)
    if tuple(keys) != EXPECTED_KEYS:
        raise SystemExit("translation keys or order differ from Crafting Categories for SkyUI 1.1.1")
    return rows


def main() -> None:
    # Upstream uses a BOM, CRLF separators, and a final CRLF.
    payload = codecs.BOM_UTF16_LE + ("\r\n".join(load_rows()) + "\r\n").encode("utf-16-le")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(payload)
    print(f"wrote {TARGET.relative_to(ROOT)} ({len(payload)} bytes, sha256={hashlib.sha256(payload).hexdigest()})")


if __name__ == "__main__":
    main()
