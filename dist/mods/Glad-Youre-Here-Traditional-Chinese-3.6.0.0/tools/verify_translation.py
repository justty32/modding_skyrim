#!/usr/bin/env python3
"""Verify the Glad You're Here 3.6.0.0 Traditional Chinese override."""

from __future__ import annotations

import argparse
import codecs
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "interface" / "translations" / "ImGladYoureHere_english.txt"
MANIFEST = ROOT / "MANIFEST.sha256"
EXPECTED_UPSTREAM_SHA256 = "a28b0f834f8db92de2a4cccc28bd41350a5d471ac90f2f782b039f33b7e3ae1c"
EXPECTED_ROWS = 213


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows_from_text(text: str, path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if line.count("\t") != 1:
            raise AssertionError(f"{path}: line {number} must contain exactly one tab")
        key, value = line.split("\t")
        if not key or not value:
            raise AssertionError(f"{path}: line {number} has an empty key or value")
        rows.append((key, value))
    if len(rows) != EXPECTED_ROWS:
        raise AssertionError(f"{path}: expected {EXPECTED_ROWS} rows, got {len(rows)}")
    if len({key for key, _ in rows}) != len(rows):
        raise AssertionError(f"{path}: duplicate translation key")
    return rows


def read_upstream(path: Path) -> tuple[bytes, list[tuple[str, str]]]:
    data = path.read_bytes()
    if not data.startswith(codecs.BOM_UTF16_LE):
        raise AssertionError(f"{path}: missing UTF-16 LE BOM")
    return data, rows_from_text(data[2:].decode("utf-16-le"), path)


def read_game_asset(path: Path) -> tuple[bytes, list[tuple[str, str]]]:
    data = path.read_bytes()
    if not data.startswith(codecs.BOM_UTF16_LE):
        raise AssertionError(f"{path}: missing UTF-16 LE BOM")
    text = data[2:].decode("utf-16-le")
    if not text.endswith("\r\n") or text.replace("\r\n", "").count("\n"):
        raise AssertionError(f"{path}: expected CRLF after every record")
    return data, rows_from_text(text, path)


def protected_tokens(value: str) -> tuple[int, int]:
    """Tokens used by the current source as format controls, not translatable prose."""
    return value.count("%"), value.count("\\n")


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
    parser.add_argument("--source", type=Path, help="current upstream ImGladYoureHere_english.txt")
    args = parser.parse_args()

    review_rows = rows_from_text(REVIEW_SOURCE.read_text(encoding="utf-8"), REVIEW_SOURCE)
    game_data, game_rows = read_game_asset(TARGET)
    if game_rows != review_rows:
        raise AssertionError("game asset differs from translation-source.tsv")
    print(f"PASS game asset: 213 rows, UTF-16 LE BOM, CRLF, sha256={digest(game_data)}")

    if args.source is not None:
        source_data, source_rows = read_upstream(args.source)
        if digest(source_data) != EXPECTED_UPSTREAM_SHA256:
            raise AssertionError("upstream source hash differs from Modpack-KR-Dev 3.6.0.0")
        if [key for key, _ in source_rows] != [key for key, _ in review_rows]:
            raise AssertionError("upstream key order differs from reviewable translation source")
        for number, ((_, source_value), (_, target_value)) in enumerate(zip(source_rows, review_rows), start=1):
            if protected_tokens(source_value) != protected_tokens(target_value):
                raise AssertionError(f"row {number}: protected % or \\n token count differs")
        print("PASS upstream parity: exact source hash, 213 keys/order, % and \\n tokens")

    print(f"PASS manifest: {verify_manifest()} files match")
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
