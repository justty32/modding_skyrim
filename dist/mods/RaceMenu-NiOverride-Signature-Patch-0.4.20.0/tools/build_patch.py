#!/usr/bin/env python3
"""Build the exact RaceMenu 0.4.20.0 NiOverride signature patch."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import tempfile


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "Scripts" / "NiOverride.pex"
SOURCE_SIZE = 12_935
SOURCE_SHA256 = "862d0e76173ebb2c790fccce2305c00ed5ea11a1f8e2dfc103ea296b2fbf8a0d"
OUTPUT_SHA256 = "d571109d7beea5b5bc7c0e2e6ca262789b4c4f77336cd90af4e84d83c44072f2"
RECORD_OFFSET = 10_536
EXPECTED_RECORD = bytes.fromhex("00 a3 00 d2")
PATCHED_RECORD = bytes.fromhex("00 a3 00 cc")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build(source: Path) -> bytes:
    data = bytearray(source.read_bytes())
    if len(data) != SOURCE_SIZE:
        raise AssertionError(f"source size {len(data)} != {SOURCE_SIZE}")
    source_hash = digest(data)
    if source_hash != SOURCE_SHA256:
        raise AssertionError(f"source sha256 {source_hash} != {SOURCE_SHA256}")
    if data[RECORD_OFFSET : RECORD_OFFSET + 4] != EXPECTED_RECORD:
        raise AssertionError(
            f"source bytes at {RECORD_OFFSET} do not match {EXPECTED_RECORD.hex(' ')}"
        )

    data[RECORD_OFFSET : RECORD_OFFSET + 4] = PATCHED_RECORD
    output = bytes(data)
    output_hash = digest(output)
    if len(output) != SOURCE_SIZE or output_hash != OUTPUT_SHA256:
        raise AssertionError(
            f"unexpected output contract: size={len(output)} sha256={output_hash}"
        )
    return output


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as tmp:
        temp_path = Path(tmp.name)
        tmp.write(data)
        tmp.flush()
        os.fsync(tmp.fileno())
    try:
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing non-canonical output",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    if source == output:
        raise AssertionError("source and output paths must differ")
    if output.exists() and digest(output.read_bytes()) != OUTPUT_SHA256 and not args.force:
        raise FileExistsError(
            f"refusing to replace non-canonical output {output}; pass --force explicitly"
        )

    patched = build(source)
    atomic_write(output, patched)
    print(
        f"PASS wrote {output}: {len(patched)} bytes, sha256={digest(patched)}, "
        "one guarded return-type index patch"
    )


if __name__ == "__main__":
    main()
