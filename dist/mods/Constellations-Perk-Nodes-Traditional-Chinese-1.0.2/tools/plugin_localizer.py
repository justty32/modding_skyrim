#!/usr/bin/env python3
"""Deterministic, byte-preserving localizer for the Constellations perk patch."""

from __future__ import annotations

from dataclasses import dataclass
import csv
import hashlib
from pathlib import Path
import struct
from typing import Iterator


PLUGIN_NAME = "Constellations Perk Nodes Traditional Chinese 1.0.2.esp"
SOURCE_SHA256 = "facddcde7c8770b4694f866d2d3ab1442088603d1d0c64955544e416a5bb451d"
LOCALIZED_FLAG = 0x00000080
COMPRESSED_FLAG = 0x00040000
EXPECTED_MASTERS = ["Skyrim.esm", "Update.esm", "ConstellationsNewSkills.esp"]
EXPECTED_RECORDS = 44


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Translation:
    form_key: str
    editor_id: str
    source_name: str
    target_name: str
    source_description: str
    target_description: str


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
            raise AssertionError(f"truncated {tag!r} payload at {position}")
        result.append(Subrecord(tag, data[position:end], data[start:end]))
        position = end
    return result


def encode_subrecord(tag: bytes, payload: bytes) -> bytes:
    if len(tag) != 4 or len(payload) > 0xFFFF:
        raise AssertionError("localized subrecord does not fit the short form")
    return tag + struct.pack("<H", len(payload)) + payload


def decode_zstring(payload: bytes) -> str:
    if not payload.endswith(b"\0") or b"\0" in payload[:-1]:
        raise AssertionError(f"not a canonical zstring: {payload!r}")
    return payload[:-1].decode("cp1252")


def read_translations(path: Path) -> list[Translation]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    expected = {
        "form_key", "editor_id", "source_name", "target_name",
        "source_description", "target_description",
    }
    if not rows or set(rows[0]) != expected:
        raise AssertionError("unexpected translation TSV columns")
    result = [Translation(**row) for row in rows]
    if len(result) != EXPECTED_RECORDS:
        raise AssertionError(f"translation count {len(result)} != {EXPECTED_RECORDS}")
    if len({row.form_key for row in result}) != len(result):
        raise AssertionError("duplicate FormKey")
    for row in result:
        if not all((row.editor_id, row.source_name, row.target_name,
                    row.source_description, row.target_description)):
            raise AssertionError(f"blank translation field for {row.form_key}")
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


def form_key(raw_form_id: int, masters: list[str]) -> str:
    index = raw_form_id >> 24
    owner = masters[index] if index < len(masters) else PLUGIN_NAME
    return f"{raw_form_id & 0xFFFFFF:06X}:{owner}"


@dataclass
class BuildState:
    masters: list[str]
    translations: dict[str, Translation]
    full_entries: list[tuple[int, str]]
    desc_entries: list[tuple[int, str]]
    seen_full: set[str]
    seen_desc: set[str]
    next_id: int = 1


def transform_record(header: bytes, body: bytes, state: BuildState) -> bytes:
    signature = header[:4]
    flags, raw_form_id = struct.unpack_from("<II", header, 8)
    if signature == b"TES4":
        changed = bytearray(header)
        struct.pack_into("<I", changed, 8, flags | LOCALIZED_FLAG)
        return bytes(changed) + body
    if signature != b"PERK":
        return header + body
    if flags & COMPRESSED_FLAG:
        raise AssertionError("refusing to rewrite a compressed PERK")

    key = form_key(raw_form_id, state.masters)
    row = state.translations.get(key)
    if row is None:
        raise AssertionError(f"unexpected PERK record: {key}")
    subs = parse_subrecords(body)
    editor_ids = [decode_zstring(sub.payload) for sub in subs if sub.tag == b"EDID"]
    if editor_ids != [row.editor_id]:
        raise AssertionError(f"EditorID mismatch for {key}: {editor_ids}")

    output = bytearray()
    for sub in subs:
        if sub.tag == b"FULL":
            if key in state.seen_full or decode_zstring(sub.payload) != row.source_name:
                raise AssertionError(f"FULL source/topology mismatch for {key}")
            output += encode_subrecord(b"FULL", struct.pack("<I", state.next_id))
            state.full_entries.append((state.next_id, row.target_name))
            state.seen_full.add(key)
            state.next_id += 1
        elif sub.tag == b"DESC":
            if key in state.seen_desc or decode_zstring(sub.payload) != row.source_description:
                raise AssertionError(f"DESC source/topology mismatch for {key}")
            output += encode_subrecord(b"DESC", struct.pack("<I", state.next_id))
            state.desc_entries.append((state.next_id, row.target_description))
            state.seen_desc.add(key)
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
        if position + 24 > end:
            raise AssertionError(f"truncated record/group header at {position}")
        header = plugin[position : position + 24]
        size = struct.unpack_from("<I", header, 4)[0]
        if header[:4] == b"GRUP":
            if size < 24 or position + size > end:
                raise AssertionError(f"invalid GRUP size {size} at {position}")
            children = transform_region(plugin, position + 24, position + size, state)
            changed = bytearray(header)
            struct.pack_into("<I", changed, 4, 24 + len(children))
            output += changed + children
            position += size
        else:
            record_end = position + 24 + size
            if record_end > end:
                raise AssertionError(f"invalid record size at {position}")
            output += transform_record(header, plugin[position + 24 : record_end], state)
            position = record_end
    if position != end:
        raise AssertionError("region traversal did not end exactly")
    return bytes(output)


def build_localized_plugin(
    source: bytes, rows: list[Translation]
) -> tuple[bytes, list[tuple[int, str]], list[tuple[int, str]]]:
    masters = tes4_masters(source)
    if masters != EXPECTED_MASTERS:
        raise AssertionError(f"master contract mismatch: {masters}")
    state = BuildState(masters, {row.form_key: row for row in rows}, [], [], set(), set())
    output = transform_region(source, 0, len(source), state)
    expected_keys = set(state.translations)
    if state.seen_full != expected_keys or state.seen_desc != expected_keys:
        raise AssertionError("not every translation row matched one FULL and one DESC")
    if state.next_id != EXPECTED_RECORDS * 2 + 1:
        raise AssertionError(f"unexpected final string id {state.next_id}")
    return output, state.full_entries, state.desc_entries


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
    if len(data) < 8:
        raise AssertionError("truncated STRINGS header")
    count, data_size = struct.unpack_from("<II", data)
    data_start = 8 + count * 8
    if data_start + data_size != len(data):
        raise AssertionError("STRINGS size contract mismatch")
    result: dict[int, str] = {}
    for index in range(count):
        string_id, offset = struct.unpack_from("<II", data, 8 + index * 8)
        position = data_start + offset
        if length_prefixed:
            size = struct.unpack_from("<I", data, position)[0]
            raw = data[position + 4 : position + 4 + size]
            if len(raw) != size or not raw.endswith(b"\0"):
                raise AssertionError("invalid length-prefixed string")
        else:
            end = data.index(b"\0", position)
            raw = data[position : end + 1]
        if string_id in result:
            raise AssertionError(f"duplicate string id {string_id:#x}")
        result[string_id] = raw[:-1].decode("utf-8")
    return result


def iter_records(plugin: bytes) -> Iterator[tuple[bytes, bytes, bytes]]:
    """Yield (record header, body, group-path marker) in file order."""
    def walk(start: int, end: int, path: bytes) -> Iterator[tuple[bytes, bytes, bytes]]:
        position = start
        while position < end:
            header = plugin[position : position + 24]
            size = struct.unpack_from("<I", header, 4)[0]
            if header[:4] == b"GRUP":
                marker = header[:4] + header[8:24]
                yield from walk(position + 24, position + size, path + marker)
                position += size
            else:
                yield header, plugin[position + 24 : position + 24 + size], path
                position += 24 + size
    yield from walk(0, len(plugin), b"")
