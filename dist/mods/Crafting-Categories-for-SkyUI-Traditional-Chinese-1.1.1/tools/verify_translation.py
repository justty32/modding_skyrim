#!/usr/bin/env python3
"""Verify the Crafting Categories for SkyUI 1.1.1 Traditional Chinese override."""

from __future__ import annotations

import argparse
import codecs
import hashlib
from pathlib import Path

from build_translation import EXPECTED_KEYS


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "Interface" / "Translations" / "CraftingCategories_ENGLISH.txt"
MANIFEST = ROOT / "MANIFEST.sha256"
EXPECTED_SOURCE_SHA256 = "ed93daca5f50c8b02fcf78a801842ce4bad1527340495a34900a4f52c5eeb5c5"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_rows(path: Path) -> tuple[bytes, list[tuple[str, str]]]:
    data = path.read_bytes()
    if not data.startswith(codecs.BOM_UTF16_LE):
        raise AssertionError(f"{path}: missing UTF-16 LE BOM")
    body = data[len(codecs.BOM_UTF16_LE):]
    if len(body) % 2:
        raise AssertionError(f"{path}: odd UTF-16 LE payload")
    text = body.decode("utf-16-le")
    if not text.endswith("\r\n"):
        raise AssertionError(f"{path}: expected a final CRLF")
    if "\r\n".join(text.split("\r\n")) != text or "\n" in text.replace("\r\n", "") or "\r" in text.replace("\r\n", ""):
        raise AssertionError(f"{path}: must use CRLF only")
    rows: list[tuple[str, str]] = []
    lines = text.split("\r\n")
    if lines.pop() != "":
        raise AssertionError(f"{path}: malformed final CRLF")
    for number, line in enumerate(lines, start=1):
        if line.count("\t") != 1:
            raise AssertionError(f"{path}: line {number} needs exactly one tab")
        key, value = line.split("\t")
        if not key or not value:
            raise AssertionError(f"{path}: line {number} has an empty key or value")
        rows.append((key, value))
    return data, rows


def review_rows() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for number, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines(), start=1):
        if line.count("\t") != 1:
            raise AssertionError(f"{SOURCE}: line {number} needs exactly one tab")
        key, value = line.split("\t")
        if not key or not value:
            raise AssertionError(f"{SOURCE}: line {number} has an empty key or value")
        rows.append((key, value))
    return rows


def verify_manifest() -> int:
    checked = 0
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), start=1):
        if "  " not in line:
            raise AssertionError(f"{MANIFEST}: malformed line {number}")
        expected, relative = line.split("  ", 1)
        candidate = (ROOT / relative).resolve()
        if ROOT not in candidate.parents or digest(candidate.read_bytes()) != expected:
            raise AssertionError(f"{MANIFEST}: checksum mismatch for {relative}")
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="upstream 1.1.1 ENGLISH translation file")
    args = parser.parse_args()

    expected = review_rows()
    if tuple(key for key, _ in expected) != EXPECTED_KEYS or len(expected) != 17:
        raise AssertionError("review source keys or order differ from 1.1.1")
    if len({key for key, _ in expected}) != len(expected):
        raise AssertionError("review source contains duplicate keys")
    target_data, target = parse_rows(TARGET)
    if target != expected:
        raise AssertionError("game asset differs from reviewable translation source")
    print("PASS game asset: UTF-16 LE BOM, CRLF including final CRLF, 17 exact rows")

    if args.source:
        upstream_data, upstream = parse_rows(args.source)
        if digest(upstream_data) != EXPECTED_SOURCE_SHA256:
            raise AssertionError("source checksum is not the approved Crafting Categories 1.1.1 baseline")
        if tuple(key for key, _ in upstream) != EXPECTED_KEYS:
            raise AssertionError("upstream keys or order differ from 1.1.1")
        print("PASS upstream parity: approved hash, 17 keys, exact order")

    print(f"PASS manifest: {verify_manifest()} files match")
    print(f"RESULT: PASS ({digest(target_data)})")


if __name__ == "__main__":
    main()
