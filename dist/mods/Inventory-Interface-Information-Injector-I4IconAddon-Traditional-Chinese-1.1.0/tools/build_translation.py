#!/usr/bin/env python3
"""Build the I4 Icon Addon UTF-16 LE translation asset from UTF-8 TSV."""

from __future__ import annotations

import codecs
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "Interface" / "Translations" / "I4IconAddon_ENGLISH.txt"
EXPECTED_KEYS = (
    "$Backpack", "$ClothingCloak", "$ScrollSpider", "$CampingSupplies",
    "$BuildingMaterial", "$NetchLeather", "$FishingRod", "$AyleidCrystal",
    "$HorseTack", "$PetGear", "$SoulTomato", "$BrokenWeapon",
    "$DwarvenScrap", "$ElderScroll", "$Instrument", "$BugJar", "$BearTrap",
)


def load_lines() -> list[str]:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    keys: list[str] = []
    for number, line in enumerate(lines, start=1):
        if line.count("\t") != 1:
            raise SystemExit(f"line {number}: expected exactly one tab")
        key, value = line.split("\t")
        if not key or not value:
            raise SystemExit(f"line {number}: key and value must be non-empty")
        keys.append(key)
    if tuple(keys) != EXPECTED_KEYS:
        raise SystemExit("translation keys or order differ from I4 Icon Addon 1.1.0")
    return lines


def main() -> None:
    # The current upstream asset uses CRLF between records and no final newline.
    payload = codecs.BOM_UTF16_LE + "\r\n".join(load_lines()).encode("utf-16-le")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    print(f"wrote {TARGET.relative_to(ROOT)} ({len(payload)} bytes, sha256={digest})")


if __name__ == "__main__":
    main()
