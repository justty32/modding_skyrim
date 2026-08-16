#!/usr/bin/env python3
"""Verify source provenance, semantic text-only delta, reproducibility, and manifest."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import struct

from plugin_localizer import (
    EXPECTED_DESC, EXPECTED_FULL, EXPECTED_MASTERS, LOCALIZED_FLAG, PLUGIN_NAME,
    SOURCE_SHA256, build_localized_plugin, decode_strings, encode_strings,
    form_key, iter_records, parse_subrecords, read_translations, sha256, tes4_masters,
)


ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "tools" / "translation-source.tsv"
MANIFEST = ROOT / "MANIFEST.sha256"
BASE = Path(PLUGIN_NAME).stem
SIMPLE_FORBIDDEN = set("这为后发体龙锻钢轻卫盗贼坚丽风边头术锁护")


def normalized_header(header: bytes) -> tuple[bytes, int, int, bytes]:
    flags, raw_form_id = struct.unpack_from("<II", header, 8)
    if header[:4] == b"TES4":
        flags &= ~LOCALIZED_FLAG
    return header[:4], flags, raw_form_id, header[16:24]


def verify_semantic_delta(source: bytes, output: bytes, rows_by_key: dict[str, object]) -> None:
    if tes4_masters(source) != EXPECTED_MASTERS or tes4_masters(output) != EXPECTED_MASTERS:
        raise AssertionError("master list mismatch")
    src_records = list(iter_records(source))
    out_records = list(iter_records(output))
    if len(src_records) != len(out_records):
        raise AssertionError("record count changed")

    full_table = decode_strings(
        (ROOT / "Strings" / f"{BASE}_English.STRINGS").read_bytes(),
        length_prefixed=False,
    )
    desc_table = decode_strings(
        (ROOT / "Strings" / f"{BASE}_English.DLSTRINGS").read_bytes(),
        length_prefixed=True,
    )
    full_count = desc_count = 0
    source_tree = []
    output_tree = []
    for (sh, sb, sp), (oh, ob, op) in zip(src_records, out_records):
        if sp != op:
            raise AssertionError("GRUP topology changed")
        if normalized_header(sh) != normalized_header(oh):
            raise AssertionError(f"record header changed: {sh[:4]!r}")
        source_tree.append((sp, normalized_header(sh)))
        output_tree.append((op, normalized_header(oh)))
        ss = parse_subrecords(sb)
        os = parse_subrecords(ob)
        if [x.tag for x in ss] != [x.tag for x in os]:
            raise AssertionError("subrecord topology changed")
        key = form_key(struct.unpack_from("<I", sh, 12)[0], EXPECTED_MASTERS)
        for src_sub, out_sub in zip(ss, os):
            if src_sub.tag == b"FULL":
                full_count += 1
                row = rows_by_key[key]
                string_id = struct.unpack("<I", out_sub.payload)[0]
                if full_table.get(string_id) != row.target:
                    raise AssertionError(f"FULL table mismatch for {key}")
            elif src_sub.tag == b"DESC":
                desc_count += 1
                if src_sub.payload != b"\0":
                    raise AssertionError(f"non-empty source DESC for {key}")
                string_id = struct.unpack("<I", out_sub.payload)[0]
                if desc_table.get(string_id) != "":
                    raise AssertionError(f"empty DESC table mismatch for {key}")
            elif src_sub.payload != out_sub.payload:
                raise AssertionError(f"non-text subrecord changed: {key} {src_sub.tag!r}")
    if source_tree != output_tree:
        raise AssertionError("record topology changed")
    if (full_count, desc_count) != (EXPECTED_FULL, EXPECTED_DESC):
        raise AssertionError(f"text topology is {full_count} FULL/{desc_count} DESC")
    source_flags = struct.unpack_from("<I", src_records[0][0], 8)[0]
    output_flags = struct.unpack_from("<I", out_records[0][0], 8)[0]
    if source_flags & LOCALIZED_FLAG or output_flags != source_flags | LOCALIZED_FLAG:
        raise AssertionError("TES4 localized flag is not the sole flag delta")
    print(
        f"PASS semantic delta: {len(src_records)} records; exact GRUP/record/subrecord topology; "
        f"all non-text payloads identical; {full_count} FULL + {desc_count} empty DESC localized"
    )


def verify_tables(rows: list[object]) -> None:
    english_full = (ROOT / "Strings" / f"{BASE}_English.STRINGS").read_bytes()
    chinese_full = (ROOT / "Strings" / f"{BASE}_Chinese.STRINGS").read_bytes()
    english_desc = (ROOT / "Strings" / f"{BASE}_English.DLSTRINGS").read_bytes()
    chinese_desc = (ROOT / "Strings" / f"{BASE}_Chinese.DLSTRINGS").read_bytes()
    if english_full != chinese_full or english_desc != chinese_desc:
        raise AssertionError("English/Chinese tables must be byte-identical")
    full = decode_strings(english_full, length_prefixed=False)
    desc = decode_strings(english_desc, length_prefixed=True)
    if len(full) != EXPECTED_FULL or len(desc) != EXPECTED_DESC:
        raise AssertionError("string table entry count mismatch")
    if set(full) != {row.string_id for row in rows}:
        raise AssertionError("FULL ids differ from review TSV")
    if any(desc.values()):
        raise AssertionError("DESC table contains non-empty text")
    values = list(full.values())
    if any("\ufffd" in value or "???" in value for value in values):
        raise AssertionError("replacement marker/mojibake sentinel found")
    offenders = sorted({char for value in values for char in value if char in SIMPLE_FORBIDDEN})
    if offenders:
        raise AssertionError(f"common Simplified Chinese glyphs found: {offenders}")
    if any(ROOT.glob("Strings/*.ILSTRINGS")):
        raise AssertionError("unexpected empty ILSTRINGS file")
    print("PASS strings: 70 UTF-8 targets; English/Chinese tables byte-identical; 69 empty DESC")


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
    checked = 0
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if "  " not in line:
            raise AssertionError(f"malformed manifest line {number}")
        expected, relative = line.split("  ", 1)
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents:
            raise AssertionError(f"unsafe manifest path {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"manifest mismatch: {relative}")
        checked += 1
    expected_files = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and path.name != MANIFEST.name and "__pycache__" not in path.parts
    }
    listed = {line.split("  ", 1)[1] for line in MANIFEST.read_text().splitlines()}
    if listed != expected_files:
        raise AssertionError(f"manifest coverage mismatch: {sorted(expected_files ^ listed)}")
    print(f"PASS manifest: {checked} files, complete coverage")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path, help="exact official English ESP")
    args = parser.parse_args()
    if sha256(args.source) != SOURCE_SHA256:
        raise SystemExit("source SHA-256 mismatch")
    rows = read_translations(TSV)
    if sum(row.provenance == "Skyrim Traditional Chinese 8.20 exact FormID seed" for row in rows) != 12:
        raise AssertionError("expected exactly 12 vanilla 8.20 seeds")
    if sum(row.provenance == "CT77 custom; Skyrim 8.20 terminology" for row in rows) != 58:
        raise AssertionError("expected exactly 58 CT77 custom translations")
    rows_by_key = {row.form_key: row for row in rows}
    output = (ROOT / PLUGIN_NAME).read_bytes()
    verify_semantic_delta(args.source.read_bytes(), output, rows_by_key)
    verify_tables(rows)
    verify_reproducible(args.source, rows)
    verify_manifest()
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
