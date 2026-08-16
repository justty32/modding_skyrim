#!/usr/bin/env python3
"""Minimal, byte-preserving Skyrim plugin localizer used by this release.

The source plugin is intentionally not reserialized through a general-purpose
library.  Records and groups are copied verbatim except for the TES4 localized
flag, FULL/DESC payloads, and the size fields made necessary by those payloads.
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
import hashlib
from pathlib import Path
import struct
from typing import Iterator


PLUGIN_NAME = "Remodeled Armor - Vanilla Replacer.esp"
SOURCE_SHA256 = "611cb362893016a25509db6afabd8753398248d08a05bd54ef93ceb8875f157a"
ARCHIVE_SHA256 = "3dc631e4c3b061e0feb999254172ca42d6df98be86c42461a39ed8accedeb4a6"
LOCALIZED_FLAG = 0x00000080
COMPRESSED_FLAG = 0x00040000
EXPECTED_MASTERS = ["Skyrim.esm", "Update.esm", "Dawnguard.esm", "Dragonborn.esm"]
EXPECTED_FULL = 70
EXPECTED_DESC = 69


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Translation:
    string_id: int
    form_key: str
    editor_id: str
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
    pos = 0
    while pos < len(data):
        start = pos
        if pos + 6 > len(data):
            raise AssertionError(f"truncated subrecord header at {pos}")
        tag = data[pos : pos + 4]
        size = struct.unpack_from("<H", data, pos + 4)[0]
        pos += 6
        if tag == b"XXXX":
            if size != 4 or pos + 10 > len(data):
                raise AssertionError(f"malformed XXXX at {start}")
            size = struct.unpack_from("<I", data, pos)[0]
            pos += 4
            tag = data[pos : pos + 4]
            pos += 6  # real tag plus ignored 16-bit size
        end = pos + size
        if end > len(data):
            raise AssertionError(f"truncated {tag!r} payload at {pos}")
        result.append(Subrecord(tag, data[pos:end], data[start:end]))
        pos = end
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
    expected_header = {
        "string_id", "form_key", "editor_id", "source", "target", "provenance"
    }
    if not rows or set(rows[0]) != expected_header:
        raise AssertionError("unexpected translation TSV columns")
    result: list[Translation] = []
    for row in rows:
        item = Translation(
            int(row["string_id"], 16), row["form_key"], row["editor_id"],
            row["source"], row["target"], row["provenance"],
        )
        if not item.target.strip():
            raise AssertionError(f"blank target for {item.form_key}")
        result.append(item)
    if len(result) != EXPECTED_FULL:
        raise AssertionError(f"translation count {len(result)} != {EXPECTED_FULL}")
    if len({row.form_key for row in result}) != len(result):
        raise AssertionError("duplicate FormKey")
    if len({row.string_id for row in result}) != len(result):
        raise AssertionError("duplicate string id")
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
    seen: set[str]
    next_id: int = 1


def transform_record(header: bytes, body: bytes, state: BuildState) -> bytes:
    signature = header[:4]
    flags, raw_form_id = struct.unpack_from("<II", header, 8)
    if signature == b"TES4":
        changed = bytearray(header)
        struct.pack_into("<I", changed, 8, flags | LOCALIZED_FLAG)
        return bytes(changed) + body

    key = form_key(raw_form_id, state.masters)
    subs = parse_subrecords(body)
    if not any(sub.tag in (b"FULL", b"DESC") for sub in subs):
        return header + body
    if flags & COMPRESSED_FLAG:
        raise AssertionError(f"refusing to rewrite compressed localized record {key}")

    editor_ids = [decode_zstring(sub.payload) for sub in subs if sub.tag == b"EDID"]
    editor_id = editor_ids[0] if len(editor_ids) == 1 else ""
    out = bytearray()
    for sub in subs:
        if sub.tag == b"FULL":
            row = state.translations.get(key)
            if row is None:
                raise AssertionError(f"FULL has no translation row: {key}")
            if row.editor_id != editor_id:
                raise AssertionError(f"EditorID mismatch for {key}: {editor_id!r}")
            if row.source != decode_zstring(sub.payload):
                raise AssertionError(f"source text mismatch for {key}")
            if row.string_id != state.next_id:
                raise AssertionError(
                    f"string id mismatch for {key}: TSV={row.string_id:#x}, "
                    f"actual={state.next_id:#x}"
                )
            out += encode_subrecord(b"FULL", struct.pack("<I", state.next_id))
            state.full_entries.append((state.next_id, row.target))
            state.seen.add(key)
            state.next_id += 1
        elif sub.tag == b"DESC":
            if sub.payload != b"\0":
                raise AssertionError(f"non-empty DESC is outside this release contract: {key}")
            out += encode_subrecord(b"DESC", struct.pack("<I", state.next_id))
            state.desc_entries.append((state.next_id, ""))
            state.next_id += 1
        else:
            out += sub.raw

    changed = bytearray(header)
    struct.pack_into("<I", changed, 4, len(out))
    return bytes(changed) + bytes(out)


def transform_region(plugin: bytes, start: int, end: int, state: BuildState) -> bytes:
    out = bytearray()
    pos = start
    while pos < end:
        if pos + 24 > end:
            raise AssertionError(f"truncated record/group header at {pos}")
        header = plugin[pos : pos + 24]
        signature = header[:4]
        size = struct.unpack_from("<I", header, 4)[0]
        if signature == b"GRUP":
            if size < 24 or pos + size > end:
                raise AssertionError(f"invalid GRUP size {size} at {pos}")
            children = transform_region(plugin, pos + 24, pos + size, state)
            changed = bytearray(header)
            struct.pack_into("<I", changed, 4, 24 + len(children))
            out += changed + children
            pos += size
        else:
            record_end = pos + 24 + size
            if record_end > end:
                raise AssertionError(f"invalid {signature!r} record size at {pos}")
            out += transform_record(header, plugin[pos + 24 : record_end], state)
            pos = record_end
    if pos != end:
        raise AssertionError("region traversal did not end exactly")
    return bytes(out)


def build_localized_plugin(source: bytes, rows: list[Translation]) -> tuple[bytes, list[tuple[int, str]], list[tuple[int, str]]]:
    masters = tes4_masters(source)
    if masters != EXPECTED_MASTERS:
        raise AssertionError(f"master contract mismatch: {masters}")
    state = BuildState(masters, {row.form_key: row for row in rows}, [], [], set())
    output = transform_region(source, 0, len(source), state)
    if len(state.full_entries) != EXPECTED_FULL or len(state.desc_entries) != EXPECTED_DESC:
        raise AssertionError(
            f"localized topology mismatch: FULL={len(state.full_entries)} "
            f"DESC={len(state.desc_entries)}"
        )
    if state.seen != set(state.translations):
        missing = sorted(set(state.translations) - state.seen)
        raise AssertionError(f"unused translation rows: {missing}")
    if state.next_id != EXPECTED_FULL + EXPECTED_DESC + 1:
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
        pos = data_start + offset
        if length_prefixed:
            size = struct.unpack_from("<I", data, pos)[0]
            raw = data[pos + 4 : pos + 4 + size]
            if len(raw) != size or not raw.endswith(b"\0"):
                raise AssertionError("invalid length-prefixed string")
        else:
            end = data.index(b"\0", pos)
            raw = data[pos : end + 1]
        if string_id in result:
            raise AssertionError(f"duplicate string id {string_id:#x}")
        result[string_id] = raw[:-1].decode("utf-8")
    return result


def iter_records(plugin: bytes) -> Iterator[tuple[bytes, bytes, bytes]]:
    """Yield (header, body, normalized group path marker) in file order."""
    def walk(start: int, end: int, path: bytes) -> Iterator[tuple[bytes, bytes, bytes]]:
        pos = start
        while pos < end:
            header = plugin[pos : pos + 24]
            size = struct.unpack_from("<I", header, 4)[0]
            if header[:4] == b"GRUP":
                marker = header[:4] + header[8:24]
                yield from walk(pos + 24, pos + size, path + marker)
                pos += size
            else:
                yield header, plugin[pos + 24 : pos + 24 + size], path
                pos += 24 + size
    yield from walk(0, len(plugin), b"")
