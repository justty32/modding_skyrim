#!/usr/bin/env python3
"""Prepare, build, and verify the IFD Lydia 4.2.2 Traditional Chinese overlay."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile
import zlib


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "tools" / "translation-source.json"
MANIFEST = ROOT / "MANIFEST.sha256"
OUTPUT_ESP = ROOT / "ImprovedCompanionsBoogaloo.esp"
OUTPUT_PEX = ROOT / "scripts" / "lydiaconfigscriptnew.pex"

SOURCE_ESP_SHA256 = "b1f7482ba331618aec8194e154f28eb2e0c78c9ca2ce4d2a09e35668c7f85a8d"
SEED_ARCHIVE_SHA256 = "2d2903171f7daec23645c298ac80d13555a9038ddf79b7bd868c002ce7979385"
SOURCE_BSA_SHA256 = "5216db18b82a06362713b398ff8c2d97136a875db7d452bb3d77a1b9ff00416c"
INTERFACE_BSA_SHA256 = "5c8d5275eeaaa87eec84c893da8dc3bf977e0197eba86560bb0d1dc651432957"
TRADITIONAL_TABLE_HASHES = {
    "Skyrim_English.STRINGS": "ae1cd52056ab4b06e44a30a6e0509feeea4f0ddfd186cc5027b6c5af53a14ef4",
    "Skyrim_English.DLSTRINGS": "fd3814b1f2a16b96c6b8adbb18017ad905284435e8a38aaebdbbab904acd0fd5",
    "Skyrim_English.ILSTRINGS": "e71d4a1f07c0fae9c4d07ab5ff8ecc15346ba19a4c4f02f75f81b0d77e2c94d9",
}
SEED_ESP_MEMBER = "ImprovedCompanionsBoogaloo.esp"
SEED_PEX_MEMBER = "scripts/lydiaconfigscriptnew.pex"
SOURCE_PEX_MEMBER = "scripts\\lydiaconfigscriptnew.pex"
EXPECTED_RECORDS = 5708
EXPECTED_PLUGIN_FIELDS = 1794
EXPECTED_PEX_FIELDS = 18
COMPRESSED = 0x00040000
SIMPLE_FORBIDDEN = set("这为后发体龙锻钢轻卫盗贼坚丽风边头术锁护")


PEX_OVERRIDES = {
    82: "萊迪亞對話設定",
    85: "萊迪亞發言頻率",
    88: "將萊迪亞設為必要角色",
    89: "裝備評論",
    90: "其他評論",
    91: "任務評論",
    92: "玩家種族評論",
    93: "浪漫評論",
    94: "技能評論",
    95: "低技能評論",
    96: "地點評論",
    97: "浪漫場景字幕框",
    98: "停用對加入派系的異議",
    99: "停用對侍奉魔神的異議",
    113: "勾選後，玩家將無法殺死萊迪亞。預設只有玩家能殺死她；若其他模組也會變更萊迪亞的保護狀態，請勿啟用。",
    114: "啟用後，萊迪亞不會反對玩家加入盜賊公會、黑暗兄弟會或沃基哈氏族。",
    115: "啟用後，萊迪亞不會反對玩家侍奉梅魯涅斯·大袞、莫拉格·巴爾、梅法拉、波耶西亞、瓦爾迷納或娜米拉。",
    123: "數值越高，引擎層腳本要求萊迪亞發言時，她實際開口的機率就越高。",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


@dataclass(frozen=True)
class Subrecord:
    tag: bytes
    payload: bytes
    raw: bytes


@dataclass(frozen=True)
class Record:
    signature: bytes
    raw_form_id: int
    path: tuple[bytes, ...]
    header: bytes
    body: bytes
    subrecords: tuple[Subrecord, ...]


def parse_subrecords(data: bytes) -> tuple[Subrecord, ...]:
    output: list[Subrecord] = []
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
        output.append(Subrecord(tag, data[position:end], data[start:end]))
        position = end
    return tuple(output)


def encode_subrecord(tag: bytes, payload: bytes) -> bytes:
    if len(tag) != 4:
        raise AssertionError("subrecord tag is not four bytes")
    if len(payload) <= 0xFFFF:
        return tag + struct.pack("<H", len(payload)) + payload
    return b"XXXX\x04\x00" + struct.pack("<I", len(payload)) + tag + b"\x00\x00" + payload


def record_body(header: bytes, stored: bytes) -> bytes:
    if struct.unpack_from("<I", header, 8)[0] & COMPRESSED:
        if len(stored) < 4:
            raise AssertionError("compressed record lacks size prefix")
        expected = struct.unpack_from("<I", stored)[0]
        body = zlib.decompress(stored[4:])
        if len(body) != expected:
            raise AssertionError("compressed record size mismatch")
        return body
    return stored


def iter_records(plugin: bytes) -> list[Record]:
    output: list[Record] = []

    def walk(start: int, end: int, path: tuple[bytes, ...]) -> None:
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
                walk(position + 24, position + size, path + (marker,))
                position += size
            else:
                record_end = position + 24 + size
                if record_end > end:
                    raise AssertionError("invalid record size")
                body = record_body(header, plugin[position + 24 : record_end])
                output.append(Record(
                    header[:4], struct.unpack_from("<I", header, 12)[0], path,
                    header, body, parse_subrecords(body),
                ))
                position = record_end
        if position != end:
            raise AssertionError("record walk did not end on boundary")

    walk(0, len(plugin), ())
    return output


def semantic_header(header: bytes) -> bytes:
    return header[:4] + header[8:24]


def canonical_zstring(payload: bytes, encoding: str) -> str:
    if not payload.endswith(b"\0") or b"\0" in payload[:-1]:
        raise AssertionError("changed payload is not a canonical zstring")
    return payload[:-1].decode(encoding)


def plugin_identity(record: Record, subrecord_index: int) -> str:
    return f"{record.signature.decode('ascii')}:{record.raw_form_id:08X}:{subrecord_index}"


def compare_plugins(source: bytes, seed: bytes) -> list[dict[str, object]]:
    source_records = iter_records(source)
    seed_records = iter_records(seed)
    if len(source_records) != EXPECTED_RECORDS or len(seed_records) != EXPECTED_RECORDS:
        raise AssertionError("unexpected record count")
    output: list[dict[str, object]] = []
    for left, right in zip(source_records, seed_records):
        if (left.signature, left.raw_form_id, left.path) != (right.signature, right.raw_form_id, right.path):
            raise AssertionError("record identity/order/GRUP path differs")
        if semantic_header(left.header) != semantic_header(right.header):
            raise AssertionError(f"record header differs: {left.signature!r} {left.raw_form_id:08X}")
        if [s.tag for s in left.subrecords] != [s.tag for s in right.subrecords]:
            raise AssertionError(f"subrecord topology differs: {left.signature!r} {left.raw_form_id:08X}")
        for index, (source_sub, seed_sub) in enumerate(zip(left.subrecords, right.subrecords)):
            if source_sub.payload == seed_sub.payload:
                continue
            source_text = canonical_zstring(source_sub.payload, "cp1252")
            seed_text = canonical_zstring(seed_sub.payload, "utf-8")
            output.append({
                "identity": plugin_identity(left, index),
                "signature": left.signature.decode("ascii"),
                "raw_form_id": f"{left.raw_form_id:08X}",
                "subrecord_index": index,
                "tag": source_sub.tag.decode("ascii"),
                "source": source_text,
                "seed": seed_text,
            })
    if len(output) != EXPECTED_PLUGIN_FIELDS:
        raise AssertionError(f"changed plugin field count {len(output)} != {EXPECTED_PLUGIN_FIELDS}")
    return output


def pex_parse(data: bytes) -> tuple[list[bytes], list[bytes], int, bytes]:
    if data[:4] != bytes.fromhex("fa 57 c0 de") or data[4:8] != bytes.fromhex("03 02 00 01"):
        raise AssertionError("not a Skyrim PEX 3.2 file")
    position = 16

    def read_string() -> bytes:
        nonlocal position
        if position + 2 > len(data):
            raise AssertionError("truncated PEX string length")
        size = int.from_bytes(data[position : position + 2], "big")
        position += 2
        end = position + size
        if end > len(data):
            raise AssertionError("truncated PEX string")
        value = data[position:end]
        position = end
        return value

    prestrings = [read_string() for _ in range(3)]
    count_position = position
    count = int.from_bytes(data[position : position + 2], "big")
    position += 2
    strings = [read_string() for _ in range(count)]
    return prestrings, strings, count_position, data[position:]


def compare_pex(source: bytes, seed: bytes) -> list[dict[str, object]]:
    source_pre, source_strings, _, source_tail = pex_parse(source)
    seed_pre, seed_strings, _, seed_tail = pex_parse(seed)
    if source[:16] != seed[:16] or source_pre != seed_pre:
        raise AssertionError("PEX header/prestrings differ")
    if len(source_strings) != len(seed_strings) or source_tail != seed_tail:
        raise AssertionError("PEX declaration/bytecode contract differs")
    output = []
    for index, (left, right) in enumerate(zip(source_strings, seed_strings)):
        if left == right:
            continue
        output.append({
            "index": index,
            "source": left.decode("cp1252"),
            "seed": right.decode("utf-8"),
            "target": PEX_OVERRIDES[index],
            "provenance": "manual Traditional Chinese MCM edit",
        })
    if len(output) != EXPECTED_PEX_FIELDS or set(PEX_OVERRIDES) != {row["index"] for row in output}:
        raise AssertionError("unexpected PEX string-table delta")
    return output


def bsa_members(data: bytes) -> tuple[int, list[tuple[str, int, int]]]:
    magic, version, folder_offset, flags, folder_count, file_count, _, _, _ = struct.unpack_from(
        "<4s8I", data, 0
    )
    if magic != b"BSA\0" or version != 105:
        raise AssertionError("only Skyrim SE BSA v105 is supported")
    position = folder_offset + folder_count * 24
    entries: list[list[object]] = []
    for index in range(folder_count):
        _, count, _, _ = struct.unpack_from("<QIIQ", data, folder_offset + index * 24)
        name_size = data[position]
        position += 1
        folder = data[position : position + name_size].rstrip(b"\0").decode("utf-8")
        position += name_size
        for _ in range(count):
            _, size, offset = struct.unpack_from("<QII", data, position)
            position += 16
            entries.append([folder, size, offset, ""])
    if len(entries) != file_count:
        raise AssertionError("BSA file count mismatch")
    for entry in entries:
        end = data.index(b"\0", position)
        entry[3] = data[position:end].decode("utf-8")
        position = end + 1
    return flags, [
        (f"{folder}\\{name}", int(size), int(offset))
        for folder, size, offset, name in entries
    ]


def bsa_member(data: bytes, wanted: str) -> bytes:
    flags, entries = bsa_members(data)
    for name, size_field, offset in entries:
        if name.casefold() != wanted.casefold():
            continue
        size = size_field & 0x3FFFFFFF
        payload = data[offset : offset + size]
        compressed = bool(flags & 0x4) ^ bool(size_field & 0x40000000)
        if compressed:
            expected = struct.unpack_from("<I", payload)[0]
            payload = zlib.decompress(payload[4:])
            if len(payload) != expected:
                raise AssertionError("BSA member decompressed size mismatch")
        return payload
    raise AssertionError(f"BSA member not found: {wanted}")


def decode_strings(data: bytes, *, length_prefixed: bool) -> dict[int, str]:
    count, data_size = struct.unpack_from("<II", data)
    data_start = 8 + count * 8
    if data_start + data_size != len(data):
        raise AssertionError("STRINGS size mismatch")
    output: dict[int, str] = {}
    for index in range(count):
        string_id, offset = struct.unpack_from("<II", data, 8 + index * 8)
        position = data_start + offset
        if length_prefixed:
            size = struct.unpack_from("<I", data, position)[0]
            raw = data[position + 4 : position + 4 + size]
            if not raw.endswith(b"\0"):
                raise AssertionError("unterminated length-prefixed string")
            raw = raw[:-1]
        else:
            end = data.index(b"\0", position)
            raw = data[position:end]
        output[string_id] = raw.decode("utf-8")
    return output


def vanilla_translation_map(interface_bsa: bytes, traditional_dir: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    conflicts: set[str] = set()
    for extension, length_prefixed in (
        ("STRINGS", False), ("DLSTRINGS", True), ("ILSTRINGS", True),
    ):
        filename = f"Skyrim_English.{extension}"
        traditional_path = traditional_dir / filename
        expected = TRADITIONAL_TABLE_HASHES[filename]
        if sha256(traditional_path) != expected:
            raise AssertionError(f"Traditional table hash mismatch: {filename}")
        english = decode_strings(
            bsa_member(interface_bsa, f"strings\\skyrim_english.{extension.lower()}"),
            length_prefixed=length_prefixed,
        )
        traditional = decode_strings(traditional_path.read_bytes(), length_prefixed=length_prefixed)
        if set(english) != set(traditional):
            raise AssertionError(f"vanilla string-id set mismatch: {extension}")
        for string_id, source in english.items():
            target = traditional[string_id]
            if source in mapping and mapping[source] != target:
                conflicts.add(source)
            else:
                mapping[source] = target
    for source in conflicts:
        mapping.pop(source, None)
    return mapping


def normalize_terminology(text: str) -> str:
    replacements = {
        "天際": "天霜",
        "武衛": "男爵",
        "模塊": "模組",
        "莉迪亞": "萊迪亞",
        "默認": "預設",
        "設置": "設定",
        "軟件": "軟體",
        "鼠標": "滑鼠",
        "文件": "檔案",
        "數據": "資料",
        "信息": "資訊",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def seed_archive_members(path: Path) -> tuple[bytes, bytes]:
    if sha256(path) != SEED_ARCHIVE_SHA256:
        raise AssertionError("CHS seed archive hash mismatch")
    with zipfile.ZipFile(path) as archive:
        return archive.read(SEED_ESP_MEMBER), archive.read(SEED_PEX_MEMBER)


def load_ledger() -> dict[str, object]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if ledger.get("schema") != 1:
        raise AssertionError("translation ledger schema mismatch")
    if len(ledger.get("plugin", [])) != EXPECTED_PLUGIN_FIELDS:
        raise AssertionError("translation ledger plugin count mismatch")
    if len(ledger.get("pex", [])) != EXPECTED_PEX_FIELDS:
        raise AssertionError("translation ledger PEX count mismatch")
    return ledger


def prepare(args: argparse.Namespace) -> None:
    source_esp = args.source_esp.read_bytes()
    if sha256_bytes(source_esp) != SOURCE_ESP_SHA256:
        raise AssertionError("official ESP hash mismatch")
    seed_esp, seed_pex = seed_archive_members(args.seed_archive)
    plugin_rows = compare_plugins(source_esp, seed_esp)

    if sha256(args.source_bsa) != SOURCE_BSA_SHA256:
        raise AssertionError("official BSA hash mismatch")
    source_pex = bsa_member(args.source_bsa.read_bytes(), SOURCE_PEX_MEMBER)
    pex_rows = compare_pex(source_pex, seed_pex)

    if sha256(args.interface_bsa) != INTERFACE_BSA_SHA256:
        raise AssertionError("Skyrim Interface BSA hash mismatch")
    vanilla = vanilla_translation_map(args.interface_bsa.read_bytes(), args.traditional_strings)

    try:
        from opencc import OpenCC
    except ImportError as error:
        raise AssertionError("prepare requires python-opencc") from error
    converter = OpenCC("s2tw")
    for row in plugin_rows:
        source = str(row["source"])
        if source in vanilla:
            row["target"] = vanilla[source]
            row["provenance"] = "Skyrim Traditional Chinese 8.20 exact English-text match"
        else:
            row["target"] = normalize_terminology(converter.convert(str(row["seed"])))
            row["provenance"] = "IFD Lydia CHS 4.2.2 + OpenCC s2tw + terminology normalization"
        if not row["target"]:
            raise AssertionError(f"empty target: {row['identity']}")

    ledger = {
        "schema": 1,
        "plugin": plugin_rows,
        "pex": pex_rows,
    }
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = Counter(row["provenance"] for row in plugin_rows)
    print(f"wrote {LEDGER}: {len(plugin_rows)} plugin fields + {len(pex_rows)} PEX strings")
    for name, count in sorted(counts.items()):
        print(f"  {count}: {name}")


def build_plugin(source: bytes, rows: list[dict[str, object]]) -> bytes:
    wanted = {str(row["identity"]): row for row in rows}
    seen: set[str] = set()

    def transform_region(start: int, end: int) -> bytes:
        output = bytearray()
        position = start
        while position < end:
            header = source[position : position + 24]
            size = struct.unpack_from("<I", header, 4)[0]
            if header[:4] == b"GRUP":
                children = transform_region(position + 24, position + size)
                changed = bytearray(header)
                struct.pack_into("<I", changed, 4, 24 + len(children))
                output += changed + children
                position += size
                continue

            record_end = position + 24 + size
            stored = source[position + 24 : record_end]
            signature = header[:4].decode("ascii")
            raw_form_id = struct.unpack_from("<I", header, 12)[0]
            prefix = f"{signature}:{raw_form_id:08X}:"
            applicable = {key: row for key, row in wanted.items() if key.startswith(prefix)}
            if not applicable:
                output += source[position:record_end]
                position = record_end
                continue

            body = record_body(header, stored)
            subs = parse_subrecords(body)
            changed_body = bytearray()
            for index, sub in enumerate(subs):
                identity = f"{prefix}{index}"
                row = applicable.get(identity)
                if row is None:
                    changed_body += sub.raw
                    continue
                if sub.tag.decode("ascii") != row["tag"]:
                    raise AssertionError(f"tag mismatch: {identity}")
                if canonical_zstring(sub.payload, "cp1252") != row["source"]:
                    raise AssertionError(f"source text mismatch: {identity}")
                changed_body += encode_subrecord(sub.tag, str(row["target"]).encode("utf-8") + b"\0")
                seen.add(identity)

            if struct.unpack_from("<I", header, 8)[0] & COMPRESSED:
                stored_output = struct.pack("<I", len(changed_body)) + zlib.compress(bytes(changed_body), level=9)
            else:
                stored_output = bytes(changed_body)
            changed_header = bytearray(header)
            struct.pack_into("<I", changed_header, 4, len(stored_output))
            output += changed_header + stored_output
            position = record_end
        return bytes(output)

    result = transform_region(0, len(source))
    if seen != set(wanted):
        raise AssertionError(f"unused plugin ledger entries: {sorted(set(wanted) - seen)[:10]}")
    return result


def build_pex(source: bytes, rows: list[dict[str, object]]) -> bytes:
    _, strings, count_position, tail = pex_parse(source)
    wanted = {int(row["index"]): row for row in rows}
    output = bytearray(source[:count_position])
    output += len(strings).to_bytes(2, "big")
    for index, value in enumerate(strings):
        if index in wanted:
            row = wanted[index]
            if value.decode("cp1252") != row["source"]:
                raise AssertionError(f"PEX source mismatch at string {index}")
            value = str(row["target"]).encode("utf-8")
        output += len(value).to_bytes(2, "big") + value
    output += tail
    return bytes(output)


def build(args: argparse.Namespace) -> None:
    source = args.source_esp.read_bytes()
    if sha256_bytes(source) != SOURCE_ESP_SHA256:
        raise AssertionError("official ESP hash mismatch")
    if sha256(args.source_bsa) != SOURCE_BSA_SHA256:
        raise AssertionError("official BSA hash mismatch")
    ledger = load_ledger()
    source_pex = bsa_member(args.source_bsa.read_bytes(), SOURCE_PEX_MEMBER)
    OUTPUT_ESP.write_bytes(build_plugin(source, list(ledger["plugin"])))
    OUTPUT_PEX.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PEX.write_bytes(build_pex(source_pex, list(ledger["pex"])))
    print(f"wrote {OUTPUT_ESP} ({OUTPUT_ESP.stat().st_size} bytes)")
    print(f"wrote {OUTPUT_PEX} ({OUTPUT_PEX.stat().st_size} bytes)")


def verify_plugin(source: bytes, output: bytes, rows: list[dict[str, object]]) -> None:
    source_records = iter_records(source)
    output_records = iter_records(output)
    wanted = {str(row["identity"]): row for row in rows}
    seen: set[str] = set()
    if len(source_records) != EXPECTED_RECORDS or len(output_records) != EXPECTED_RECORDS:
        raise AssertionError("record count changed")
    for left, right in zip(source_records, output_records):
        if (left.signature, left.raw_form_id, left.path) != (right.signature, right.raw_form_id, right.path):
            raise AssertionError("record identity/order/GRUP topology changed")
        if semantic_header(left.header) != semantic_header(right.header):
            raise AssertionError("record flags/FormID/version bytes changed")
        if [s.tag for s in left.subrecords] != [s.tag for s in right.subrecords]:
            raise AssertionError("subrecord topology changed")
        for index, (source_sub, output_sub) in enumerate(zip(left.subrecords, right.subrecords)):
            identity = plugin_identity(left, index)
            row = wanted.get(identity)
            if row is None:
                if source_sub.raw != output_sub.raw:
                    raise AssertionError(f"non-text payload changed: {identity}")
                continue
            if source_sub.tag.decode("ascii") != row["tag"]:
                raise AssertionError(f"ledger tag mismatch: {identity}")
            if canonical_zstring(source_sub.payload, "cp1252") != row["source"]:
                raise AssertionError(f"ledger source mismatch: {identity}")
            if canonical_zstring(output_sub.payload, "utf-8") != row["target"]:
                raise AssertionError(f"target mismatch: {identity}")
            seen.add(identity)
    if seen != set(wanted):
        raise AssertionError("plugin ledger coverage mismatch")
    print("PASS plugin semantic delta: 5,708 records; exact topology/headers; only 1,794 ledgered zstrings changed")


def verify_pex(source: bytes, output: bytes, rows: list[dict[str, object]]) -> None:
    source_pre, source_strings, _, source_tail = pex_parse(source)
    output_pre, output_strings, _, output_tail = pex_parse(output)
    if source[:16] != output[:16] or source_pre != output_pre or source_tail != output_tail:
        raise AssertionError("PEX header/declarations/bytecode changed")
    wanted = {int(row["index"]): row for row in rows}
    for index, (left, right) in enumerate(zip(source_strings, output_strings)):
        if index in wanted:
            row = wanted[index]
            if left.decode("cp1252") != row["source"] or right.decode("utf-8") != row["target"]:
                raise AssertionError(f"PEX ledger mismatch at string {index}")
        elif left != right:
            raise AssertionError(f"unlisted PEX string changed at index {index}")
    print("PASS PEX semantic delta: 128 string slots; 18 display strings changed; 3,986-byte declaration/bytecode tail identical")


def verify_manifest() -> None:
    if not MANIFEST.exists():
        print("SKIP manifest: MANIFEST.sha256 not present")
        return
    listed: set[str] = set()
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if "  " not in line:
            raise AssertionError(f"malformed manifest line {number}")
        expected, relative = line.split("  ", 1)
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents or sha256(path) != expected:
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


def write_manifest(_: argparse.Namespace) -> None:
    paths = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and path.name != MANIFEST.name and "__pycache__" not in path.parts
    )
    lines = [f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in paths]
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST}: {len(paths)} files")


def verify(args: argparse.Namespace) -> None:
    source = args.source_esp.read_bytes()
    if sha256_bytes(source) != SOURCE_ESP_SHA256:
        raise AssertionError("official ESP hash mismatch")
    if sha256(args.source_bsa) != SOURCE_BSA_SHA256:
        raise AssertionError("official BSA hash mismatch")
    ledger = load_ledger()
    source_pex = bsa_member(args.source_bsa.read_bytes(), SOURCE_PEX_MEMBER)
    expected_esp = build_plugin(source, list(ledger["plugin"]))
    expected_pex = build_pex(source_pex, list(ledger["pex"]))
    if OUTPUT_ESP.read_bytes() != expected_esp or OUTPUT_PEX.read_bytes() != expected_pex:
        raise AssertionError("packaged payload is not a byte-identical fresh rebuild")
    print("PASS reproducibility: packaged ESP/PEX equal a fresh in-memory rebuild")
    verify_plugin(source, expected_esp, list(ledger["plugin"]))
    verify_pex(source_pex, expected_pex, list(ledger["pex"]))

    targets = [str(row["target"]) for row in ledger["plugin"]] + [str(row["target"]) for row in ledger["pex"]]
    offenders = sorted({char for value in targets for char in value if char in SIMPLE_FORBIDDEN})
    if offenders:
        raise AssertionError(f"common Simplified Chinese glyphs remain: {offenders}")
    if any("\ufffd" in value or "???" in value for value in targets):
        raise AssertionError("replacement/mojibake sentinel found")
    token_pattern = re.compile(r"<[^>]+>|\[[A-Za-z]+\]|\\n|%\d*\$?[A-Za-z]|\{[^{}]+\}")
    for row in ledger["plugin"]:
        if sorted(token_pattern.findall(str(row["source"]))) != sorted(token_pattern.findall(str(row["target"]))):
            raise AssertionError(f"markup/control token mismatch: {row['identity']}")
    counts = Counter(row["provenance"] for row in ledger["plugin"])
    print(f"PASS text ledger: {len(targets)} targets; UTF-8; markup/control tokens preserved; no common Simplified glyphs; provenance={dict(counts)}")
    verify_manifest()
    print("RESULT: PASS")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    sub = result.add_subparsers(dest="command", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--source-esp", type=Path, required=True)
    common.add_argument("--source-bsa", type=Path, required=True)

    prepare_parser = sub.add_parser("prepare", parents=[common])
    prepare_parser.add_argument("--seed-archive", type=Path, required=True)
    prepare_parser.add_argument("--interface-bsa", type=Path, required=True)
    prepare_parser.add_argument("--traditional-strings", type=Path, required=True)
    prepare_parser.set_defaults(function=prepare)

    build_parser = sub.add_parser("build", parents=[common])
    build_parser.set_defaults(function=build)
    verify_parser = sub.add_parser("verify", parents=[common])
    verify_parser.set_defaults(function=verify)
    manifest_parser = sub.add_parser("manifest")
    manifest_parser.set_defaults(function=write_manifest)
    return result


if __name__ == "__main__":
    arguments = parser().parse_args()
    arguments.function(arguments)
