#!/usr/bin/env python3
"""Deterministic byte-preserving localizer for Skyrim SE plugins.

The build rewrites only fields declared in contract.json, plus the TES4
localized flag and unavoidable record/group sizes. Compressed record bodies
are decompressed, edited, and deterministically recompressed; verification
compares their uncompressed semantic payloads.
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
from typing import Iterator
import zlib


LOCALIZED_FLAG = 0x00000080
COMPRESSED_FLAG = 0x00040000
TSV_FIELDS = (
    "string_id", "form_key", "record_type", "editor_id", "field",
    "occurrence", "source", "target", "provenance",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class FieldRule:
    record_type: str
    field: str
    table: str
    editor_prefix: str = ""


@dataclass(frozen=True)
class Contract:
    plugin_name: str
    source_sha256: str
    expected_masters: tuple[str, ...]
    expected_records: int
    expected_rows: int
    rules: tuple[FieldRule, ...]

    @classmethod
    def read(cls, path: Path) -> "Contract":
        raw = json.loads(path.read_text(encoding="utf-8"))
        rules = tuple(FieldRule(**item) for item in raw["fields"])
        if any(rule.table not in {"STRINGS", "DLSTRINGS", "ILSTRINGS"} for rule in rules):
            raise AssertionError("contract has an unknown string-table type")
        keys = [(r.record_type, r.field, r.editor_prefix) for r in rules]
        if len(keys) != len(set(keys)):
            raise AssertionError("contract has duplicate field rules")
        return cls(
            raw["plugin_name"], raw["source_sha256"],
            tuple(raw["expected_masters"]), int(raw["expected_records"]),
            int(raw["expected_rows"]), rules,
        )


@dataclass(frozen=True)
class Translation:
    string_id: int
    form_key: str
    record_type: str
    editor_id: str
    field: str
    occurrence: int
    source: str
    target: str
    provenance: str

    @property
    def key(self) -> tuple[str, str, str, int]:
        return self.form_key, self.record_type, self.field, self.occurrence


@dataclass(frozen=True)
class Subrecord:
    tag: bytes
    payload: bytes
    raw: bytes


@dataclass(frozen=True)
class Record:
    header: bytes
    body: bytes
    path: bytes

    @property
    def signature(self) -> bytes:
        return self.header[:4]

    @property
    def flags(self) -> int:
        return struct.unpack_from("<I", self.header, 8)[0]

    @property
    def raw_form_id(self) -> int:
        return struct.unpack_from("<I", self.header, 12)[0]


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


def decode_inline_text(payload: bytes) -> str:
    raw = payload[:-1] if payload.endswith(b"\0") else payload
    if b"\0" in raw:
        raise AssertionError("inline text contains an embedded NUL")
    return raw.decode("cp1252")


def uncompressed_body(header: bytes, body: bytes) -> bytes:
    flags = struct.unpack_from("<I", header, 8)[0]
    if not flags & COMPRESSED_FLAG:
        return body
    if len(body) < 4:
        raise AssertionError("compressed record is missing its size prefix")
    expected = struct.unpack_from("<I", body)[0]
    result = zlib.decompress(body[4:])
    if len(result) != expected:
        raise AssertionError(f"compressed record size mismatch: {len(result)} != {expected}")
    return result


def compressed_body(header: bytes, body: bytes) -> bytes:
    flags = struct.unpack_from("<I", header, 8)[0]
    if not flags & COMPRESSED_FLAG:
        return body
    return struct.pack("<I", len(body)) + zlib.compress(body, level=9)


def read_translations(path: Path, contract: Contract) -> list[Translation]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != TSV_FIELDS:
            raise AssertionError(f"unexpected translation TSV columns: {reader.fieldnames}")
        rows = [
            Translation(
                int(row["string_id"], 16), row["form_key"], row["record_type"],
                row["editor_id"], row["field"], int(row["occurrence"]),
                row["source"], row["target"], row["provenance"],
            )
            for row in reader
        ]
    if len(rows) != contract.expected_rows:
        raise AssertionError(f"translation row count {len(rows)} != {contract.expected_rows}")
    if [row.string_id for row in rows] != list(range(1, len(rows) + 1)):
        raise AssertionError("string IDs must be sequential in TSV order")
    if len({row.key for row in rows}) != len(rows):
        raise AssertionError("duplicate translation field key")
    if any(not row.provenance.strip() for row in rows):
        raise AssertionError("every translation row needs provenance")
    if any(not row.target and row.source for row in rows):
        raise AssertionError("a non-empty source has a blank target")
    return rows


def tes4_masters(plugin: bytes) -> list[str]:
    if plugin[:4] != b"TES4":
        raise AssertionError("plugin does not begin with TES4")
    size = struct.unpack_from("<I", plugin, 4)[0]
    return [
        decode_zstring(sub.payload)
        for sub in parse_subrecords(plugin[24 : 24 + size])
        if sub.tag == b"MAST"
    ]


def form_key(raw_form_id: int, masters: list[str], plugin_name: str) -> str:
    index = raw_form_id >> 24
    owner = masters[index] if index < len(masters) else plugin_name
    return f"{raw_form_id & 0xFFFFFF:06X}:{owner}"


def record_editor_id(body: bytes) -> str:
    values = [decode_zstring(x.payload) for x in parse_subrecords(body) if x.tag == b"EDID"]
    return values[0] if len(values) == 1 else ""


def matched_rule(contract: Contract, signature: str, field: str, editor_id: str) -> FieldRule | None:
    matches = [
        rule for rule in contract.rules
        if rule.record_type == signature and rule.field == field
        and (not rule.editor_prefix or editor_id.startswith(rule.editor_prefix))
    ]
    if len(matches) > 1:
        raise AssertionError(f"ambiguous field rules for {signature}.{field} {editor_id}")
    return matches[0] if matches else None


@dataclass
class BuildState:
    contract: Contract
    masters: list[str]
    rows: dict[tuple[str, str, str, int], Translation]
    tables: dict[str, list[tuple[int, str]]]
    seen: set[tuple[str, str, str, int]]


def transform_record(header: bytes, stored_body: bytes, state: BuildState) -> bytes:
    signature = header[:4].decode("ascii")
    flags, raw_form_id = struct.unpack_from("<II", header, 8)
    if signature == "TES4":
        changed = bytearray(header)
        struct.pack_into("<I", changed, 8, flags | LOCALIZED_FLAG)
        return bytes(changed) + stored_body

    body = uncompressed_body(header, stored_body)
    editor_id = record_editor_id(body)
    key = form_key(raw_form_id, state.masters, state.contract.plugin_name)
    output = bytearray()
    occurrences: dict[str, int] = {}
    touched = False
    for sub in parse_subrecords(body):
        field = sub.tag.decode("ascii")
        occurrence = occurrences.get(field, 0)
        occurrences[field] = occurrence + 1
        rule = matched_rule(state.contract, signature, field, editor_id)
        if rule is None:
            output += sub.raw
            continue
        row_key = key, signature, field, occurrence
        row = state.rows.get(row_key)
        if row is None:
            raise AssertionError(f"localized field has no TSV row: {row_key}")
        source = decode_inline_text(sub.payload)
        if row.editor_id != editor_id or row.source != source:
            raise AssertionError(
                f"translation source mismatch for {row_key}: "
                f"editor={editor_id!r}, source={source!r}"
            )
        output += encode_subrecord(sub.tag, struct.pack("<I", row.string_id))
        state.tables[rule.table].append((row.string_id, row.target))
        state.seen.add(row_key)
        touched = True

    if not touched:
        return header + stored_body
    new_stored = compressed_body(header, bytes(output))
    changed = bytearray(header)
    struct.pack_into("<I", changed, 4, len(new_stored))
    return bytes(changed) + new_stored


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
    source: bytes, rows: list[Translation], contract: Contract,
) -> tuple[bytes, dict[str, list[tuple[int, str]]]]:
    masters = tes4_masters(source)
    if tuple(masters) != contract.expected_masters:
        raise AssertionError(f"master contract mismatch: {masters}")
    state = BuildState(
        contract, masters, {row.key: row for row in rows},
        {name: [] for name in ("STRINGS", "DLSTRINGS", "ILSTRINGS")}, set(),
    )
    output = transform_region(source, 0, len(source), state)
    if state.seen != set(state.rows):
        missing = sorted(set(state.rows) - state.seen)
        raise AssertionError(f"unused translation rows: {missing[:10]}")
    return output, state.tables


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
            if position + 4 > len(data):
                raise AssertionError("truncated length-prefixed string")
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


def iter_records(plugin: bytes) -> Iterator[Record]:
    def walk(start: int, end: int, path: bytes) -> Iterator[Record]:
        position = start
        while position < end:
            if position + 24 > end:
                raise AssertionError("truncated record/group header")
            header = plugin[position : position + 24]
            size = struct.unpack_from("<I", header, 4)[0]
            if header[:4] == b"GRUP":
                if size < 24 or position + size > end:
                    raise AssertionError("invalid group size")
                marker = header[:4] + header[8:24]
                yield from walk(position + 24, position + size, path + marker)
                position += size
            else:
                record_end = position + 24 + size
                if record_end > end:
                    raise AssertionError("invalid record size")
                yield Record(header, plugin[position + 24 : record_end], path)
                position = record_end
    yield from walk(0, len(plugin), b"")


def normalized_header(header: bytes) -> tuple[bytes, int, int, bytes]:
    flags, raw_form_id = struct.unpack_from("<II", header, 8)
    if header[:4] == b"TES4":
        flags &= ~LOCALIZED_FLAG
    return header[:4], flags, raw_form_id, header[16:24]


def tokens(value: str) -> list[str]:
    placeholders = re.findall(r"<[^<>\s]+>|<[^<>\s]+\)", value)
    without_tags = re.sub(r"<[^<>]+>", "", value)
    without_tags = re.sub(r"<[^<>\s]+\)", "", without_tags)
    numbers = re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?%?", without_tags)
    return sorted(placeholders + numbers)
