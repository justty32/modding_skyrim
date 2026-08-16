#!/usr/bin/env python3
"""Verify the Constellations 1.0.2 Traditional Chinese text-only override."""

from __future__ import annotations

import argparse
import codecs
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRANSLATION_SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "Interface" / "Translations" / "ConstellationsNewSkills_ENGLISH.txt"
MANIFEST = ROOT / "MANIFEST.sha256"
EXPECTED_SOURCE_SHA256 = "69646dc81195b7e4faeb81cc88ddecf76af7a2b1a7467af2d26e45eb3aa0caa4"
EXPECTED_KEYS = (
    "$Athletics_Name",
    "$HandToHand_Name",
    "$Sorcery_Name",
    "$Athletics_Description",
    "$HandToHand_Description",
    "$Sorcery_Description",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_utf8_translation_source(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    rows: list[tuple[str, str]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if line.count("\t") != 1:
            raise AssertionError(f"{path}: line {number} must contain exactly one tab")
        key, value = line.split("\t")
        if not key or not value:
            raise AssertionError(f"{path}: line {number} has an empty key or value")
        rows.append((key, value))
    return rows


def parse_game_translation(path: Path) -> tuple[bytes, list[tuple[str, str]]]:
    data = path.read_bytes()
    if not data.startswith(codecs.BOM_UTF16_LE):
        raise AssertionError(f"{path}: missing UTF-16 LE BOM")
    body = data[len(codecs.BOM_UTF16_LE) :]
    if len(body) % 2:
        raise AssertionError(f"{path}: UTF-16 LE payload has odd byte length")
    text = body.decode("utf-16-le")
    if "\x00" in text:
        raise AssertionError(f"{path}: decoded text contains NUL")
    if text.endswith(("\r", "\n")):
        raise AssertionError(f"{path}: final record must not have a line terminator")
    if "\r\n".join(text.split("\r\n")) != text:
        raise AssertionError(f"{path}: invalid line terminators")
    if "\n" in text.replace("\r\n", "") or "\r" in text.replace("\r\n", ""):
        raise AssertionError(f"{path}: found a non-CRLF line terminator")

    rows: list[tuple[str, str]] = []
    for number, line in enumerate(text.split("\r\n"), start=1):
        if line.count("\t") != 1:
            raise AssertionError(f"{path}: line {number} must contain exactly one tab")
        key, value = line.split("\t")
        if not key or not value:
            raise AssertionError(f"{path}: line {number} has an empty key or value")
        rows.append((key, value))
    return data, rows


def verify_manifest() -> int:
    checked = 0
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), start=1):
        if "  " not in line:
            raise AssertionError(f"{MANIFEST}: malformed line {number}")
        expected, relative = line.split("  ", maxsplit=1)
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents:
            raise AssertionError(f"{MANIFEST}: unsafe path on line {number}")
        actual = sha256(path.read_bytes())
        if actual != expected:
            raise AssertionError(f"{relative}: sha256 {actual} != {expected}")
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        help="optional path to the upstream 1.0.2 ENGLISH translation file",
    )
    args = parser.parse_args()

    expected_rows = parse_utf8_translation_source(TRANSLATION_SOURCE)
    if tuple(key for key, _ in expected_rows) != EXPECTED_KEYS:
        raise AssertionError("translation-source.tsv keys or order differ from 1.0.2")
    if len(set(key for key, _ in expected_rows)) != len(EXPECTED_KEYS):
        raise AssertionError("translation-source.tsv contains duplicate keys")
    print("PASS reviewable source: UTF-8, 6 unique keys, exact order")

    target_data, target_rows = parse_game_translation(TARGET)
    if target_rows != expected_rows:
        raise AssertionError("game asset differs from translation-source.tsv")
    print(
        "PASS game asset: UTF-16 LE BOM, CRLF, no final newline, "
        f"6 exact rows, sha256={sha256(target_data)}"
    )

    if args.source is not None:
        source_data, source_rows = parse_game_translation(args.source)
        source_digest = sha256(source_data)
        if source_digest != EXPECTED_SOURCE_SHA256:
            raise AssertionError(
                f"upstream source sha256 {source_digest} != {EXPECTED_SOURCE_SHA256}"
            )
        if tuple(key for key, _ in source_rows) != EXPECTED_KEYS:
            raise AssertionError("upstream keys or order differ from expected 1.0.2")
        print("PASS upstream parity: exact source hash and key/order match")

    if MANIFEST.exists():
        checked = verify_manifest()
        print(f"PASS manifest: {checked} files match")

    print("RESULT: PASS")


if __name__ == "__main__":
    main()
