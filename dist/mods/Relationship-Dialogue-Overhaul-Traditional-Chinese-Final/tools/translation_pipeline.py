#!/usr/bin/env python3
"""Build and verify the RDO Final Traditional Chinese text-only overlay."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import struct
import sys
import zipfile
import zlib
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ESP = ROOT / "Relationship Dialogue Overhaul.esp"
OUTPUT_SCRIPTS = ROOT / "scripts"
LEDGER = ROOT / "tools" / "translation-source.json"
MANIFEST = ROOT / "MANIFEST.sha256"

SOURCE_ESP_SHA256 = "b8d33bd731dded257b517402135cc7ba69be8d7e2b2cc8f038481802b363c2d0"
SOURCE_BSA_SHA256 = "40e20585512cc5fe796faab112863592a5549165fd378d5d14a098652207be42"
SEED_ARCHIVE_SHA256 = "45271a07353ef99bac7ecff6cbf19da59afec17bdfc8f2f3cb2db43fafbbafd5"
SEED_ESP_MEMBER = "Relationship Dialogue Overhaul.esp"
EXPECTED_RECORDS = 9766
EXPECTED_FIELDS = 4071
EXPECTED_TAGS = {
    "CNAM": 1,
    "DESC": 13,
    "DNAM": 11,
    "FULL": 180,
    "MNAM": 1,
    "NAM1": 3776,
    "NNAM": 16,
    "RNAM": 72,
    "SHRT": 1,
}
COMPRESSED = 0x00040000
TOKEN_RE = re.compile(r"<[^<>]+>|%[^%\s]+%|\$[A-Za-z0-9_]+|\\[nrt]")
FORBIDDEN_SIMPLE = set("这为后发体龙锻钢轻卫盗贼坚丽风边头术锁护")
TOKEN_SOURCE = "Do you remember now? (<bribecost> gold)"
TOKEN_SEED = "你還記得嗎？（賄賂<BribeCost>枚金幣）"
TOKEN_TARGET = "你還記得嗎？（賄賂<bribecost>枚金幣）"

PEX_FIELDS = {
    "rdo_geleborfolloweraliasscript.pex": (48, "Gelebor is still waiting for you", "加拉伯爾仍在等著你"),
    "rdo_geleborfollowerscript.pex": (62, "Gelebor leaves your service.", "加拉伯爾不再為你效力。"),
    "rdo_isranfolloweraliasscript.pex": (33, "Isran is still waiting for you", "伊瑟倫仍在等著你"),
    "rdo_isranfollowerscript.pex": (69, "Isran leaves your service", "伊瑟倫不再為你效力"),
    "rdo_valericafolloweraliasscript.pex": (35, "Valerica is still waiting for you", "維爾瑞卡仍在等著你"),
    "rdo_valericafollowerscript.pex": (75, "Valerica leaves your service", "維爾瑞卡不再為你效力"),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


@dataclass(frozen=True)
class Subrecord:
    tag: bytes
    payload: bytes


@dataclass(frozen=True)
class Record:
    signature: bytes
    raw_form_id: int
    path: tuple[bytes, ...]
    header: bytes
    subrecords: tuple[Subrecord, ...]


def parse_subrecords(data: bytes) -> tuple[Subrecord, ...]:
    output = []
    position = 0
    while position < len(data):
        if position + 6 > len(data):
            raise AssertionError("truncated subrecord header")
        tag = data[position : position + 4]
        size = struct.unpack_from("<H", data, position + 4)[0]
        position += 6
        if tag == b"XXXX":
            if size != 4 or position + 10 > len(data):
                raise AssertionError("malformed XXXX subrecord")
            size = struct.unpack_from("<I", data, position)[0]
            position += 4
            tag = data[position : position + 4]
            position += 6
        end = position + size
        if end > len(data):
            raise AssertionError("truncated subrecord payload")
        output.append(Subrecord(tag, data[position:end]))
        position = end
    return tuple(output)


def record_body(header: bytes, stored: bytes) -> bytes:
    if struct.unpack_from("<I", header, 8)[0] & COMPRESSED:
        expected = struct.unpack_from("<I", stored)[0]
        body = zlib.decompress(stored[4:])
        if len(body) != expected:
            raise AssertionError("compressed record size mismatch")
        return body
    return stored


def iter_records(plugin: bytes) -> list[Record]:
    output = []

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
                    header[:4],
                    struct.unpack_from("<I", header, 12)[0],
                    path,
                    header,
                    parse_subrecords(body),
                ))
                position = record_end
        if position != end:
            raise AssertionError("record walk ended off boundary")

    walk(0, len(plugin), ())
    return output


def semantic_header(header: bytes) -> bytes:
    return header[:4] + header[8:24]


def canonical_zstring(payload: bytes, encoding: str) -> str:
    if not payload.endswith(b"\0") or b"\0" in payload[:-1]:
        raise AssertionError("changed payload is not a canonical zstring")
    return payload[:-1].decode(encoding)


def plugin_rows(source: bytes, target: bytes) -> list[dict[str, object]]:
    source_records = iter_records(source)
    target_records = iter_records(target)
    if len(source_records) != EXPECTED_RECORDS or len(target_records) != EXPECTED_RECORDS:
        raise AssertionError("unexpected record count")
    rows = []
    tags = collections.Counter()
    for left, right in zip(source_records, target_records):
        if (left.signature, left.raw_form_id, left.path) != (right.signature, right.raw_form_id, right.path):
            raise AssertionError("record identity/order/GRUP path differs")
        if semantic_header(left.header) != semantic_header(right.header):
            raise AssertionError(f"record header differs: {left.signature!r} {left.raw_form_id:08X}")
        if [x.tag for x in left.subrecords] != [x.tag for x in right.subrecords]:
            raise AssertionError(f"subrecord topology differs: {left.signature!r} {left.raw_form_id:08X}")
        for index, (a, b) in enumerate(zip(left.subrecords, right.subrecords)):
            if a.payload == b.payload:
                continue
            source_text = canonical_zstring(a.payload, "cp1252")
            target_text = canonical_zstring(b.payload, "utf-8")
            if source_text == TOKEN_SOURCE:
                if target_text != TOKEN_TARGET:
                    raise AssertionError("bribecost token correction missing")
                provenance = "RDO Final CHT + exact engine-token case correction"
            else:
                provenance = "RDO Final CHT"
            if collections.Counter(TOKEN_RE.findall(source_text)) != collections.Counter(TOKEN_RE.findall(target_text)):
                raise AssertionError(f"control token mismatch: {left.raw_form_id:08X}:{index}")
            if source_text.count("\n") != target_text.count("\n"):
                raise AssertionError(f"newline mismatch: {left.raw_form_id:08X}:{index}")
            if not target_text or "\ufffd" in target_text or "???" in target_text:
                raise AssertionError(f"invalid target text: {left.raw_form_id:08X}:{index}")
            bad = sorted(set(target_text) & FORBIDDEN_SIMPLE)
            if bad:
                raise AssertionError(f"common Simplified glyphs remain: {bad}")
            tag = a.tag.decode("ascii")
            tags[tag] += 1
            rows.append({
                "identity": f"{left.signature.decode('ascii')}:{left.raw_form_id:08X}:{index}",
                "signature": left.signature.decode("ascii"),
                "raw_form_id": f"{left.raw_form_id:08X}",
                "subrecord_index": index,
                "tag": tag,
                "source": source_text,
                "target": target_text,
                "provenance": provenance,
            })
    if len(rows) != EXPECTED_FIELDS:
        raise AssertionError(f"changed field count {len(rows)} != {EXPECTED_FIELDS}")
    if dict(sorted(tags.items())) != EXPECTED_TAGS:
        raise AssertionError(f"changed tag counts differ: {dict(tags)}")
    return rows


def pex_parse(data: bytes) -> tuple[list[bytes], list[bytes], bytes]:
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
    count = int.from_bytes(data[position : position + 2], "big")
    position += 2
    strings = [read_string() for _ in range(count)]
    return prestrings, strings, data[position:]


def bsa_members(data: bytes) -> tuple[int, list[tuple[str, int, int]]]:
    magic, version, folder_offset, flags, folder_count, file_count, _, _, _ = struct.unpack_from("<4s8I", data, 0)
    if magic != b"BSA\0" or version != 105:
        raise AssertionError("only Skyrim SE BSA v105 is supported")
    position = folder_offset + folder_count * 24
    entries = []
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
    return flags, [(f"{folder}\\{name}", int(size), int(offset)) for folder, size, offset, name in entries]


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


def seed_members(seed_archive: Path) -> tuple[bytes, dict[str, bytes]]:
    if sha256(seed_archive) != SEED_ARCHIVE_SHA256:
        raise AssertionError("RDO CHT seed archive hash mismatch")
    with zipfile.ZipFile(seed_archive) as archive:
        esp = archive.read(SEED_ESP_MEMBER)
        scripts = {name: archive.read(f"scripts/{name}") for name in PEX_FIELDS}
    if esp.count(b"<BribeCost>") != 1 or esp.count(b"<bribecost>") != 0:
        raise AssertionError("unexpected seed bribecost token state")
    return esp.replace(b"<BribeCost>", b"<bribecost>"), scripts


def pex_rows(source_bsa: bytes, targets: dict[str, bytes]) -> list[dict[str, object]]:
    rows = []
    for name, (expected_index, expected_source, expected_target) in sorted(PEX_FIELDS.items()):
        source = bsa_member(source_bsa, f"scripts\\{name}")
        target = targets[name]
        source_pre, source_strings, source_tail = pex_parse(source)
        target_pre, target_strings, target_tail = pex_parse(target)
        if source[:16] != target[:16] or source_pre != target_pre:
            raise AssertionError(f"PEX header/prestrings differ: {name}")
        if len(source_strings) != len(target_strings) or source_tail != target_tail:
            raise AssertionError(f"PEX declaration/bytecode contract differs: {name}")
        changed = [i for i, pair in enumerate(zip(source_strings, target_strings)) if pair[0] != pair[1]]
        if changed != [expected_index]:
            raise AssertionError(f"unexpected PEX changed slots: {name}: {changed}")
        source_text = source_strings[expected_index].decode("cp1252")
        target_text = target_strings[expected_index].decode("utf-8")
        if (source_text, target_text) != (expected_source, expected_target):
            raise AssertionError(f"unexpected PEX display text: {name}")
        rows.append({
            "script": name,
            "index": expected_index,
            "source": source_text,
            "target": target_text,
            "source_sha256": sha256_bytes(source),
            "target_sha256": sha256_bytes(target),
            "tail_sha256": sha256_bytes(source_tail),
            "provenance": "RDO Final CHT; one existing display string slot only",
        })
    return rows


def prepare(args: argparse.Namespace) -> tuple[bytes, dict[str, bytes], dict[str, object]]:
    source_esp = args.source_esp.read_bytes()
    source_bsa = args.source_bsa.read_bytes()
    if sha256_bytes(source_esp) != SOURCE_ESP_SHA256:
        raise AssertionError("official RDO Final ESP hash mismatch")
    if sha256_bytes(source_bsa) != SOURCE_BSA_SHA256:
        raise AssertionError("official RDO Final BSA hash mismatch")
    target_esp, target_scripts = seed_members(args.seed_archive)
    ledger = {
        "schema": 1,
        "source": {
            "official_esp_sha256": SOURCE_ESP_SHA256,
            "official_bsa_sha256": SOURCE_BSA_SHA256,
            "cht_seed_archive_sha256": SEED_ARCHIVE_SHA256,
        },
        "plugin": plugin_rows(source_esp, target_esp),
        "pex": pex_rows(source_bsa, target_scripts),
    }
    return target_esp, target_scripts, ledger


def write_manifest() -> None:
    paths = sorted(path for path in ROOT.rglob("*") if path.is_file() and path != MANIFEST and "__pycache__" not in path.parts)
    lines = [f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in paths]
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote manifest: {len(paths)} files")


def verify_manifest() -> None:
    listed = set()
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        path = ROOT / relative
        if sha256(path) != digest:
            raise AssertionError(f"manifest mismatch: {relative}")
        listed.add(relative)
    actual = {path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file() and path != MANIFEST and "__pycache__" not in path.parts}
    if listed != actual:
        raise AssertionError(f"manifest coverage mismatch: {sorted(listed ^ actual)}")
    print(f"PASS manifest: {len(listed)} files, complete coverage")


def build(args: argparse.Namespace) -> None:
    target_esp, target_scripts, ledger = prepare(args)
    OUTPUT_ESP.write_bytes(target_esp)
    OUTPUT_SCRIPTS.mkdir(parents=True, exist_ok=True)
    for name, data in target_scripts.items():
        (OUTPUT_SCRIPTS / name).write_bytes(data)
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote ESP + {len(target_scripts)} PEX + {len(ledger['plugin']) + len(ledger['pex'])} ledger rows")


def verify(args: argparse.Namespace) -> None:
    target_esp, target_scripts, ledger = prepare(args)
    if OUTPUT_ESP.read_bytes() != target_esp:
        raise AssertionError("packaged ESP differs from fresh rebuild")
    for name, data in target_scripts.items():
        if (OUTPUT_SCRIPTS / name).read_bytes() != data:
            raise AssertionError(f"packaged PEX differs from seed: {name}")
    if json.loads(LEDGER.read_text(encoding="utf-8")) != ledger:
        raise AssertionError("packaged ledger differs from fresh audit")
    print("PASS reproducibility: packaged ESP/PEX/ledger equal a fresh audited rebuild")
    print("PASS plugin semantic delta: 9,766 records; only 4,071 canonical UTF-8 display zstrings changed")
    print("PASS PEX semantic delta: 6 existing display slots changed; every declaration/bytecode tail identical")
    print("PASS text gate: engine tokens/newlines preserved; no empty/replacement/???/common Simplified targets")
    verify_manifest()
    print("RESULT: PASS")


def parser() -> argparse.ArgumentParser:
    output = argparse.ArgumentParser()
    sub = output.add_subparsers(dest="command", required=True)
    for name, function in (("build", build), ("verify", verify)):
        command = sub.add_parser(name)
        command.add_argument("--source-esp", type=Path, required=True)
        command.add_argument("--source-bsa", type=Path, required=True)
        command.add_argument("--seed-archive", type=Path, required=True)
        command.set_defaults(function=function)
    command = sub.add_parser("manifest")
    command.set_defaults(function=lambda _: write_manifest())
    return output


def main() -> int:
    args = parser().parse_args()
    try:
        args.function(args)
    except (AssertionError, OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
