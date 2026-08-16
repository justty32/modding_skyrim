#!/usr/bin/env python3
"""Verify the NFF 2.8.6b Traditional Chinese text-only override."""

from __future__ import annotations

import argparse
import codecs
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = ROOT / "tools" / "translation-source.tsv"
TARGET = ROOT / "Interface" / "Translations" / "nwsFollowerFramework_english.txt"
MANIFEST = ROOT / "MANIFEST.sha256"
EXPECTED_UPSTREAM_SHA256 = "4a43027afafdd3654d6e17b5a7b5aac7e0f5469ac0743f6646d015d493f2fd2f"
EXPECTED_ROWS = 1398
MALFORMED_UPSTREAM = (
    "$FF_LootSpeedDS Speeds of movement of followers that are looting, "
    "which also can help speed up loot time."
)
NUMBER_RE = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?%?")
CONTROL_RE = re.compile(r"%(?:\d+\$)?[A-Za-z]|\\[nrt]|<[^>]+>|\{[^{}]+\}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_rows(lines: list[str], path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for number, line in enumerate(lines, start=1):
        if not line or line.startswith(";"):
            continue
        if line.count("\t") != 1:
            raise AssertionError(f"{path}: line {number} must contain exactly one tab")
        key, value = line.split("\t")
        if not key.startswith("$") or not value:
            raise AssertionError(f"{path}: line {number} has an invalid key or empty value")
        rows.append((key, value))
    if len(rows) != EXPECTED_ROWS:
        raise AssertionError(f"{path}: expected {EXPECTED_ROWS} rows, got {len(rows)}")
    if len({key for key, _ in rows}) != len(rows):
        raise AssertionError(f"{path}: duplicate translation key")
    return rows


def read_upstream(path: Path) -> tuple[bytes, list[tuple[str, str]]]:
    data = path.read_bytes()
    if digest(data) != EXPECTED_UPSTREAM_SHA256:
        raise AssertionError("upstream source hash differs from NFF 2.8.6b")
    if not data.startswith(codecs.BOM_UTF16_LE):
        raise AssertionError(f"{path}: missing UTF-16 LE BOM")
    lines = data[2:].decode("utf-16-le").splitlines()
    malformed = [line for line in lines if line == MALFORMED_UPSTREAM]
    if len(malformed) != 1:
        raise AssertionError("expected the one known upstream missing-tab line")
    lines[lines.index(MALFORMED_UPSTREAM)] = MALFORMED_UPSTREAM.replace(" ", "\t", 1)
    return data, parse_rows(lines, path)


def read_game_asset(path: Path) -> tuple[bytes, list[tuple[str, str]]]:
    data = path.read_bytes()
    if not data.startswith(codecs.BOM_UTF16_LE):
        raise AssertionError(f"{path}: missing UTF-16 LE BOM")
    text = data[2:].decode("utf-16-le")
    if not text.endswith("\r\n") or text.replace("\r\n", "").count("\n"):
        raise AssertionError(f"{path}: expected CRLF after every record")
    return data, parse_rows(text.splitlines(), path)


def protected_tokens(value: str) -> tuple[list[str], list[str]]:
    return NUMBER_RE.findall(value), CONTROL_RE.findall(value)


def verify_manifest() -> int:
    checked = 0
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), start=1):
        if "  " not in line:
            raise AssertionError(f"{MANIFEST}: malformed line {number}")
        expected, relative = line.split("  ", maxsplit=1)
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents or not path.is_file() or digest(path.read_bytes()) != expected:
            raise AssertionError(f"{MANIFEST}: mismatched or unsafe entry {relative}")
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path, help="NFF 2.8.6b English translation file")
    args = parser.parse_args()

    review_rows = parse_rows(REVIEW_SOURCE.read_text(encoding="utf-8").splitlines(), REVIEW_SOURCE)
    game_data, game_rows = read_game_asset(TARGET)
    if game_rows != review_rows:
        raise AssertionError("game asset differs from translation-source.tsv")
    print(f"PASS game asset: {EXPECTED_ROWS} rows, UTF-16 LE BOM, CRLF, sha256={digest(game_data)}")

    _, upstream_rows = read_upstream(args.source)
    if [key for key, _ in upstream_rows] != [key for key, _ in review_rows]:
        raise AssertionError("upstream key order differs from reviewable translation source")
    for number, ((key, source_value), (_, target_value)) in enumerate(
        zip(upstream_rows, review_rows), start=1
    ):
        if protected_tokens(source_value) != protected_tokens(target_value):
            raise AssertionError(f"row {number} ({key}): protected number/control tokens differ")
    print("PASS upstream parity: exact hash, key/order parity, numbers and control tokens")
    print("PASS upstream repair: restored missing tab for $FF_LootSpeedDS")

    print(f"PASS manifest: {verify_manifest()} files match")
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
