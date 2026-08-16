#!/usr/bin/env python3
"""Build the reviewed USSEP PERK translation ledger from record-identity matches.

The 8.20 translation files use the English filename too because the live profile
has ``sLanguage=ENGLISH``.  Matching therefore happens by FormKey and subrecord
string id, never by fuzzy English text.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import struct
import zlib

from plugin_localizer import (
    EXPECTED_FIELDS,
    EXPECTED_RECORDS,
    SOURCE_SHA256,
    USSEP_NAME,
    decode_strings,
    decode_zstring,
    form_key,
    iter_records,
    parse_subrecords,
    sha256,
    tes4_masters,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tools" / "translation-source.tsv"
COMPRESSED_FLAG = 0x00040000
SUPPORTED_OWNERS = {
    "Skyrim.esm": "Skyrim",
    "Dawnguard.esm": "Dawnguard",
    "Dragonborn.esm": "Dragonborn",
    "ccbgssse037-curios.esl": "ccBGSSSE037-Curios",
}
CONSTELLATIONS_WINNERS = {
    "0E5F46:Skyrim.esm",
    "0E5F4A:Skyrim.esm",
}

# Only fields where USSEP changed the visible meaning/numbers, or the 8.20
# record-matched target is still English/incorrect, are overridden by hand.
OVERRIDES = {
    ("052190:Skyrim.esm", "DESC"): "可在鍛造爐製作龍系護具與龍骨武器，並將其強化兩倍。",
    ("0581DD:Skyrim.esm", "DESC"): "復生或召喚的不死生物持續時間更長。",
    ("058F79:Skyrim.esm", "DESC"): "可以向任何商人出售贓物。",
    ("103ADA:Skyrim.esm", "DESC"): "張弓切入瞄準時，時間減慢 50%。",
    ("103ADB:Skyrim.esm", "DESC"): "張弓切入瞄準時，時間減慢 75%。",
    ("105F2E:Skyrim.esm", "DESC"): "從可採集的材料來源取得兩份材料。",
    ("0250E8:Dragonborn.esm", "FULL"): "度坎之怒",
    ("0250E9:Dragonborn.esm", "FULL"): "薩克里斯之怒",
    ("0CF788:Skyrim.esm", "DESC"): "用於套用天賦技能增益的統一天賦。",
    ("017740:Dragonborn.esm", "FULL"): "NPC 結界吸收",
    ("000854:ccbgssse037-curios.esl", "FULL"): "銀矢特技",
    ("000854:ccbgssse037-curios.esl", "DESC"): "對狼人與不死生物造成銀製武器傷害。",
}
USSEP_SEMANTIC_FIELDS = {
    ("052190:Skyrim.esm", "DESC"),
    ("0581DD:Skyrim.esm", "DESC"),
    ("058F79:Skyrim.esm", "DESC"),
    ("103ADA:Skyrim.esm", "DESC"),
    ("103ADB:Skyrim.esm", "DESC"),
    ("105F2E:Skyrim.esm", "DESC"),
    ("0250E8:Dragonborn.esm", "FULL"),
    ("0250E9:Dragonborn.esm", "FULL"),
}


def find_case_insensitive(directory: Path, name: str) -> Path:
    matches = {path.name.casefold(): path for path in directory.iterdir() if path.is_file()}
    try:
        return matches[name.casefold()]
    except KeyError as exc:
        raise AssertionError(f"missing {name} under {directory}") from exc


def table(strings_dir: Path, stem: str, field: str) -> dict[int, str]:
    extension = "STRINGS" if field == "FULL" else "DLSTRINGS"
    path = find_case_insensitive(strings_dir, f"{stem}_Chinese.{extension}")
    return decode_strings(path.read_bytes(), length_prefixed=field == "DESC")


def perk_records(plugin: Path, own_name: str) -> dict[str, list[object]]:
    content = plugin.read_bytes()
    masters = tes4_masters(content)
    result = {}
    for header, body, _ in iter_records(content):
        if header[:4] != b"PERK":
            continue
        flags, raw_form_id = struct.unpack_from("<II", header, 8)
        if flags & COMPRESSED_FLAG:
            expected_size = struct.unpack_from("<I", body)[0]
            body = zlib.decompress(body[4:])
            if len(body) != expected_size:
                raise AssertionError(f"decompressed PERK size mismatch in {plugin.name}")
        key = form_key(raw_form_id, masters, own_name)
        if key in result:
            raise AssertionError(f"duplicate PERK FormKey in {plugin.name}: {key}")
        result[key] = parse_subrecords(body)
    return result


def inline_fields(body: bytes) -> tuple[str, dict[str, str]]:
    editor_ids = []
    visible = {}
    for subrecord in parse_subrecords(body):
        if subrecord.tag == b"EDID":
            editor_ids.append(decode_zstring(subrecord.payload))
        elif subrecord.tag in (b"FULL", b"DESC"):
            visible[subrecord.tag.decode("ascii")] = decode_zstring(subrecord.payload)
    if len(editor_ids) != 1:
        raise AssertionError("USSEP PERK does not have exactly one EDID")
    return editor_ids[0], visible


def localized_target(
    subrecords: list[object], field: str, strings_dir: Path, stem: str
) -> str:
    matches = [subrecord for subrecord in subrecords if subrecord.tag == field.encode("ascii")]
    if len(matches) != 1 or len(matches[0].payload) != 4:
        raise AssertionError(f"base {stem} PERK has invalid {field} topology")
    string_id = struct.unpack("<I", matches[0].payload)[0]
    try:
        return table(strings_dir, stem, field)[string_id].strip()
    except KeyError as exc:
        raise AssertionError(f"missing {stem} {field} string id {string_id}") from exc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path, help="exact USSEP 4.3.8a ESP")
    parser.add_argument("--data-dir", required=True, type=Path, help="Skyrim Data directory")
    parser.add_argument("--strings-dir", required=True, type=Path, help="Skyrim CHT 8.20 Strings directory")
    args = parser.parse_args()
    if sha256(args.source) != SOURCE_SHA256:
        raise SystemExit("USSEP source SHA-256 mismatch")

    base_records = {
        owner: perk_records(find_case_insensitive(args.data_dir, owner), owner)
        for owner in SUPPORTED_OWNERS
    }
    source = args.source.read_bytes()
    source_masters = tes4_masters(source)
    rows = []
    selected_keys = set()
    for header, body, _ in iter_records(source):
        if header[:4] != b"PERK":
            continue
        key = form_key(struct.unpack_from("<I", header, 12)[0], source_masters, USSEP_NAME)
        editor_id, visible = inline_fields(body)
        if not visible.get("FULL") or not visible.get("DESC"):
            continue
        if key in CONSTELLATIONS_WINNERS:
            raise AssertionError(f"later Constellations winner leaked into USSEP target set: {key}")
        owner = key.split(":", 1)[1]
        if owner not in base_records or key not in base_records[owner]:
            raise AssertionError(f"no record-identity CHT source for {key}")
        selected_keys.add(key)
        for field in ("FULL", "DESC"):
            identity = (key, field)
            target = OVERRIDES.get(identity)
            if target is None:
                target = localized_target(
                    base_records[owner][key], field, args.strings_dir, SUPPORTED_OWNERS[owner]
                )
                provenance = "Skyrim Traditional Chinese 8.20 record mapping"
            elif identity in USSEP_SEMANTIC_FIELDS:
                provenance = "Skyrim Traditional Chinese 8.20 adapted to USSEP 4.3.8a"
            else:
                provenance = "USSEP 4.3.8a custom Traditional Chinese"
            rows.append({
                "form_key": key,
                "editor_id": editor_id,
                "field": field,
                "source": visible[field],
                "target": target,
                "provenance": provenance,
            })

    if len(selected_keys) != EXPECTED_RECORDS or len(rows) != EXPECTED_FIELDS:
        raise AssertionError(
            f"selection is {len(selected_keys)} records/{len(rows)} fields, "
            f"expected {EXPECTED_RECORDS}/{EXPECTED_FIELDS}"
        )
    if set(OVERRIDES) - {(row["form_key"], row["field"]) for row in rows}:
        raise AssertionError("an override does not belong to the selected source set")

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("form_key", "editor_id", "field", "source", "target", "provenance"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUTPUT}: {len(selected_keys)} records / {len(rows)} fields")


if __name__ == "__main__":
    main()
