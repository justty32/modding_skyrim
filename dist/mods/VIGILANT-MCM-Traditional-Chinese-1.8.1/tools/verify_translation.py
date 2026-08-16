#!/usr/bin/env python3
"""Verify the VIGILANT SE 1.8.1 Traditional Chinese MCM override."""

from __future__ import annotations

import argparse
import codecs
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSLATION_SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "interface" / "Translations" / "VIGILANT_ENGLISH.txt"
MANIFEST = ROOT / "MANIFEST.sha256"
EXPECTED_SOURCE_SHA256 = "148a04073297213ec84de8e55491b02559649ea7be63cde16616bf0ab1bd1d6f"
EXPECTED_KEYS = (
    "$VigBossDifficulty", "$VigDiffLvl", "$VigIncAttack", "$VigAnimStab",
    "$VigMusLoop", "$VigSceneSkipKey", "$VigDebug", "$VigInfoDifficulty",
    "$VigInfoAttackPower", "$VigInfoAnimStab", "$VigInfoMusLoop", "$VigSceneSkip",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_source(path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.count("\t") != 1:
            raise AssertionError(f"{path}: line {number} must contain exactly one tab")
        key, value = line.split("\t")
        if not key or not value:
            raise AssertionError(f"{path}: line {number} has an empty key or value")
        rows.append((key, value))
    return rows


def parse_game_asset(path: Path) -> tuple[bytes, list[tuple[str, str]]]:
    data = path.read_bytes()
    if not data.startswith(codecs.BOM_UTF16_LE):
        raise AssertionError(f"{path}: missing UTF-16 LE BOM")
    text = data[len(codecs.BOM_UTF16_LE):].decode("utf-16-le")
    if text.endswith(("\r", "\n")):
        raise AssertionError(f"{path}: final record must not have a line terminator")
    if "\r\n".join(text.split("\r\n")) != text:
        raise AssertionError(f"{path}: invalid line terminators")
    return data, [tuple(line.split("\t")) for line in text.split("\r\n")]


def verify_manifest() -> int:
    checked = 0
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), start=1):
        if "  " not in line:
            raise AssertionError(f"{MANIFEST}: malformed line {number}")
        expected, relative = line.split("  ", maxsplit=1)
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents or sha256(path.read_bytes()) != expected:
            raise AssertionError(f"{relative}: manifest mismatch")
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="live VIGILANT 1.8.1 ENGLISH translation file")
    args = parser.parse_args()
    source_rows = parse_source(TRANSLATION_SOURCE)
    if tuple(key for key, _ in source_rows) != EXPECTED_KEYS or len(set(key for key, _ in source_rows)) != len(EXPECTED_KEYS):
        raise AssertionError("reviewable source keys or order differ from VIGILANT SE 1.8.1")
    print("PASS reviewable source: UTF-8, 12 unique keys, exact order")
    target_data, target_rows = parse_game_asset(TARGET)
    if target_rows != source_rows:
        raise AssertionError("game asset differs from translation-source.tsv")
    print(f"PASS game asset: UTF-16 LE BOM, CRLF, no final newline, 12 exact rows, sha256={sha256(target_data)}")
    if args.source is not None:
        upstream_data, upstream_rows = parse_game_asset(args.source)
        if sha256(upstream_data) != EXPECTED_SOURCE_SHA256 or tuple(key for key, _ in upstream_rows) != EXPECTED_KEYS:
            raise AssertionError("upstream source hash or key/order differ from VIGILANT SE 1.8.1")
        print("PASS upstream parity: exact source hash and key/order match")
    print(f"PASS manifest: {verify_manifest()} files match")
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
