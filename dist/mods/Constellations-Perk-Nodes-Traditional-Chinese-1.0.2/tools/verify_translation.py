#!/usr/bin/env python3
"""Verify provenance, text-only semantic delta, encoding, and reproducibility."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import struct

from plugin_localizer import (
    EXPECTED_MASTERS, EXPECTED_RECORDS, LOCALIZED_FLAG, PLUGIN_NAME,
    SOURCE_SHA256, build_localized_plugin, decode_strings, encode_strings,
    form_key, iter_records, parse_subrecords, read_translations, sha256,
    tes4_masters,
)


ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "tools" / "translation-source.tsv"
MANIFEST = ROOT / "MANIFEST.sha256"
BASE = Path(PLUGIN_NAME).stem
SIMPLE_FORBIDDEN = set("这为后发体龙锻钢轻卫盗贼坚丽风边头术锁护里")


def normalized_header(header: bytes) -> tuple[bytes, int, int, bytes]:
    flags, raw_form_id = struct.unpack_from("<II", header, 8)
    if header[:4] == b"TES4":
        flags &= ~LOCALIZED_FLAG
    return header[:4], flags, raw_form_id, header[16:24]


def verify_semantic_delta(source: bytes, output: bytes, rows_by_key: dict[str, object]) -> None:
    if tes4_masters(source) != EXPECTED_MASTERS or tes4_masters(output) != EXPECTED_MASTERS:
        raise AssertionError("master list mismatch")
    source_records = list(iter_records(source))
    output_records = list(iter_records(output))
    if len(source_records) != EXPECTED_RECORDS + 1 or len(output_records) != len(source_records):
        raise AssertionError("record count changed or source topology is unexpected")

    full_table = decode_strings(
        (ROOT / "Strings" / f"{BASE}_English.STRINGS").read_bytes(),
        length_prefixed=False,
    )
    desc_table = decode_strings(
        (ROOT / "Strings" / f"{BASE}_English.DLSTRINGS").read_bytes(),
        length_prefixed=True,
    )
    full_count = desc_count = 0
    for (source_header, source_body, source_path), (output_header, output_body, output_path) in zip(
        source_records, output_records
    ):
        if source_path != output_path or normalized_header(source_header) != normalized_header(output_header):
            raise AssertionError("GRUP topology or record header changed")
        source_subs = parse_subrecords(source_body)
        output_subs = parse_subrecords(output_body)
        if [sub.tag for sub in source_subs] != [sub.tag for sub in output_subs]:
            raise AssertionError("subrecord topology changed")
        key = form_key(struct.unpack_from("<I", source_header, 12)[0], EXPECTED_MASTERS)
        for source_sub, output_sub in zip(source_subs, output_subs):
            if source_sub.tag == b"FULL":
                row = rows_by_key[key]
                string_id = struct.unpack("<I", output_sub.payload)[0]
                if full_table.get(string_id) != row.target_name:
                    raise AssertionError(f"FULL table mismatch for {key}")
                full_count += 1
            elif source_sub.tag == b"DESC":
                row = rows_by_key[key]
                string_id = struct.unpack("<I", output_sub.payload)[0]
                if desc_table.get(string_id) != row.target_description:
                    raise AssertionError(f"DESC table mismatch for {key}")
                desc_count += 1
            elif source_sub.payload != output_sub.payload:
                raise AssertionError(f"non-text payload changed: {key} {source_sub.tag!r}")
    if (full_count, desc_count) != (EXPECTED_RECORDS, EXPECTED_RECORDS):
        raise AssertionError(f"text topology is {full_count} FULL/{desc_count} DESC")
    source_flags = struct.unpack_from("<I", source_records[0][0], 8)[0]
    output_flags = struct.unpack_from("<I", output_records[0][0], 8)[0]
    if source_flags & LOCALIZED_FLAG or output_flags != source_flags | LOCALIZED_FLAG:
        raise AssertionError("TES4 localized flag is not the sole flag delta")
    print(
        "PASS semantic delta: 45 records; exact GRUP/record/subrecord topology; "
        "all non-text payloads identical; 44 FULL + 44 DESC localized"
    )


def numeric_tokens(value: str) -> list[str]:
    return re.findall(r"\d+(?:%| times)?", value)


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
    if any("\ufffd" in value or "???" in value for value in values):
        raise AssertionError("replacement marker/mojibake sentinel found")
    offenders = sorted({char for value in values for char in value if char in SIMPLE_FORBIDDEN})
    if offenders:
        raise AssertionError(f"common Simplified Chinese glyphs found: {offenders}")
    for row in rows:
        if numeric_tokens(row.source_name) != numeric_tokens(row.target_name):
            raise AssertionError(f"name numeric-token mismatch: {row.form_key}")
        source_numbers = [token.split()[0] for token in numeric_tokens(row.source_description)]
        target_numbers = [token.split()[0] for token in numeric_tokens(row.target_description)]
        if source_numbers != target_numbers:
            raise AssertionError(f"description numeric-token mismatch: {row.form_key}")
    if any(ROOT.glob("Strings/*.ILSTRINGS")):
        raise AssertionError("unexpected ILSTRINGS file")
    print("PASS strings: 44 UTF-8 names + 44 descriptions; language tables byte-identical; numbers preserved")


def verify_reproducible(source: Path, rows: list[object]) -> None:
    plugin, full, desc = build_localized_plugin(source.read_bytes(), rows)
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


def verify_manifest() -> None:
    listed: set[str] = set()
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
    args = parser.parse_args()
    if sha256(args.source) != SOURCE_SHA256:
        raise SystemExit("source SHA-256 mismatch")
    rows = read_translations(TSV)
    output = (ROOT / PLUGIN_NAME).read_bytes()
    verify_semantic_delta(args.source.read_bytes(), output, {row.form_key: row for row in rows})
    verify_tables(rows)
    verify_reproducible(args.source, rows)
    verify_manifest()
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
