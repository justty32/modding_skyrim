#!/usr/bin/env python3
"""Verify provenance, text-only semantic delta, tables, and reproducibility."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from pathlib import Path
import struct

from plugin_localizer import (
    Contract, LOCALIZED_FLAG, build_localized_plugin, decode_inline_text,
    decode_strings, encode_strings, form_key, iter_records, matched_rule,
    normalized_header, parse_subrecords, read_translations, record_editor_id,
    sha256, tes4_masters, tokens, uncompressed_body,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "tools" / "contract.json"
TSV = ROOT / "tools" / "translation-source.tsv"
MANIFEST = ROOT / "MANIFEST.sha256"
SIMPLE_FORBIDDEN = set("这为后发体龙锻钢轻卫盗贼坚丽风边头术锁护")


def read_tables(contract: Contract) -> dict[str, dict[int, str]]:
    base = Path(contract.plugin_name).stem
    result: dict[str, dict[int, str]] = {}
    for table in ("STRINGS", "DLSTRINGS", "ILSTRINGS"):
        english = ROOT / "Strings" / f"{base}_English.{table}"
        chinese = ROOT / "Strings" / f"{base}_Chinese.{table}"
        if english.exists() != chinese.exists():
            raise AssertionError(f"language-pair mismatch for {table}")
        if not english.exists():
            continue
        if english.read_bytes() != chinese.read_bytes():
            raise AssertionError(f"English/Chinese {table} files are not byte-identical")
        result[table] = decode_strings(
            english.read_bytes(), length_prefixed=table != "STRINGS",
        )
    return result


def verify_semantic_delta(
    source: bytes, output: bytes, contract: Contract, rows: list[object],
    tables: dict[str, dict[int, str]],
) -> None:
    if tuple(tes4_masters(source)) != contract.expected_masters:
        raise AssertionError("source master list mismatch")
    if tuple(tes4_masters(output)) != contract.expected_masters:
        raise AssertionError("output master list mismatch")
    source_records = list(iter_records(source))
    output_records = list(iter_records(output))
    if len(source_records) != contract.expected_records or len(output_records) != contract.expected_records:
        raise AssertionError("record count changed or violates contract")
    rows_by_key = {row.key: row for row in rows}
    seen: set[tuple[str, str, str, int]] = set()
    localized = 0

    for src_record, out_record in zip(source_records, output_records):
        if src_record.path != out_record.path:
            raise AssertionError("GRUP topology changed")
        if normalized_header(src_record.header) != normalized_header(out_record.header):
            raise AssertionError(f"record header changed: {src_record.signature!r}")
        src_body = uncompressed_body(src_record.header, src_record.body)
        out_body = uncompressed_body(out_record.header, out_record.body)
        src_subs = parse_subrecords(src_body)
        out_subs = parse_subrecords(out_body)
        if [x.tag for x in src_subs] != [x.tag for x in out_subs]:
            raise AssertionError("subrecord topology changed")
        signature = src_record.signature.decode("ascii")
        editor_id = record_editor_id(src_body)
        key = form_key(src_record.raw_form_id, list(contract.expected_masters), contract.plugin_name)
        occurrences: dict[str, int] = {}
        for src_sub, out_sub in zip(src_subs, out_subs):
            field = src_sub.tag.decode("ascii")
            occurrence = occurrences.get(field, 0)
            occurrences[field] = occurrence + 1
            rule = matched_rule(contract, signature, field, editor_id)
            if rule is None:
                if src_sub.payload != out_sub.payload:
                    raise AssertionError(f"non-text payload changed: {key} {field}")
                continue
            row_key = key, signature, field, occurrence
            row = rows_by_key[row_key]
            if decode_inline_text(src_sub.payload) != row.source:
                raise AssertionError(f"source text mismatch: {row_key}")
            if len(out_sub.payload) != 4:
                raise AssertionError(f"localized payload is not a uint32: {row_key}")
            string_id = struct.unpack("<I", out_sub.payload)[0]
            if string_id != row.string_id or tables[rule.table].get(string_id) != row.target:
                raise AssertionError(f"string table mismatch: {row_key}")
            seen.add(row_key)
            localized += 1
    if seen != set(rows_by_key):
        raise AssertionError("semantic sweep did not cover every TSV row")
    source_flags = struct.unpack_from("<I", source_records[0].header, 8)[0]
    output_flags = struct.unpack_from("<I", output_records[0].header, 8)[0]
    if source_flags & LOCALIZED_FLAG or output_flags != source_flags | LOCALIZED_FLAG:
        raise AssertionError("TES4 localized flag is not the sole flag delta")
    print(
        f"PASS semantic delta: {len(source_records)} records; exact topology and non-text payloads; "
        f"{localized} text fields localized"
    )


def verify_tables(contract: Contract, rows: list[object], tables: dict[str, dict[int, str]]) -> None:
    expected: dict[str, set[int]] = {name: set() for name in ("STRINGS", "DLSTRINGS", "ILSTRINGS")}
    for row in rows:
        rule = matched_rule(contract, row.record_type, row.field, row.editor_id)
        if rule is None:
            raise AssertionError(f"TSV row has no field rule: {row.key}")
        expected[rule.table].add(row.string_id)
        if tokens(row.source) != tokens(row.target):
            raise AssertionError(f"number/placeholder drift: {row.key}")
    expected = {key: value for key, value in expected.items() if value}
    if set(tables) != set(expected):
        raise AssertionError(f"string-table set mismatch: {sorted(tables)} != {sorted(expected)}")
    for table, ids in expected.items():
        if set(tables[table]) != ids:
            raise AssertionError(f"string IDs differ for {table}")
    targets = [row.target for row in rows]
    if any("\ufffd" in value or "???" in value for value in targets):
        raise AssertionError("replacement marker/mojibake sentinel found")
    offenders = sorted({char for value in targets for char in value if char in SIMPLE_FORBIDDEN})
    if offenders:
        raise AssertionError(f"common Simplified Chinese glyphs found: {offenders}")
    print(
        "PASS strings: " + ", ".join(f"{name}={len(values)}" for name, values in tables.items())
        + "; UTF-8; tokens preserved; English/Chinese byte-identical"
    )
    print("PASS provenance:", dict(Counter(row.provenance for row in rows)))


def verify_reproducible(
    source: bytes, contract: Contract, rows: list[object], tables: dict[str, dict[int, str]],
) -> None:
    plugin, rebuilt_tables = build_localized_plugin(source, rows, contract)
    if plugin != (ROOT / contract.plugin_name).read_bytes():
        raise AssertionError("packaged ESP is not a byte-identical rebuild")
    base = Path(contract.plugin_name).stem
    for table, entries in rebuilt_tables.items():
        if not entries:
            continue
        expected = encode_strings(entries, length_prefixed=table != "STRINGS")
        for language in ("English", "Chinese"):
            if expected != (ROOT / "Strings" / f"{base}_{language}.{table}").read_bytes():
                raise AssertionError(f"{language} {table} is not reproducible")
    print("PASS reproducibility: packaged ESP and string tables equal a fresh rebuild")


def verify_manifest() -> None:
    listed: set[str] = set()
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if "  " not in line:
            raise AssertionError(f"malformed manifest line {number}")
        expected, relative = line.split("  ", 1)
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents:
            raise AssertionError(f"unsafe manifest path {relative}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
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
    parser.add_argument("--source", required=True, type=Path, help="exact official English ESP")
    args = parser.parse_args()
    contract = Contract.read(CONTRACT_PATH)
    if sha256(args.source) != contract.source_sha256:
        raise SystemExit("source SHA-256 mismatch")
    rows = read_translations(TSV, contract)
    source = args.source.read_bytes()
    output = (ROOT / contract.plugin_name).read_bytes()
    tables = read_tables(contract)
    verify_semantic_delta(source, output, contract, rows, tables)
    verify_tables(contract, rows, tables)
    verify_reproducible(source, contract, rows, tables)
    verify_manifest()
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
