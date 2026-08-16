#!/usr/bin/env python3
"""Build VIGILANT's game-facing UTF-16 LE MCM translation asset."""

from __future__ import annotations

import codecs
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "interface" / "Translations" / "VIGILANT_ENGLISH.txt"
EXPECTED_KEYS = (
    "$VigBossDifficulty", "$VigDiffLvl", "$VigIncAttack", "$VigAnimStab",
    "$VigMusLoop", "$VigSceneSkipKey", "$VigDebug", "$VigInfoDifficulty",
    "$VigInfoAttackPower", "$VigInfoAnimStab", "$VigInfoMusLoop", "$VigSceneSkip",
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
        raise SystemExit("translation keys or order differ from VIGILANT SE 1.8.1")
    return lines


def main() -> None:
    # The live file has CRLF between records and no final newline.
    payload = codecs.BOM_UTF16_LE + "\r\n".join(load_lines()).encode("utf-16-le")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(payload)
    print(f"wrote {TARGET.relative_to(ROOT)} ({len(payload)} bytes, sha256={hashlib.sha256(payload).hexdigest()})")


if __name__ == "__main__":
    main()
