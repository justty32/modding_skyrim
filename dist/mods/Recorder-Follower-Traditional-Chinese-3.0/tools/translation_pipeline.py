#!/usr/bin/env python3
"""Rebuild and verify the exact-version Recorder 3.0 Traditional Chinese overlay."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ARTIFACT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
SHARED = REPO / "scripts/inline_translation_overlay.py"
SOURCE_SHA256 = "85c36c5e264980e4f2b7e0913c4647b24b4351e7cea4f3c431d4cb3d3f8c58ca"
SEED_SHA256 = "865e3af606c9ca517a517abf7ca9e791d8939f70d06ad4acf5a2a0a529d47ced"
PLUGIN_NAME = "Recorder Follower Base.esp"
EXPECTED_RECORDS = 1380
EXPECTED_ROWS = 1429


def load_shared():
    spec = importlib.util.spec_from_file_location("recorder_inline_overlay", SHARED)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load shared pipeline: {SHARED}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


OV = load_shared()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_inputs(source_path: Path, seed_path: Path) -> tuple[bytes, bytes]:
    source = source_path.read_bytes()
    seed = seed_path.read_bytes()
    if sha256(source) != SOURCE_SHA256:
        raise AssertionError(f"unexpected source SHA-256: {sha256(source)}")
    if sha256(seed) != SEED_SHA256:
        raise AssertionError(f"unexpected seed SHA-256: {sha256(seed)}")
    return source, seed


def build_rows(source: bytes, seed: bytes) -> list[dict[str, object]]:
    rows = OV.collect_seed_rows(
        source,
        seed,
        provenance="Recorder Follower Base CHT 3.0; OpenCC s2tw character normalization",
        converter="s2tw",
    )
    if len(rows) != EXPECTED_ROWS:
        raise AssertionError(f"translation coverage changed: {len(rows)} != {EXPECTED_ROWS}")
    return rows


def verify_seed_scope(source: bytes, seed: bytes) -> None:
    left = OV.TP.iter_records(source)
    right = OV.TP.iter_records(seed)
    if len(left) != EXPECTED_RECORDS or len(right) != EXPECTED_RECORDS:
        raise AssertionError("record count changed")
    changed = 0
    for a, b in zip(left, right):
        if (a.signature, a.raw_form_id, a.path) != (b.signature, b.raw_form_id, b.path):
            raise AssertionError("seed record identity/order/group path changed")
        if OV.TP.semantic_header(a.header) != OV.TP.semantic_header(b.header):
            raise AssertionError(f"seed semantic header changed: {a.raw_form_id:08X}")
        if [item.tag for item in a.subrecords] != [item.tag for item in b.subrecords]:
            raise AssertionError(f"seed subrecord topology changed: {a.raw_form_id:08X}")
        for x, y in zip(a.subrecords, b.subrecords):
            if x.payload == y.payload:
                continue
            if x.tag not in OV.LOCALIZABLE_TAGS:
                raise AssertionError(
                    f"seed non-text payload changed: {a.signature.decode()}:{a.raw_form_id:08X}:{x.tag.decode()}"
                )
            changed += 1
    if changed != EXPECTED_ROWS:
        raise AssertionError(f"seed delta count changed: {changed} != {EXPECTED_ROWS}")


def ledger(rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "schema": 1,
        "plugin": PLUGIN_NAME,
        "source_sha256": SOURCE_SHA256,
        "seed_sha256": SEED_SHA256,
        "field_count": len(rows),
        "fields": rows,
    }


def render_ledger(rows: list[dict[str, object]]) -> bytes:
    return (json.dumps(ledger(rows), ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def run_build(source_path: Path, seed_path: Path) -> None:
    source, seed = load_inputs(source_path, seed_path)
    verify_seed_scope(source, seed)
    rows = build_rows(source, seed)
    output = OV.transform_plugin(source, rows)
    OV.verify_overlay(source, output, rows)
    (ARTIFACT / PLUGIN_NAME).write_bytes(output)
    (ARTIFACT / "tools/translation-source.json").write_bytes(render_ledger(rows))
    print(f"built {PLUGIN_NAME}: {len(rows)} fields; sha256={sha256(output)}")


def run_verify(source_path: Path, seed_path: Path) -> None:
    source, seed = load_inputs(source_path, seed_path)
    verify_seed_scope(source, seed)
    rows = build_rows(source, seed)
    rebuilt = OV.transform_plugin(source, rows)
    packaged = (ARTIFACT / PLUGIN_NAME).read_bytes()
    packaged_ledger = (ARTIFACT / "tools/translation-source.json").read_bytes()
    OV.verify_overlay(source, packaged, rows)
    if packaged != rebuilt:
        raise AssertionError("packaged ESP differs from fresh rebuild")
    if packaged_ledger != render_ledger(rows):
        raise AssertionError("packaged ledger differs from fresh rebuild")
    print(
        f"PASS: {EXPECTED_RECORDS} records; {len(rows)} text fields; "
        f"all non-text payloads unchanged; sha256={sha256(packaged)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--source-esp", required=True, type=Path)
    parser.add_argument("--seed-esp", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "build":
        run_build(args.source_esp, args.seed_esp)
    else:
        run_verify(args.source_esp, args.seed_esp)


if __name__ == "__main__":
    main()
