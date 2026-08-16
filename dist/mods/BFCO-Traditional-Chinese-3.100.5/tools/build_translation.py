#!/usr/bin/env python3
"""Build the BFCO 3.100.5 game translation asset from its UTF-8 review source."""

from __future__ import annotations

import codecs
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "translation-source.txt"
TARGET = ROOT / "Interface" / "Translations" / "SCSI-ACTbfco-Main_english.txt"
EXPECTED_LINE_COUNT = 52
EXPECTED_KEYS = (
    "$BFCO", "$BFCO_SettingsPage", "$BFCO_header00", "$BFCO_TgInputType",
    "$BFCO_TgInputType_help", "$BFCO_TgInputTypeNUM_0", "$BFCO_TgInputTypeNUM_1",
    "$BFCO_TgInputTypeNUM_2", "$BFCO_TgInputTypeNUM_2short", "$BFCO_TgAnimaType",
    "$BFCO_TgAnimaType_help", "$BFCO_AnimaType_0", "$BFCO_AnimaType_1",
    "$BFCO_AnimaType_1short", "$BFCO_header01", "$BFCO_KeyAttackPowerNUM",
    "$BFCO_KeyAttackPowerNUM_help", "$BFCO_KeyAttackPowerNUMmodf",
    "$BFCO_KeyAttackPowerNUMmodf_help", "$BFCO_TgRmbAttackPowerNUM",
    "$BFCO_TgRmbAttackPowerNUM_help", "$BFCO_header02", "$BFCO_KeyAttackComb",
    "$BFCO_KeyAttackComb_help", "$BFCO_KeyAttackCombmodf", "$BFCO_KeyAttackCombmodf_help",
    "$BFCO_TgKeyAttackComb", "$BFCO_TgKeyAttackComb_help", "$BFCO_Debugheader",
    "$BFCO_TgJumpingAttack", "$BFCO_TgJumpingAttack_help", "$BFCO_TgDirectionalAttack",
    "$BFCO_TgDirectionalAttack_help", "$BFCO_TgDirectionalAttackHK",
    "$BFCO_TgDirectionalAttackHK_help", "$BFCO_TgInstantBlock", "$BFCO_TgInstantBlock_help",
)


def read_review_source() -> str:
    text = SOURCE.read_text(encoding="utf-8")
    if "\r" in text or not text.endswith("\n"):
        raise ValueError("review source must use LF and end with LF")
    lines = text.split("\n")
    if len(lines) != EXPECTED_LINE_COUNT:
        raise ValueError(f"expected {EXPECTED_LINE_COUNT} logical lines, got {len(lines)}")
    rows = [line.split("\t", 1) for line in lines if line]
    if any(line.count("\t") != 1 for line in lines if line):
        raise ValueError("each nonblank line must contain exactly one tab")
    if any(len(row) != 2 or not row[0] or not row[1] for row in rows):
        raise ValueError("each nonblank line must contain one nonempty key and value")
    keys = tuple(row[0] for row in rows)
    if keys != EXPECTED_KEYS or len(set(keys)) != len(keys):
        raise ValueError("translation keys or order differ from BFCO 3.100.5")
    return text


def main() -> None:
    text = read_review_source()
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(codecs.BOM_UTF16_LE + text.replace("\n", "\r\n").encode("utf-16-le"))
    print(f"built {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
