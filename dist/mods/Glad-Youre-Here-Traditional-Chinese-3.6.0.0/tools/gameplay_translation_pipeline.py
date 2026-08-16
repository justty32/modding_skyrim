#!/usr/bin/env python3
"""Build a version-locked GYH 3.6.0 text overlay from the reviewed 3.2.3 CHS seed."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
ENGINE_PATH = REPO / "scripts/inline_translation_overlay.py"
OUTPUT = ROOT / "ImGladYoureHere.esp"
LEDGER = ROOT / "tools/gameplay-translation-source.json"
MANIFEST = ROOT / "MANIFEST.sha256"
SOURCE_SHA256 = "799c725c1ac53466cd00747fa9940f35e48646b42dc955c5e8a42d3d1ad40199"
SEED_SHA256 = "1335bba1c37ac8c96345aa930ba48e13f9fc2bcca7c6c2ea227f4241770cf94e"
SEED_ARCHIVE_SHA256 = "2a19d83ac9a92336222643f149dc82bf5138a70c85396508a9011f47dd65c21f"
EXPECTED_FIELDS = 828
MANUAL = {
    ("DIAL", 0x05000D64, "FULL", 0): "很高興你在這裡。",
    ("DIAL", 0x0502DBF5, "FULL", 0): "很高興你在這裡。",
}


def load_engine():
    spec = importlib.util.spec_from_file_location("gyh_inline_translation", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load inline translation engine")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ENGINE = load_engine()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def prepare(source_path: Path, seed_path: Path):
    source = source_path.read_bytes()
    seed = seed_path.read_bytes()
    if sha256_bytes(source) != SOURCE_SHA256:
        raise AssertionError("Glad You're Here 3.6.0 source hash mismatch")
    if sha256_bytes(seed) != SEED_SHA256:
        raise AssertionError("Glad You're Here 3.2.3 CHS seed hash mismatch")
    rows = ENGINE.collect_seed_rows(
        source, seed,
        provenance="Glad You're Here CHS 3.2.3 (Nexus 82669) matched into exact 3.6.0 source",
        manual=MANUAL,
    )
    if len(rows) != EXPECTED_FIELDS:
        raise AssertionError(f"unexpected translated field count: {len(rows)}")
    output = ENGINE.transform_plugin(source, rows)
    ENGINE.verify_overlay(source, output, rows)
    ledger = {
        "schema": 1,
        "source": {
            "official_3_6_0_esp_sha256": SOURCE_SHA256,
            "chs_3_2_3_seed_esp_sha256": SEED_SHA256,
            "chs_3_2_3_seed_archive_sha256": SEED_ARCHIVE_SHA256,
        },
        "coverage": {
            "current_records": 1211,
            "seed_records": 1091,
            "translated_fields": EXPECTED_FIELDS,
            "boundary": "Only stable record FormID + localizable tag occurrence matches; newer unmatched 3.6.0 text remains unchanged.",
        },
        "plugin": rows,
    }
    return output, ledger


def artifact_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and path != MANIFEST and "__pycache__" not in path.parts)


def write_manifest() -> None:
    MANIFEST.write_text("".join(f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}\n" for path in artifact_files()), encoding="utf-8")


def verify_manifest() -> None:
    listed = set()
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        if sha256(ROOT / relative) != digest:
            raise AssertionError(f"manifest mismatch: {relative}")
        listed.add(relative)
    actual = {path.relative_to(ROOT).as_posix() for path in artifact_files()}
    if listed != actual:
        raise AssertionError(f"manifest coverage mismatch: {sorted(listed ^ actual)}")


def build(args: argparse.Namespace) -> None:
    output, ledger = prepare(args.source, args.seed)
    OUTPUT.write_bytes(output)
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_manifest()
    print(f"built GYH 3.6.0 overlay: {len(ledger['plugin'])} translated fields")


def verify(args: argparse.Namespace) -> None:
    output, ledger = prepare(args.source, args.seed)
    if OUTPUT.read_bytes() != output:
        raise AssertionError("packaged GYH ESP differs from fresh rebuild")
    if json.loads(LEDGER.read_text(encoding="utf-8")) != ledger:
        raise AssertionError("packaged GYH ledger differs")
    verify_manifest()
    print(f"PASS: 1,211 current records preserved; {len(ledger['plugin'])} matched text fields translated; every nontext payload unchanged")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    args = parser.parse_args()
    try:
        (build if args.command == "build" else verify)(args)
    except (AssertionError, OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
