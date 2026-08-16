#!/usr/bin/env python3
"""Verify the PROTEUS 3.4.0 Input Wait Menu Traditional Chinese override."""

from __future__ import annotations

import argparse
import codecs
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "Interface" / "translations" / "Input Wait Menu_english.txt"
MANIFEST = ROOT / "MANIFEST.sha256"
EXPECTED_UPSTREAM_SHA256 = "1230b4f0e891c73a4761b2f7d952907555b6d93d7f4948ea268a89b414991cbc"
EXPECTED_ROWS = 80
TOKEN = re.compile(r"\\\{\\\}|\\b\\d+(?:\\.\\d+)?\\b|%|\\\\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_rows(text: str, path: Path, *, expect_crlf: bool) -> list[tuple[str, str]]:
    if expect_crlf:
        if "\n" in text.replace("\r\n", "") or "\r" in text.replace("\r\n", ""):
            raise AssertionError(f"{path}: line endings are not exclusively CRLF")
        if text.endswith("\r\n"):
            raise AssertionError(f"{path}: unexpected final newline")
        lines = text.split("\r\n")
    else:
        lines = text.splitlines()
    rows: list[tuple[str, str]] = []
    for number, line in enumerate(lines, start=1):
        if line.count("\t") != 1:
            raise AssertionError(f"{path}: line {number} must contain exactly one tab")
        key, value = line.split("\t")
        if not key.startswith("$") or not value:
            raise AssertionError(f"{path}: line {number} has an invalid key or empty value")
        rows.append((key, value))
    if len(rows) != EXPECTED_ROWS or len({key for key, _ in rows}) != EXPECTED_ROWS:
        raise AssertionError(f"{path}: expected {EXPECTED_ROWS} unique rows")
    return rows


def read_utf16le(path: Path, *, expect_crlf: bool) -> tuple[bytes, list[tuple[str, str]]]:
    data = path.read_bytes()
    if not data.startswith(codecs.BOM_UTF16_LE):
        raise AssertionError(f"{path}: missing UTF-16LE BOM")
    return data, parse_rows(data[2:].decode("utf-16le"), path, expect_crlf=expect_crlf)


def verify_manifest() -> int:
    checked = 0
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), start=1):
        if "  " not in line:
            raise AssertionError(f"{MANIFEST}: malformed line {number}")
        expected, relative = line.split("  ", maxsplit=1)
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents or digest(path.read_bytes()) != expected:
            raise AssertionError(f"{MANIFEST}: mismatched or unsafe entry {relative}")
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="active PROTEUS Input Wait Menu_english.txt")
    args = parser.parse_args()

    review_rows = parse_rows(REVIEW_SOURCE.read_text(encoding="utf-8"), REVIEW_SOURCE, expect_crlf=False)
    asset_data, asset_rows = read_utf16le(TARGET, expect_crlf=True)
    if asset_rows != review_rows:
        raise AssertionError("game asset differs from translation-source.tsv")
    print(f"PASS game asset: {EXPECTED_ROWS} rows, UTF-16LE BOM, CRLF, no final newline, sha256={digest(asset_data)}")

    if args.source is not None:
        source_data, source_rows = read_utf16le(args.source, expect_crlf=True)
        if digest(source_data) != EXPECTED_UPSTREAM_SHA256:
            raise AssertionError("upstream source hash differs from active PROTEUS 3.4.0")
        if [key for key, _ in source_rows] != [key for key, _ in review_rows]:
            raise AssertionError("upstream key order differs from reviewable translation source")
        for number, ((_, english), (_, chinese)) in enumerate(zip(source_rows, review_rows), start=1):
            if TOKEN.findall(english) != TOKEN.findall(chinese):
                raise AssertionError(f"row {number}: placeholder or number token differs")
        print("PASS upstream parity: exact source hash, 80 keys/order, placeholders and numeric tokens")

    print(f"PASS manifest: {verify_manifest()} files match")
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
