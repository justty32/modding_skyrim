#!/usr/bin/env python3
"""Build an exact AI Overhaul 1.9 NPC-name overlay from installed CHT core strings."""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PARSER = REPO / "dist/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/tools/translation_pipeline.py"
OVERLAY = REPO / "scripts/inline_translation_overlay.py"
OUTPUT = ROOT / "AI Overhaul.esp"
LEDGER = ROOT / "tools/name-translation-source.json"
MANIFEST = ROOT / "MANIFEST.sha256"
SOURCE_SHA256 = "8296a6ad435f6e31a74f24dd91444fa777c24a3a77a8c4989d9a8738db42a3ef"
EXPECTED_RECORDS = 3265
EXPECTED_NPC_NAMES = 424
EXPECTED_TRANSLATED_NAMES = 423
MASTER_SPECS = {
    0: ("Skyrim.esm", "Skyrim_English.STRINGS",
        "2bbc77fdec35a70ef96b710f8c525e50a1db9e63e11a391a0eb9ee8f56d36107",
        "ae1cd52056ab4b06e44a30a6e0509feeea4f0ddfd186cc5027b6c5af53a14ef4"),
    2: ("Dawnguard.esm", "Dawnguard_English.STRINGS",
        "1bda804009a21228acf6b30aa6aa7a692b247ff8a0313fe9aa69b3617ed4a6c4",
        "b9374779eacc52bc67782e559c51add595d6190b42e9052433d7d6cede62abdb"),
    3: ("HearthFires.esm", "Hearthfires_English.STRINGS",
        "ad4ca9f32c81e7ddd3e39ec95e03b07841f20712989e598778442ea69b6e6a97",
        "b1b2724c139024f3731bbb6a9595c81989502628c948db01bbbc3a9265a995b9"),
    4: ("Dragonborn.esm", "Dragonborn_English.STRINGS",
        "5f44f343552688c04f73bf83de58b90f70c7376b133fbbcb56b6fe33acf8778b",
        "7456c622f63406e69c65bccb702f495e90cf3bc9d8b7523ccdb187be3ac08c21"),
}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TP = load_module("aio_name_parser", PARSER)
OVERLAY_ENGINE = load_module("aio_name_overlay", OVERLAY)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def has_han(value: str) -> bool:
    return any("\u3400" <= char <= "\u9fff" for char in value)


def parse_strings(path: Path) -> dict[int, str]:
    data = path.read_bytes()
    if len(data) < 8:
        raise AssertionError(f"truncated STRINGS header: {path}")
    count, data_size = struct.unpack_from("<II", data, 0)
    data_start = 8 + count * 8
    if data_start + data_size != len(data):
        raise AssertionError(f"STRINGS size mismatch: {path}")
    result = {}
    for index in range(count):
        string_id, offset = struct.unpack_from("<II", data, 8 + index * 8)
        start = data_start + offset
        end = data.find(b"\0", start)
        if end < 0:
            raise AssertionError(f"unterminated STRINGS value: {string_id}")
        result[string_id] = data[start:end].decode("utf-8")
    return result


def build_rows(source: bytes, game_data: Path, cht_strings: Path) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    records = TP.iter_records(source)
    if len(records) != EXPECTED_RECORDS:
        raise AssertionError(f"unexpected AI Overhaul record count: {len(records)}")

    candidates: dict[int, list[tuple[object, int, str]]] = collections.defaultdict(list)
    skipped = []
    for record in records:
        if record.signature != b"NPC_":
            continue
        for subrecord_index, subrecord in enumerate(record.subrecords):
            if subrecord.tag != b"FULL":
                continue
            source_text = TP.canonical_zstring(subrecord.payload, "cp1252")
            master_index = record.raw_form_id >> 24
            if master_index not in MASTER_SPECS:
                skipped.append({
                    "raw_form_id": f"{record.raw_form_id:08X}",
                    "source": source_text,
                    "reason": "no installed authoritative CHT core STRINGS source",
                })
            else:
                candidates[master_index].append((record, subrecord_index, source_text))

    if sum(len(items) for items in candidates.values()) + len(skipped) != EXPECTED_NPC_NAMES:
        raise AssertionError("unexpected NPC FULL field count")

    rows = []
    for master_index, items in sorted(candidates.items()):
        plugin_name, strings_name, plugin_hash, strings_hash = MASTER_SPECS[master_index]
        plugin_path = game_data / plugin_name
        strings_path = cht_strings / strings_name
        if sha256(plugin_path) != plugin_hash:
            raise AssertionError(f"master hash mismatch: {plugin_name}")
        if sha256(strings_path) != strings_hash:
            raise AssertionError(f"CHT STRINGS hash mismatch: {strings_name}")

        wanted = {record.raw_form_id & 0xFFFFFF for record, _, _ in items}
        master_records: dict[int, object] = {}
        for record in TP.iter_records(plugin_path.read_bytes()):
            local_id = record.raw_form_id & 0xFFFFFF
            if record.signature != b"NPC_" or local_id not in wanted:
                continue
            if local_id in master_records:
                raise AssertionError(f"ambiguous master NPC local FormID: {local_id:06X}")
            master_records[local_id] = record
        table = parse_strings(strings_path)

        for record, subrecord_index, source_text in items:
            local_id = record.raw_form_id & 0xFFFFFF
            master_record = master_records.get(local_id)
            if master_record is None:
                raise AssertionError(f"master NPC absent: {record.raw_form_id:08X}")
            full = next((sub for sub in master_record.subrecords if sub.tag == b"FULL"), None)
            if full is None or len(full.payload) != 4:
                raise AssertionError(f"master NPC FULL is not localized: {record.raw_form_id:08X}")
            string_id = struct.unpack("<I", full.payload)[0]
            target = table.get(string_id)
            if not target or not has_han(target) or "\ufffd" in target:
                raise AssertionError(f"invalid CHT NPC name: {record.raw_form_id:08X}")
            if target == source_text:
                raise AssertionError(f"unexpected already-translated NPC name: {record.raw_form_id:08X}")
            rows.append({
                "identity": f"NPC_:{record.raw_form_id:08X}:FULL:0",
                "signature": "NPC_",
                "raw_form_id": f"{record.raw_form_id:08X}",
                "tag": "FULL",
                "tag_occurrence": 0,
                "source_subrecord_index": subrecord_index,
                "source": source_text,
                "target": target,
                "master": plugin_name,
                "master_string_id": string_id,
                "provenance": f"Skyrim Traditional Chinese 8.20 Core and Fonts/{strings_name}",
            })

    if len(rows) != EXPECTED_TRANSLATED_NAMES or len(skipped) != 1:
        raise AssertionError(f"unexpected coverage: translated={len(rows)} skipped={len(skipped)}")
    return rows, skipped


def prepare(source_path: Path, game_data: Path, cht_strings: Path):
    source = source_path.read_bytes()
    if sha256_bytes(source) != SOURCE_SHA256:
        raise AssertionError("installed AI Overhaul 1.9 source hash mismatch")
    rows, skipped = build_rows(source, game_data, cht_strings)
    output = OVERLAY_ENGINE.transform_plugin(source, rows)
    OVERLAY_ENGINE.verify_overlay(source, output, rows)
    ledger = {
        "schema": 1,
        "source": {
            "plugin": str(source_path),
            "plugin_sha256": SOURCE_SHA256,
            "cht_release": "Skyrim Traditional Chinese 8.20 Core and Fonts",
        },
        "translated": rows,
        "skipped": skipped,
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
    output, ledger = prepare(args.source, args.game_data, args.cht_strings)
    OUTPUT.write_bytes(output)
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_manifest()
    print(f"built: {len(ledger['translated'])} translated NPC names; {len(ledger['skipped'])} explicitly skipped")


def verify(args: argparse.Namespace) -> None:
    output, ledger = prepare(args.source, args.game_data, args.cht_strings)
    if OUTPUT.read_bytes() != output:
        raise AssertionError("packaged AI Overhaul ESP is not reproducible")
    if json.loads(LEDGER.read_text(encoding="utf-8")) != ledger:
        raise AssertionError("packaged translation ledger differs")
    verify_manifest()
    print("PASS: 3,265 records preserved; only 423 NPC_ FULL fields changed")
    print("PASS: all non-name payloads are byte-identical; one Fishing NPC is explicitly untranslated")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--game-data", type=Path, required=True)
    parser.add_argument("--cht-strings", type=Path, required=True)
    args = parser.parse_args()
    try:
        (build if args.command == "build" else verify)(args)
    except (AssertionError, OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
