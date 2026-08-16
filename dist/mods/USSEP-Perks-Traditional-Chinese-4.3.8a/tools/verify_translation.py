#!/usr/bin/env python3
"""Verify provenance, text-only delta, encoding, and reproducibility."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
from pathlib import Path
import re
import struct

from plugin_localizer import (
    EXPECTED_FIELDS,
    EXPECTED_MASTERS,
    EXPECTED_RECORDS,
    LOCALIZED_FLAG,
    PLUGIN_NAME,
    SOURCE_SHA256,
    build_localized_plugin,
    decode_strings,
    decode_zstring,
    encode_strings,
    form_key,
    iter_records,
    parse_subrecords,
    read_translations,
    sha256,
    tes4_masters,
)


ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "tools" / "translation-source.tsv"
MANIFEST = ROOT / "MANIFEST.sha256"
BASE = Path(PLUGIN_NAME).stem
CONSTELLATIONS_WINNERS = {"0E5F46:Skyrim.esm", "0E5F4A:Skyrim.esm"}
SIMPLE_FORBIDDEN = set("这为后发体龙锻钢轻卫盗贼坚丽风边头术锁护")
EXPECTED_PROVENANCE = {
    "Skyrim Traditional Chinese 8.20 record mapping": 186,
    "Skyrim Traditional Chinese 8.20 adapted to USSEP 4.3.8a": 8,
    "USSEP 4.3.8a custom Traditional Chinese": 4,
}


def normalized_header(header: bytes) -> tuple[bytes, int, int, bytes]:
    flags, raw_form_id = struct.unpack_from("<II", header, 8)
    if header[:4] == b"TES4":
        flags &= ~LOCALIZED_FLAG
    return header[:4], flags, raw_form_id, header[16:24]


def verify_semantic_delta(source: bytes, output: bytes, rows: list[object]) -> None:
    if tes4_masters(source) != EXPECTED_MASTERS or tes4_masters(output) != EXPECTED_MASTERS:
        raise AssertionError("master list mismatch")
    source_records = list(iter_records(source))
    output_records = list(iter_records(output))
    if len(source_records) != EXPECTED_RECORDS + 1 or len(output_records) != len(source_records):
        raise AssertionError("record count changed or source topology is unexpected")

    rows_by_identity = {(row.form_key, row.field): row for row in rows}
    full_table = decode_strings(
        (ROOT / "Strings" / f"{BASE}_English.STRINGS").read_bytes(),
        length_prefixed=False,
    )
    desc_table = decode_strings(
        (ROOT / "Strings" / f"{BASE}_English.DLSTRINGS").read_bytes(),
        length_prefixed=True,
    )
    seen = set()
    patch_keys = set()
    for (source_header, source_body, source_path), (output_header, output_body, output_path) in zip(
        source_records, output_records
    ):
        if source_path != output_path or normalized_header(source_header) != normalized_header(output_header):
            raise AssertionError("GRUP topology or record header changed")
        source_subs = parse_subrecords(source_body)
        output_subs = parse_subrecords(output_body)
        if [sub.tag for sub in source_subs] != [sub.tag for sub in output_subs]:
            raise AssertionError("subrecord topology changed")
        if source_header[:4] == b"TES4":
            for source_sub, output_sub in zip(source_subs, output_subs):
                if source_sub.raw != output_sub.raw:
                    raise AssertionError("TES4 subrecord changed")
            continue

        key = form_key(struct.unpack_from("<I", source_header, 12)[0], EXPECTED_MASTERS, PLUGIN_NAME)
        patch_keys.add(key)
        for source_sub, output_sub in zip(source_subs, output_subs):
            if source_sub.tag in (b"FULL", b"DESC"):
                field = source_sub.tag.decode("ascii")
                row = rows_by_identity[(key, field)]
                if decode_zstring(source_sub.payload) != row.source:
                    raise AssertionError(f"source text changed for {key} {field}")
                if len(output_sub.payload) != 4:
                    raise AssertionError(f"localized id size mismatch for {key} {field}")
                string_id = struct.unpack("<I", output_sub.payload)[0]
                target_table = full_table if field == "FULL" else desc_table
                if target_table.get(string_id) != row.target:
                    raise AssertionError(f"string table mismatch for {key} {field}")
                seen.add((key, field))
            elif source_sub.raw != output_sub.raw:
                raise AssertionError(f"non-text payload changed: {key} {source_sub.tag!r}")

    if seen != set(rows_by_identity):
        raise AssertionError("localized field coverage mismatch")
    if patch_keys & CONSTELLATIONS_WINNERS:
        raise AssertionError("later Constellations winner was included")
    if len(patch_keys) != EXPECTED_RECORDS:
        raise AssertionError("PERK FormKey count mismatch")
    source_flags = struct.unpack_from("<I", source_records[0][0], 8)[0]
    output_flags = struct.unpack_from("<I", output_records[0][0], 8)[0]
    if source_flags & LOCALIZED_FLAG or output_flags != source_flags | LOCALIZED_FLAG:
        raise AssertionError("TES4 localized flag is not the sole flag delta")
    print(
        "PASS semantic delta: 99 PERK records; exact GRUP/record/subrecord topology; "
        "all non-text payloads identical; Constellations winners excluded"
    )


def numeric_tokens(value: str) -> list[str]:
    return re.findall(r"\d+(?:\.\d+)?", value)


def verify_ledger(rows: list[object]) -> None:
    counts = {name: 0 for name in EXPECTED_PROVENANCE}
    for row in rows:
        if row.provenance not in counts:
            raise AssertionError(f"unknown provenance for {row.form_key} {row.field}")
        counts[row.provenance] += 1
        if Counter(numeric_tokens(row.source)) != Counter(numeric_tokens(row.target)):
            raise AssertionError(f"numeric-token mismatch: {row.form_key} {row.field}")
    if counts != EXPECTED_PROVENANCE:
        raise AssertionError(f"provenance counts changed: {counts}")
    print("PASS ledger: 198 reviewed fields; provenance counts and numeric tokens preserved")


def verify_tables(rows: list[object]) -> None:
    english_full = (ROOT / "Strings" / f"{BASE}_English.STRINGS").read_bytes()
    chinese_full = (ROOT / "Strings" / f"{BASE}_Chinese.STRINGS").read_bytes()
    english_desc = (ROOT / "Strings" / f"{BASE}_English.DLSTRINGS").read_bytes()
    chinese_desc = (ROOT / "Strings" / f"{BASE}_Chinese.DLSTRINGS").read_bytes()
    if english_full != chinese_full or english_desc != chinese_desc:
        raise AssertionError("English/Chinese tables must be byte-identical")
    full = decode_strings(english_full, length_prefixed=False)
    desc = decode_strings(english_desc, length_prefixed=True)
    if len(full) != EXPECTED_RECORDS or len(desc) != EXPECTED_RECORDS:
        raise AssertionError("string table entry count mismatch")
    values = list(full.values()) + list(desc.values())
    if any("\ufffd" in value or "???" in value or "\t" in value or "\n" in value for value in values):
        raise AssertionError("replacement marker, mojibake sentinel, or control whitespace found")
    offenders = sorted({char for value in values for char in value if char in SIMPLE_FORBIDDEN})
    if offenders:
        raise AssertionError(f"common Simplified Chinese glyphs found: {offenders}")
    ascii_words = sorted({
        word
        for value in values
        for word in re.findall(r"[A-Za-z]{2,}", value)
        if word != "NPC"
    })
    if ascii_words:
        raise AssertionError(f"unexpected English words in targets: {ascii_words}")
    if any(ROOT.glob("Strings/*.ILSTRINGS")):
        raise AssertionError("unexpected ILSTRINGS file")
    if len(rows) != EXPECTED_FIELDS:
        raise AssertionError("ledger field count mismatch")
    print("PASS strings: 99 UTF-8 names + 99 descriptions; language tables byte-identical")


def verify_reproducible(source: Path, rows: list[object]) -> bytes:
    extracted, plugin, full, desc = build_localized_plugin(source.read_bytes(), rows)
    if plugin != (ROOT / PLUGIN_NAME).read_bytes():
        raise AssertionError("packaged ESP is not a byte-identical rebuild")
    expected_full = encode_strings(full, length_prefixed=False)
    expected_desc = encode_strings(desc, length_prefixed=True)
    for language in ("English", "Chinese"):
        if expected_full != (ROOT / "Strings" / f"{BASE}_{language}.STRINGS").read_bytes():
            raise AssertionError(f"{language} STRINGS is not reproducible")
        if expected_desc != (ROOT / "Strings" / f"{BASE}_{language}.DLSTRINGS").read_bytes():
            raise AssertionError(f"{language} DLSTRINGS is not reproducible")
    print("PASS reproducibility: packaged ESP/STRINGS equal a fresh in-memory rebuild")
    return extracted


def verify_manifest() -> None:
    listed = set()
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if "  " not in line:
            raise AssertionError(f"malformed manifest line {number}")
        expected, relative = line.split("  ", 1)
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise AssertionError(f"manifest mismatch: {relative}")
        listed.add(relative)
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and path.name != MANIFEST.name and "__pycache__" not in path.parts
    }
    if listed != actual:
        raise AssertionError(f"manifest coverage mismatch: {sorted(listed ^ actual)}")
    print(f"PASS manifest: {len(listed)} files, complete coverage")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument(
        "--skip-manifest", action="store_true", help="allow verification before docs/manifest are finalized"
    )
    args = parser.parse_args()
    if sha256(args.source) != SOURCE_SHA256:
        raise SystemExit("source SHA-256 mismatch")
    rows = read_translations(TSV)
    extracted = verify_reproducible(args.source, rows)
    verify_semantic_delta(extracted, (ROOT / PLUGIN_NAME).read_bytes(), rows)
    verify_ledger(rows)
    verify_tables(rows)
    if not args.skip_manifest:
        verify_manifest()
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
