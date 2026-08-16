#!/usr/bin/env python3
"""Build a minimal localized PERK patch from exact USSEP 4.3.8a bytes."""

from __future__ import annotations

from dataclasses import dataclass
import csv
import hashlib
from pathlib import Path
import struct
from typing import Iterator


PLUGIN_NAME = "USSEP Perks Traditional Chinese 4.3.8a.esp"
USSEP_NAME = "unofficial skyrim special edition patch.esp"
SOURCE_SHA256 = "2df73db3622005e04470e3603f804e2fd855ae932a9847073f386bd8013e9d98"
SOURCE_MASTERS = [
    "Skyrim.esm", "Update.esm", "Dawnguard.esm", "HearthFires.esm",
    "Dragonborn.esm", "ccbgssse001-fish.esm", "ccqdrsse001-survivalmode.esl",
    "ccbgssse037-curios.esl", "ccbgssse025-advdsgs.esm", "_ResourcePack.esl",
]
EXPECTED_MASTERS = SOURCE_MASTERS + [USSEP_NAME]
LOCALIZED_FLAG = 0x00000080
EXPECTED_RECORDS = 99
EXPECTED_FIELDS = 198


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Translation:
    form_key: str
    editor_id: str
    field: str
    source: str
    target: str
    provenance: str


@dataclass(frozen=True)
class Subrecord:
    tag: bytes
    payload: bytes
    raw: bytes


def parse_subrecords(data: bytes) -> list[Subrecord]:
    result: list[Subrecord] = []
    position = 0
    while position < len(data):
        start = position
        if position + 6 > len(data):
            raise AssertionError(f"truncated subrecord header at {position}")
        tag = data[position : position + 4]
        size = struct.unpack_from("<H", data, position + 4)[0]
        position += 6
        if tag == b"XXXX":
            if size != 4 or position + 10 > len(data):
                raise AssertionError(f"malformed XXXX at {start}")
            size = struct.unpack_from("<I", data, position)[0]
            position += 4
            tag = data[position : position + 4]
            position += 6
        end = position + size
        if end > len(data):
            raise AssertionError(f"truncated {tag!r} payload")
        result.append(Subrecord(tag, data[position:end], data[start:end]))
        position = end
    return result


def encode_subrecord(tag: bytes, payload: bytes) -> bytes:
    if len(tag) != 4 or len(payload) > 0xFFFF:
        raise AssertionError("subrecord does not fit short encoding")
    return tag + struct.pack("<H", len(payload)) + payload


def decode_zstring(payload: bytes) -> str:
    if not payload.endswith(b"\0") or b"\0" in payload[:-1]:
        raise AssertionError("not a canonical zstring")
    return payload[:-1].decode("cp1252")


def read_translations(path: Path) -> list[Translation]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    expected = {"form_key", "editor_id", "field", "source", "target", "provenance"}
    if not rows or set(rows[0]) != expected:
        raise AssertionError("unexpected translation TSV columns")
    result = [Translation(**row) for row in rows]
    if len(result) != EXPECTED_FIELDS:
        raise AssertionError(f"translation count {len(result)} != {EXPECTED_FIELDS}")
    identities = {(row.form_key, row.field) for row in result}
    if len(identities) != len(result):
        raise AssertionError("duplicate FormKey/field")
    if {row.field for row in result} != {"FULL", "DESC"}:
        raise AssertionError("translation fields must be FULL/DESC")
    records = {row.form_key for row in result}
    if len(records) != EXPECTED_RECORDS:
        raise AssertionError(f"record count {len(records)} != {EXPECTED_RECORDS}")
    if any(not row.editor_id or not row.source or not row.target for row in result):
        raise AssertionError("blank translation field")
    return result


def tes4_masters(plugin: bytes) -> list[str]:
    if plugin[:4] != b"TES4":
        raise AssertionError("plugin does not begin with TES4")
    size = struct.unpack_from("<I", plugin, 4)[0]
    return [
        decode_zstring(sub.payload)
        for sub in parse_subrecords(plugin[24 : 24 + size])
        if sub.tag == b"MAST"
    ]


def form_key(raw_form_id: int, masters: list[str], own_name: str) -> str:
    index = raw_form_id >> 24
    owner = masters[index] if index < len(masters) else own_name
    return f"{raw_form_id & 0xFFFFFF:06X}:{owner}"


def iter_records(plugin: bytes) -> Iterator[tuple[bytes, bytes, bytes]]:
    def walk(start: int, end: int, path: bytes) -> Iterator[tuple[bytes, bytes, bytes]]:
        position = start
        while position < end:
            if position + 24 > end:
                raise AssertionError("truncated record/group header")
            header = plugin[position : position + 24]
            size = struct.unpack_from("<I", header, 4)[0]
            if header[:4] == b"GRUP":
                if size < 24 or position + size > end:
                    raise AssertionError("invalid GRUP size")
                marker = header[:4] + header[8:24]
                yield from walk(position + 24, position + size, path + marker)
                position += size
            else:
                record_end = position + 24 + size
                if record_end > end:
                    raise AssertionError("invalid record size")
                yield header, plugin[position + 24 : record_end], path
                position = record_end
    yield from walk(0, len(plugin), b"")


def make_tes4(source_header: bytes, record_count: int) -> bytes:
    body = bytearray()
    body += encode_subrecord(b"HEDR", struct.pack("<fII", 1.7, record_count, 0x800))
    body += encode_subrecord(b"CNAM", b"justty32 / Codex\0")
    body += encode_subrecord(
        b"SNAM", b"Traditional Chinese text-only patch for USSEP PERK records.\0"
    )
    for master in EXPECTED_MASTERS:
        body += encode_subrecord(b"MAST", master.encode("cp1252") + b"\0")
        body += encode_subrecord(b"DATA", b"\0" * 8)
    header = bytearray(source_header)
    struct.pack_into("<I", header, 4, len(body))
    struct.pack_into("<I", header, 8, 0)
    struct.pack_into("<I", header, 12, 0)
    return bytes(header) + bytes(body)


def extract_source_patch(source: bytes, rows: list[Translation]) -> bytes:
    if tes4_masters(source) != SOURCE_MASTERS:
        raise AssertionError("USSEP master contract mismatch")
    wanted = {row.form_key for row in rows}
    records: list[bytes] = []
    seen: set[str] = set()
    group_template = None
    position = 24 + struct.unpack_from("<I", source, 4)[0]
    while position < len(source):
        header = source[position : position + 24]
        size = struct.unpack_from("<I", header, 4)[0]
        if header[:4] == b"GRUP" and header[8:12] == b"PERK" and struct.unpack_from("<I", header, 12)[0] == 0:
            group_template = header
            break
        position += size if header[:4] == b"GRUP" else 24 + size
    if group_template is None:
        raise AssertionError("USSEP has no top-level PERK group")

    for header, body, _ in iter_records(source):
        if header[:4] != b"PERK":
            continue
        flags = struct.unpack_from("<I", header, 8)[0]
        if flags & 0x00040000:
            raise AssertionError("compressed PERK is outside the extractor contract")
        raw_form_id = struct.unpack_from("<I", header, 12)[0]
        key = form_key(raw_form_id, SOURCE_MASTERS, USSEP_NAME)
        if key in wanted:
            records.append(header + body)
            seen.add(key)
    if seen != wanted or len(records) != EXPECTED_RECORDS:
        raise AssertionError(f"source record selection mismatch: {sorted(wanted ^ seen)}")

    group = bytearray(group_template)
    struct.pack_into("<I", group, 4, 24 + sum(map(len, records)))
    tes4 = make_tes4(source[:24], len(records))
    return tes4 + bytes(group) + b"".join(records)


@dataclass
class BuildState:
    masters: list[str]
    rows: dict[tuple[str, str], Translation]
    full_entries: list[tuple[int, str]]
    desc_entries: list[tuple[int, str]]
    seen: set[tuple[str, str]]
    next_id: int = 1


def transform_record(header: bytes, body: bytes, state: BuildState) -> bytes:
    flags, raw_form_id = struct.unpack_from("<II", header, 8)
    if header[:4] == b"TES4":
        changed = bytearray(header)
        struct.pack_into("<I", changed, 8, flags | LOCALIZED_FLAG)
        return bytes(changed) + body
    if header[:4] != b"PERK":
        return header + body

    key = form_key(raw_form_id, state.masters, PLUGIN_NAME)
    subs = parse_subrecords(body)
    editor_ids = [decode_zstring(sub.payload) for sub in subs if sub.tag == b"EDID"]
    if len(editor_ids) != 1:
        raise AssertionError(f"PERK EditorID topology mismatch: {key}")
    output = bytearray()
    for sub in subs:
        field = sub.tag.decode("ascii") if sub.tag in (b"FULL", b"DESC") else ""
        if field:
            row = state.rows.get((key, field))
            if row is None or row.editor_id != editor_ids[0]:
                raise AssertionError(f"missing/mismatched row: {key} {field}")
            if decode_zstring(sub.payload) != row.source:
                raise AssertionError(f"source text mismatch: {key} {field}")
            output += encode_subrecord(sub.tag, struct.pack("<I", state.next_id))
            target = state.full_entries if field == "FULL" else state.desc_entries
            target.append((state.next_id, row.target))
            state.seen.add((key, field))
            state.next_id += 1
        else:
            output += sub.raw
    changed = bytearray(header)
    struct.pack_into("<I", changed, 4, len(output))
    return bytes(changed) + bytes(output)


def transform_region(plugin: bytes, start: int, end: int, state: BuildState) -> bytes:
    output = bytearray()
    position = start
    while position < end:
        header = plugin[position : position + 24]
        size = struct.unpack_from("<I", header, 4)[0]
        if header[:4] == b"GRUP":
            children = transform_region(plugin, position + 24, position + size, state)
            changed = bytearray(header)
            struct.pack_into("<I", changed, 4, 24 + len(children))
            output += changed + children
            position += size
        else:
            record_end = position + 24 + size
            output += transform_record(header, plugin[position + 24 : record_end], state)
            position = record_end
    return bytes(output)


def build_localized_plugin(source: bytes, rows: list[Translation]):
    extracted = extract_source_patch(source, rows)
    masters = tes4_masters(extracted)
    if masters != EXPECTED_MASTERS:
        raise AssertionError("extracted patch master list mismatch")
    state = BuildState(masters, {(r.form_key, r.field): r for r in rows}, [], [], set())
    output = transform_region(extracted, 0, len(extracted), state)
    if state.seen != set(state.rows):
        raise AssertionError(f"unused translation rows: {sorted(set(state.rows) - state.seen)}")
    if len(state.full_entries) != EXPECTED_RECORDS or len(state.desc_entries) != EXPECTED_RECORDS:
        raise AssertionError("FULL/DESC topology mismatch")
    return extracted, output, state.full_entries, state.desc_entries


def encode_strings(entries: list[tuple[int, str]], *, length_prefixed: bool) -> bytes:
    directory = bytearray()
    data = bytearray()
    for string_id, value in sorted(entries):
        raw = value.encode("utf-8") + b"\0"
        directory += struct.pack("<II", string_id, len(data))
        if length_prefixed:
            data += struct.pack("<I", len(raw))
        data += raw
    return struct.pack("<II", len(entries), len(data)) + directory + data


def decode_strings(data: bytes, *, length_prefixed: bool) -> dict[int, str]:
    count, data_size = struct.unpack_from("<II", data)
    data_start = 8 + count * 8
    if data_start + data_size != len(data):
        raise AssertionError("STRINGS size mismatch")
    result = {}
    for index in range(count):
        string_id, offset = struct.unpack_from("<II", data, 8 + index * 8)
        position = data_start + offset
        if length_prefixed:
            size = struct.unpack_from("<I", data, position)[0]
            raw = data[position + 4 : position + 4 + size]
        else:
            end = data.index(b"\0", position)
            raw = data[position : end + 1]
        if not raw.endswith(b"\0"):
            raise AssertionError("unterminated localized string")
        result[string_id] = raw[:-1].decode("utf-8")
    return result
