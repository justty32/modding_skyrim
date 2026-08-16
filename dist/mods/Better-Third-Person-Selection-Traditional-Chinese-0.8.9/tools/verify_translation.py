#!/usr/bin/env python3
"""Verify the review source, generated asset, and optional upstream 0.8.9 file."""

import argparse
import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = ROOT / "tools" / "translation-source.tsv"
ASSET = ROOT / "Interface" / "Translations" / "BetterThirdPersonSelection_ENGLISH.txt"
EXPECTED_UPSTREAM_SHA256 = "00488ab50628c75740c61fb4345a64f66ae99957df9298009e2e3beb11bc365d"
# These literals are consumed as UI placeholders or configuration notation. Keep
# their exact sequence while allowing the surrounding prose to be translated.
PRESERVED_TOKEN = re.compile(r"\[[^\]]+\]|\b\d+(?:\.\d+)?\b|\*")


def fail(message: str) -> None:
    raise ValueError(message)


def parse_tsv(path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    seen: set[str] = set()
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        if line.count("\t") != 1:
            fail(f"{path}:{number}: expected exactly one tab")
        key, value = line.split("\t")
        if not key.startswith("$") or not value:
            fail(f"{path}:{number}: expected non-empty $key and translation")
        if key in seen:
            fail(f"{path}:{number}: duplicate key {key}")
        seen.add(key)
        rows.append((key, value))
    return rows


def parse_translation(path: Path) -> tuple[list[tuple[str, str]], bytes]:
    raw = path.read_bytes()
    if not raw.startswith(b"\xff\xfe"):
        fail(f"{path}: missing UTF-16LE BOM")
    if raw[2:].startswith(b"\xfe\xff"):
        fail(f"{path}: unexpected UTF-16BE BOM")
    text = raw[2:].decode("utf-16le")
    if "\n" in text.replace("\r\n", "") or "\r" in text.replace("\r\n", ""):
        fail(f"{path}: line endings are not exclusively CRLF")
    if text.endswith("\r\n"):
        fail(f"{path}: unexpected final newline")
    rows: list[tuple[str, str]] = []
    for number, line in enumerate(text.split("\r\n"), 1):
        if line.count("\t") != 1:
            fail(f"{path}:{number}: expected exactly one tab")
        key, value = line.split("\t")
        if not key.startswith("$") or not value:
            fail(f"{path}:{number}: expected non-empty $key and translation")
        rows.append((key, value))
    return rows, raw


def parse_upstream(path: Path) -> tuple[list[tuple[str, str]], bytes]:
    raw = path.read_bytes()
    if not raw.startswith(b"\xff\xfe"):
        fail(f"{path}: upstream file lacks UTF-16LE BOM")
    text = raw[2:].decode("utf-16le")
    rows = []
    for line in text.split("\r\n"):
        if not line:
            continue
        if line.count("\t") != 1:
            fail(f"{path}: malformed upstream row {line!r}")
        rows.append(tuple(line.split("\t")))
    return rows, raw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, help="active BetterThirdPersonSelection_english.txt from 0.8.9")
    args = parser.parse_args()
    review = parse_tsv(REVIEW_SOURCE)
    asset, raw = parse_translation(ASSET)
    if asset != review:
        fail("generated asset rows differ from reviewable TSV")
    print(f"PASS reviewable source: UTF-8, {len(review)} unique keys, exact asset order")
    print("PASS game asset: UTF-16LE BOM, CRLF, no final newline, "
          f"{len(asset)} exact rows, sha256={hashlib.sha256(raw).hexdigest()}")
    if args.source:
        upstream, upstream_raw = parse_upstream(args.source)
        actual_hash = hashlib.sha256(upstream_raw).hexdigest()
        if actual_hash != EXPECTED_UPSTREAM_SHA256:
            fail(f"upstream SHA-256 differs: {actual_hash}")
        upstream_keys = [key for key, _ in upstream]
        asset_keys = [key for key, _ in asset]
        if asset_keys != upstream_keys:
            fail("key list or order differs from active 0.8.9 English source")
        for (key, english), (_, chinese) in zip(upstream, asset):
            if PRESERVED_TOKEN.findall(english) != PRESERVED_TOKEN.findall(chinese):
                fail("placeholder/token differs for key " + key)
        print("PASS upstream parity: exact 0.8.9 source hash, all keys/order, placeholders/tokens")
    else:
        print("SKIP upstream parity: pass --source /path/to/BetterThirdPersonSelection_english.txt")
    print("RESULT: PASS")


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
