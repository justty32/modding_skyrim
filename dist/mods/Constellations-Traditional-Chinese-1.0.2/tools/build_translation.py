#!/usr/bin/env python3
"""Build the game-facing UTF-16 LE translation asset from reviewable UTF-8 TSV."""

from __future__ import annotations

import codecs
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "Interface" / "Translations" / "ConstellationsNewSkills_ENGLISH.txt"
EXPECTED_KEYS = (
    "$Athletics_Name",
    "$HandToHand_Name",
    "$Sorcery_Name",
    "$Athletics_Description",
    "$HandToHand_Description",
    "$Sorcery_Description",
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
        raise SystemExit("translation keys or order differ from Constellations 1.0.2")
    return lines


def main() -> None:
    # The upstream file has CRLF between records and no newline after the last one.
    payload = codecs.BOM_UTF16_LE + "\r\n".join(load_lines()).encode("utf-16-le")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    print(f"wrote {TARGET.relative_to(ROOT)} ({len(payload)} bytes, sha256={digest})")


if __name__ == "__main__":
    main()
