#!/usr/bin/env python3
"""Verify the TrueHUD Traditional Chinese text-only override."""

from __future__ import annotations

import argparse
import codecs
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "Interface" / "Translations" / "TrueHUD_english.txt"
MANIFEST = ROOT / "MANIFEST.sha256"
SOURCE_SHA256 = "01d296193388d2c22662e407349940ce99efd69be201730a6b61ac6af2dc936a"


def read(path: Path) -> tuple[bytes, list[str]]:
    data = path.read_bytes()
    if not data.startswith(codecs.BOM_UTF16_LE):
        raise AssertionError(f"{path}: missing UTF-16 LE BOM")
    body = data[2:]
    if len(body) % 2:
        raise AssertionError(f"{path}: odd UTF-16 LE byte count")
    text = body.decode("utf-16-le")
    if "\n" in text.replace("\r\n", "") or "\r" in text.replace("\r\n", ""):
        raise AssertionError(f"{path}: non-CRLF terminator")
    return data, text.split("\r\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True, help="active TrueHUD_english.txt")
    args = parser.parse_args()
    source_bytes, source_lines = read(args.source)
    target_bytes, target_lines = read(TARGET)
    if hashlib.sha256(source_bytes).hexdigest() != SOURCE_SHA256:
        raise AssertionError("source SHA-256 does not match active d2026.4.12.0")
    if len(source_lines) != len(target_lines):
        raise AssertionError("line count differs from source")
    records = 0
    for number, (source, target) in enumerate(zip(source_lines, target_lines), 1):
        if bool(source) != bool(target):
            raise AssertionError(f"line {number}: blank-line layout differs")
        if not source:
            continue
        if source.count("\t") != 1 or target.count("\t") != 1:
            raise AssertionError(f"line {number}: each record needs one tab")
        source_key, source_value = source.split("\t")
        target_key, target_value = target.split("\t")
        if source_key != target_key:
            raise AssertionError(f"line {number}: key/order differs")
        if re.findall(r"<[^>]+>", source_value) != re.findall(r"<[^>]+>", target_value):
            raise AssertionError(f"line {number}: XML/colour tokens differ")
        records += 1
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
            raise AssertionError(f"manifest mismatch: {relative}")
    print(f"PASS source parity: {records} keys, order, blank layout, XML/colour tokens")
    print(f"PASS encoding: UTF-16 LE BOM, CRLF, sha256={hashlib.sha256(target_bytes).hexdigest()}")
    print("PASS manifest")


if __name__ == "__main__":
    main()
