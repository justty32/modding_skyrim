"""Build text-only overlays from an exact source ESP and a versioned translation seed."""

from __future__ import annotations

import collections
import importlib.util
import re
import struct
import sys
import zlib
from pathlib import Path

from opencc import OpenCC


REPO = Path(__file__).resolve().parents[1]
PARSER = REPO / "dist/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/tools/translation_pipeline.py"
LOCALIZABLE_TAGS = {b"FULL", b"DESC", b"NAM1", b"RNAM", b"ITXT", b"MNAM", b"DNAM", b"CNAM", b"FNAM", b"NNAM", b"SHRT"}
COMPRESSED = 0x00040000
TOKEN_RE = re.compile(r"<[^<>]+>|%[^%\s]+%|\$[A-Za-z0-9_]+|\\[nrt]|\{[^{}]+\}")


def _load_parser():
    spec = importlib.util.spec_from_file_location("inline_translation_parser", PARSER)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load shared plugin parser")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TP = _load_parser()


def _zstring(payload: bytes, encoding: str) -> str | None:
    try:
        return TP.canonical_zstring(payload, encoding)
    except (AssertionError, UnicodeError, ValueError):
        return None


def has_han(value: str) -> bool:
    return any("\u3400" <= char <= "\u9fff" for char in value)


def collect_seed_rows(source: bytes, seed: bytes, *, provenance: str,
                      manual: dict[tuple[str, int, str, int], str] | None = None,
                      converter: str = "s2twp") -> list[dict[str, object]]:
    """Match translated fields by stable record identity plus tag occurrence."""
    manual = manual or {}
    convert = OpenCC(converter).convert
    seed_records = {(record.signature, record.raw_form_id): record for record in TP.iter_records(seed)}
    rows = []
    for record in TP.iter_records(source):
        seed_record = seed_records.get((record.signature, record.raw_form_id))
        seed_fields: dict[tuple[bytes, int], tuple[int, str]] = {}
        if seed_record is not None:
            occurrences: collections.Counter[bytes] = collections.Counter()
            for index, subrecord in enumerate(seed_record.subrecords):
                if subrecord.tag not in LOCALIZABLE_TAGS:
                    continue
                occurrence = occurrences[subrecord.tag]
                occurrences[subrecord.tag] += 1
                value = _zstring(subrecord.payload, "utf-8")
                if value is not None:
                    seed_fields[(subrecord.tag, occurrence)] = (index, value)

        occurrences = collections.Counter()
        for index, subrecord in enumerate(record.subrecords):
            if subrecord.tag not in LOCALIZABLE_TAGS:
                continue
            occurrence = occurrences[subrecord.tag]
            occurrences[subrecord.tag] += 1
            source_text = _zstring(subrecord.payload, "cp1252")
            if not source_text:
                continue
            identity = (record.signature.decode(), record.raw_form_id, subrecord.tag.decode(), occurrence)
            manual_target = manual.get(identity)
            seed_value = seed_fields.get((subrecord.tag, occurrence))
            if manual_target is not None:
                target_text = manual_target
                seed_index = None if seed_value is None else seed_value[0]
                field_provenance = f"{provenance}; manually reviewed target"
                manually_reviewed = True
            elif seed_value is not None and has_han(seed_value[1]):
                seed_index, seed_text = seed_value
                target_text = convert(seed_text)
                field_provenance = f"{provenance}; OpenCC {converter}"
                manually_reviewed = False
            else:
                continue
            if target_text == source_text:
                continue
            if not target_text or "\ufffd" in target_text or "???" in target_text:
                raise AssertionError(f"invalid target: {identity}")
            if sorted(TOKEN_RE.findall(source_text)) != sorted(TOKEN_RE.findall(target_text)):
                if manually_reviewed:
                    raise AssertionError(f"control-token mismatch: {identity}")
                continue
            if source_text.count("\n") != target_text.count("\n"):
                if manually_reviewed:
                    raise AssertionError(f"newline mismatch: {identity}")
                continue
            rows.append({
                "identity": f"{identity[0]}:{identity[1]:08X}:{identity[2]}:{identity[3]}",
                "signature": identity[0],
                "raw_form_id": f"{identity[1]:08X}",
                "tag": identity[2],
                "tag_occurrence": identity[3],
                "source_subrecord_index": index,
                "seed_subrecord_index": seed_index,
                "source": source_text,
                "target": target_text,
                "provenance": field_provenance,
            })
    return rows


def _replace_subrecords(body: bytes, replacements: dict[tuple[bytes, int], bytes]) -> tuple[bytes, bool]:
    output = bytearray()
    occurrences: collections.Counter[bytes] = collections.Counter()
    position = 0
    changed = False
    while position < len(body):
        start = position
        if position + 6 > len(body):
            raise AssertionError("truncated subrecord header")
        tag = body[position : position + 4]
        size = struct.unpack_from("<H", body, position + 4)[0]
        position += 6
        extended = tag == b"XXXX"
        if extended:
            if size != 4 or position + 10 > len(body):
                raise AssertionError("malformed XXXX subrecord")
            size = struct.unpack_from("<I", body, position)[0]
            position += 4
            tag = body[position : position + 4]
            position += 6
        payload_end = position + size
        if payload_end > len(body):
            raise AssertionError("truncated subrecord payload")
        occurrence = occurrences[tag]
        occurrences[tag] += 1
        replacement = replacements.get((tag, occurrence))
        if replacement is None:
            output.extend(body[start:payload_end])
        else:
            prefix = bytearray(body[start:position])
            if extended:
                struct.pack_into("<I", prefix, 6, len(replacement))
            else:
                if len(replacement) > 0xFFFF:
                    raise AssertionError("replacement needs an XXXX header")
                struct.pack_into("<H", prefix, 4, len(replacement))
            output.extend(prefix)
            output.extend(replacement)
            changed = changed or replacement != body[position:payload_end]
        position = payload_end
    return bytes(output), changed


def transform_plugin(source: bytes, rows: list[dict[str, object]]) -> bytes:
    replacements: dict[tuple[bytes, int], dict[tuple[bytes, int], bytes]] = {}
    for row in rows:
        record_key = (str(row["signature"]).encode(), int(str(row["raw_form_id"]), 16))
        field_key = (str(row["tag"]).encode(), int(row["tag_occurrence"]))
        replacements.setdefault(record_key, {})[field_key] = str(row["target"]).encode("utf-8") + b"\0"

    def walk(start: int, end: int) -> bytes:
        output = bytearray()
        position = start
        while position < end:
            if position + 24 > end:
                raise AssertionError("truncated record/group header")
            header = bytearray(source[position : position + 24])
            size = struct.unpack_from("<I", header, 4)[0]
            if header[:4] == b"GRUP":
                if size < 24 or position + size > end:
                    raise AssertionError("invalid GRUP size")
                children = walk(position + 24, position + size)
                struct.pack_into("<I", header, 4, 24 + len(children))
                output.extend(header)
                output.extend(children)
                position += size
                continue

            record_end = position + 24 + size
            if record_end > end:
                raise AssertionError("invalid record size")
            key = (bytes(header[:4]), struct.unpack_from("<I", header, 12)[0])
            record_replacements = replacements.get(key)
            if not record_replacements:
                output.extend(source[position:record_end])
                position = record_end
                continue
            stored = source[position + 24 : record_end]
            flags = struct.unpack_from("<I", header, 8)[0]
            if flags & COMPRESSED:
                expected = struct.unpack_from("<I", stored)[0]
                body = zlib.decompress(stored[4:])
                if len(body) != expected:
                    raise AssertionError("compressed record size mismatch")
            else:
                body = stored
            new_body, changed = _replace_subrecords(body, record_replacements)
            if not changed:
                output.extend(source[position:record_end])
                position = record_end
                continue
            if flags & COMPRESSED:
                new_stored = struct.pack("<I", len(new_body)) + zlib.compress(new_body, 9)
            else:
                new_stored = new_body
            struct.pack_into("<I", header, 4, len(new_stored))
            output.extend(header)
            output.extend(new_stored)
            position = record_end
        return bytes(output)

    return walk(0, len(source))


def verify_overlay(source: bytes, output: bytes, rows: list[dict[str, object]]) -> None:
    expected = {(str(row["signature"]), str(row["raw_form_id"]), int(row["source_subrecord_index"])): str(row["target"])
                for row in rows}
    left = TP.iter_records(source)
    right = TP.iter_records(output)
    if len(left) != len(right):
        raise AssertionError("record count changed")
    observed = set()
    for a, b in zip(left, right):
        if (a.signature, a.raw_form_id, a.path) != (b.signature, b.raw_form_id, b.path):
            raise AssertionError("record identity/order/group path changed")
        if TP.semantic_header(a.header) != TP.semantic_header(b.header):
            raise AssertionError(f"semantic header changed: {a.raw_form_id:08X}")
        if [item.tag for item in a.subrecords] != [item.tag for item in b.subrecords]:
            raise AssertionError(f"subrecord topology changed: {a.raw_form_id:08X}")
        for index, (x, y) in enumerate(zip(a.subrecords, b.subrecords)):
            key = (a.signature.decode(), f"{a.raw_form_id:08X}", index)
            target = expected.get(key)
            if target is None:
                if x.payload != y.payload:
                    raise AssertionError(f"unexpected nontext delta: {key}")
                continue
            if y.payload != target.encode("utf-8") + b"\0":
                raise AssertionError(f"target did not land: {key}")
            observed.add(key)
    if observed != set(expected):
        raise AssertionError(f"overlay coverage mismatch: {len(observed)} != {len(expected)}")
