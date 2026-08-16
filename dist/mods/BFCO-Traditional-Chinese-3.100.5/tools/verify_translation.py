#!/usr/bin/env python3
"""Verify format and 3.100.5 source parity for the BFCO Traditional Chinese override."""

from __future__ import annotations

import argparse
import codecs
import hashlib
import re
from pathlib import Path

from build_translation import EXPECTED_KEYS, EXPECTED_LINE_COUNT, read_review_source


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "Interface" / "Translations" / "SCSI-ACTbfco-Main_english.txt"
MANIFEST = ROOT / "MANIFEST.sha256"
EXPECTED_SOURCE_SHA256 = "58f76ec42ea6d36f1a6a59e1e040fe0bd54bfc640e9a45c7ebb57fc9f9a18abb"
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_game_file(path: Path) -> tuple[bytes, str, list[tuple[str, str]]]:
    data = path.read_bytes()
    if not data.startswith(codecs.BOM_UTF16_LE):
        raise AssertionError(f"{path}: missing UTF-16 LE BOM")
    body = data[len(codecs.BOM_UTF16_LE):]
    if len(body) % 2:
        raise AssertionError(f"{path}: odd UTF-16 LE payload")
    text = body.decode("utf-16-le")
    if "\x00" in text or "\r\n".join(text.split("\r\n")) != text:
        raise AssertionError(f"{path}: must use CRLF only")
    lines = text.split("\r\n")
    if len(lines) != EXPECTED_LINE_COUNT:
        raise AssertionError(f"{path}: expected {EXPECTED_LINE_COUNT} logical lines, got {len(lines)}")
    rows = [line.split("\t", 1) for line in lines if line]
    if any(line.count("\t") != 1 for line in lines if line):
        raise AssertionError(f"{path}: each nonblank row needs exactly one tab")
    if any(len(row) != 2 or not row[0] or not row[1] for row in rows):
        raise AssertionError(f"{path}: malformed nonblank row")
    return data, text, [(key, value) for key, value in rows]


def verify_manifest() -> int:
    checked = 0
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if "  " not in line:
            raise AssertionError(f"manifest line {number}: malformed")
        expected, relative = line.split("  ", 1)
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents or sha256(path.read_bytes()) != expected:
            raise AssertionError(f"manifest line {number}: checksum mismatch for {relative}")
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="the installed BFCO 3.100.5 ENGLISH file")
    args = parser.parse_args()

    review_text = read_review_source()
    review_lines = review_text.split("\n")
    target_data, target_text, target_rows = parse_game_file(TARGET)
    if target_text != review_text.replace("\n", "\r\n"):
        raise AssertionError("game asset differs from reviewable source")
    if tuple(key for key, _ in target_rows) != EXPECTED_KEYS:
        raise AssertionError("game asset keys or order differ from BFCO 3.100.5")
    print(f"PASS review source and asset: {len(target_rows)} keys, UTF-16 LE BOM, CRLF")

    if args.source is not None:
        source_data, source_text, source_rows = parse_game_file(args.source)
        if sha256(source_data) != EXPECTED_SOURCE_SHA256:
            raise AssertionError("source checksum is not the approved 3.100.5 baseline")
        if tuple(key for key, _ in source_rows) != EXPECTED_KEYS:
            raise AssertionError("source keys or order differ from BFCO 3.100.5")
        if [bool(line) for line in source_text.split("\r\n")] != [bool(line) for line in review_lines]:
            raise AssertionError("source blank-line layout differs from review source")
        if [CJK.sub("", value) for _, value in source_rows] != [CJK.sub("", value) for _, value in target_rows]:
            raise AssertionError("a non-CJK format token changed")
        print("PASS upstream parity: approved hash, keys, blank lines, and non-CJK tokens")

    print(f"PASS manifest: {verify_manifest()} files match")
    print(f"RESULT: PASS ({sha256(target_data)})")


if __name__ == "__main__":
    main()
