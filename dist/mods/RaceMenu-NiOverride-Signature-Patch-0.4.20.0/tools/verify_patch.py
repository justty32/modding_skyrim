#!/usr/bin/env python3
"""Verify hashes, the guarded PEX record, one-byte source delta, and manifest."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "Scripts" / "NiOverride.pex"
MANIFEST = ROOT / "MANIFEST.sha256"
EXPECTED_SIZE = 12_935
SOURCE_SHA256 = "862d0e76173ebb2c790fccce2305c00ed5ea11a1f8e2dfc103ea296b2fbf8a0d"
OUTPUT_SHA256 = "d571109d7beea5b5bc7c0e2e6ca262789b4c4f77336cd90af4e84d83c44072f2"
RECORD_OFFSET = 10_536
CHANGED_OFFSET = 10_539
SOURCE_RECORD = bytes.fromhex("00 a3 00 d2")
OUTPUT_RECORD = bytes.fromhex("00 a3 00 cc")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_u16(data: bytes, pos: int) -> tuple[int, int]:
    if pos + 2 > len(data):
        raise AssertionError("truncated PEX u16")
    return int.from_bytes(data[pos : pos + 2], "big"), pos + 2


def read_pstring(data: bytes, pos: int) -> tuple[str, int]:
    size, pos = read_u16(data, pos)
    end = pos + size
    if end > len(data):
        raise AssertionError("truncated PEX string")
    return data[pos:end].decode("cp1252"), end


def parse_header_and_strings(data: bytes) -> list[str]:
    if data[:4] != bytes.fromhex("fa 57 c0 de"):
        raise AssertionError("invalid Skyrim PEX magic")
    if data[4:8] != bytes.fromhex("03 02 00 01"):
        raise AssertionError(f"unexpected PEX version/game header: {data[4:8].hex(' ')}")

    pos = 16
    source_name, pos = read_pstring(data, pos)
    _, pos = read_pstring(data, pos)
    _, pos = read_pstring(data, pos)
    if source_name != "NiOverride.psc":
        raise AssertionError(f"unexpected source name {source_name!r}")

    count, pos = read_u16(data, pos)
    strings: list[str] = []
    for _ in range(count):
        value, pos = read_pstring(data, pos)
        strings.append(value)
    if count != 263:
        raise AssertionError(f"string count {count} != 263")
    return strings


def verify_target() -> bytes:
    data = TARGET.read_bytes()
    actual_hash = digest(data)
    if len(data) != EXPECTED_SIZE:
        raise AssertionError(f"target size {len(data)} != {EXPECTED_SIZE}")
    if actual_hash != OUTPUT_SHA256:
        raise AssertionError(f"target sha256 {actual_hash} != {OUTPUT_SHA256}")

    strings = parse_header_and_strings(data)
    expected_indexes = {
        163: "GetNodeTransformScaleMode",
        204: "Int",
        210: "Float",
    }
    for index, expected in expected_indexes.items():
        if strings[index] != expected:
            raise AssertionError(
                f"PEX string #{index} is {strings[index]!r}, expected {expected!r}"
            )
    if data[RECORD_OFFSET : RECORD_OFFSET + 4] != OUTPUT_RECORD:
        raise AssertionError("patched function-name/return-type record does not match")
    if data.count(OUTPUT_RECORD) != 1:
        raise AssertionError("patched function record must occur exactly once")
    print(
        "PASS output: exact size/hash, Skyrim PEX header, 263-string table, "
        "unique GetNodeTransformScaleMode -> Int record"
    )
    return data


def verify_source(source: Path, target: bytes) -> None:
    original = source.read_bytes()
    source_hash = digest(original)
    if len(original) != EXPECTED_SIZE or source_hash != SOURCE_SHA256:
        raise AssertionError(
            f"source contract mismatch: size={len(original)} sha256={source_hash}"
        )
    if original[RECORD_OFFSET : RECORD_OFFSET + 4] != SOURCE_RECORD:
        raise AssertionError("source function-name/return-type record does not match")
    changed = [index for index, pair in enumerate(zip(original, target)) if pair[0] != pair[1]]
    if changed != [CHANGED_OFFSET]:
        raise AssertionError(f"binary delta is {changed}, expected [{CHANGED_OFFSET}]")
    if original[CHANGED_OFFSET] != 0xD2 or target[CHANGED_OFFSET] != 0xCC:
        raise AssertionError("changed byte is not D2 -> CC")
    print("PASS source delta: exact upstream hash and exactly offset 10539 D2 -> CC")


def verify_manifest() -> int:
    checked = 0
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), start=1):
        if "  " not in line:
            raise AssertionError(f"{MANIFEST}: malformed line {number}")
        expected, relative = line.split("  ", maxsplit=1)
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents:
            raise AssertionError(f"{MANIFEST}: unsafe path on line {number}")
        actual = digest(path.read_bytes())
        if actual != expected:
            raise AssertionError(f"{relative}: sha256 {actual} != {expected}")
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        help="optional exact official 0.4.20.0 NiOverride.pex for one-byte delta proof",
    )
    args = parser.parse_args()

    target = verify_target()
    if args.source is not None:
        verify_source(args.source, target)
    if MANIFEST.exists():
        print(f"PASS manifest: {verify_manifest()} files match")
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
