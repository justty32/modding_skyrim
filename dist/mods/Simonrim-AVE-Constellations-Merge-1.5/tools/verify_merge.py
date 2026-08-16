#!/usr/bin/env python3
"""Verify the exact semantic contract of the Simonrim/AVE/Constellations merge."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import zlib


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "ModpackKR_Simonrim_AVE_Constellations_MergeDev.esp"
CONTRACT = Path(__file__).with_name("contract.json")
COMPRESSED_FLAG = 0x00040000


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_subrecords(data: bytes) -> list[tuple[str, bytes]]:
    result: list[tuple[str, bytes]] = []
    position = 0
    while position < len(data):
        if position + 6 > len(data):
            raise AssertionError(f"truncated subrecord header at {position}")
        tag = data[position:position + 4]
        size = struct.unpack_from("<H", data, position + 4)[0]
        position += 6
        if tag == b"XXXX":
            if size != 4 or position + 10 > len(data):
                raise AssertionError("malformed XXXX subrecord")
            size = struct.unpack_from("<I", data, position)[0]
            position += 4
            tag = data[position:position + 4]
            position += 6
        end = position + size
        if end > len(data):
            raise AssertionError(f"truncated {tag!r} payload")
        result.append((tag.decode("ascii"), data[position:end]))
        position = end
    return result


def iter_records(plugin: bytes):
    def walk(start: int, end: int):
        position = start
        while position < end:
            if position + 24 > end:
                raise AssertionError("truncated record/group header")
            header = plugin[position:position + 24]
            size = struct.unpack_from("<I", header, 4)[0]
            if header[:4] == b"GRUP":
                if size < 24 or position + size > end:
                    raise AssertionError("invalid GRUP size")
                yield from walk(position + 24, position + size)
                position += size
                continue
            record_end = position + 24 + size
            if record_end > end:
                raise AssertionError("invalid record size")
            body = plugin[position + 24:record_end]
            flags = struct.unpack_from("<I", header, 8)[0]
            if flags & COMPRESSED_FLAG:
                expected = struct.unpack_from("<I", body)[0]
                body = zlib.decompress(body[4:])
                if len(body) != expected:
                    raise AssertionError("compressed record size mismatch")
            yield header, body
            position = record_end

    yield from walk(0, len(plugin))


def decode_zstring(payload: bytes) -> str:
    if not payload.endswith(b"\0"):
        raise AssertionError("MAST is not a zstring")
    return payload[:-1].decode("cp1252")


def parse_plugin(path: Path, own_name: str) -> tuple[list[str], dict[str, dict]]:
    data = path.read_bytes()
    records = list(iter_records(data))
    if not records or records[0][0][:4] != b"TES4":
        raise AssertionError("plugin does not start with TES4")
    masters = [
        decode_zstring(payload)
        for tag, payload in parse_subrecords(records[0][1])
        if tag == "MAST"
    ]

    def form_key(raw: int) -> str:
        index = raw >> 24
        owner = masters[index] if index < len(masters) else own_name
        return f"{raw & 0xFFFFFF:06X}:{owner}"

    result: dict[str, dict] = {}
    for header, body in records[1:]:
        signature = header[:4].decode("ascii")
        raw_form = struct.unpack_from("<I", header, 12)[0]
        key = form_key(raw_form)
        subs = parse_subrecords(body)
        entries: list[dict] = []
        non_entries: list[list[str]] = []
        llct: list[int] = []
        for tag, payload in subs:
            if tag == "LVLO":
                if len(payload) != 12:
                    raise AssertionError(f"{key}: LVLO size {len(payload)} != 12")
                level, pad, reference, count, tail = struct.unpack("<HHIHH", payload)
                entries.append({
                    "level": level,
                    "pad": pad,
                    "reference": form_key(reference),
                    "count": count,
                    "tail": tail,
                })
            elif tag == "LLCT":
                if len(payload) != 1:
                    raise AssertionError(f"{key}: LLCT size {len(payload)} != 1")
                llct.append(payload[0])
            else:
                non_entries.append([tag, payload.hex()])
        if key in result:
            raise AssertionError(f"duplicate record {key}")
        result[key] = {
            "signature": signature,
            "flags": struct.unpack_from("<I", header, 8)[0],
            "non_entries": non_entries,
            "llct": llct,
            "entries": entries,
        }
    return masters, result


def semantic_hash(record: dict, *, entries: list[dict] | None = None) -> str:
    value = {
        "signature": record["signature"],
        "flags": record["flags"],
        "non_entries": record["non_entries"],
        "entries": record["entries"] if entries is None else entries,
    }
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def expected_entry(reference: str) -> dict:
    return {"level": 1, "pad": 0, "reference": reference, "count": 1, "tail": 0}


def emit_contract(donor: Path, thaumaturgy: Path, constellations: Path) -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    donor_masters, donor_records = parse_plugin(donor, "AVE - Thaumaturgy.esp")
    thaum_masters, thaum_records = parse_plugin(thaumaturgy, "Thaumaturgy.esp")
    const_masters, const_records = parse_plugin(constellations, "ConstellationsNewSkills.esp")
    if len(donor_records) != 95 or set(r["signature"] for r in donor_records.values()) != {"LVLI"}:
        raise AssertionError("donor must contain exactly 95 LVLI records")
    shared = sorted(
        key for key in set(thaum_records) & set(const_records)
        if thaum_records[key]["signature"] == const_records[key]["signature"] == "LVLI"
    )
    if len(shared) != 93:
        raise AssertionError(f"Thaumaturgy/Constellations intersection {len(shared)} != 93")
    base_records = dict(donor_records)
    for key in shared:
        base_records.setdefault(key, thaum_records[key])
    if len(base_records) != 184:
        raise AssertionError(f"merged base record count {len(base_records)} != 184")

    additions: dict[str, list[str]] = {}
    for key in shared:
        selected = [
            entry for entry in const_records[key]["entries"]
            if entry["reference"].endswith(":ConstellationsNewSkills.esp")
        ]
        if not selected:
            raise AssertionError(f"{key}: no Constellations-owned entry")
        for entry in selected:
            if entry != expected_entry(entry["reference"]):
                raise AssertionError(f"{key}: non-canonical Constellations entry {entry}")
            if entry in base_records[key]["entries"]:
                raise AssertionError(f"{key}: declared addition is already in base")
        additions[key] = [entry["reference"] for entry in selected]
    if sum(map(len, additions.values())) != 162:
        raise AssertionError("Constellations addition count must be 162")

    contract["donor_plugin_sha256"] = sha256(donor)
    contract["thaumaturgy_plugin_sha256"] = sha256(thaumaturgy)
    contract["constellations_plugin_sha256"] = sha256(constellations)
    contract["source_masters"] = {
        "ave_thaumaturgy_1_1": donor_masters,
        "thaumaturgy_1_5": thaum_masters,
        "constellations": const_masters,
    }
    contract["constellations_additions"] = additions
    contract["base_counts"] = {
        key: len(value["entries"]) for key, value in sorted(base_records.items())
    }
    contract["expected_final_counts"] = {
        key: len(base_records[key]["entries"]) + len(references)
        for key, references in sorted(additions.items())
    }
    contract["base_semantic_sha256"] = {
        key: semantic_hash(value) for key, value in sorted(base_records.items())
    }
    for old_key in ("donor_masters", "donor_counts", "donor_semantic_sha256"):
        contract.pop(old_key, None)
    CONTRACT.write_text(json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"wrote semantic contract: {len(base_records)} LVLI base records; "
        f"{len(shared)} Constellations conflicts; 162 declared additions"
    )


def verify() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if sha256(PLUGIN) != contract["plugin_sha256"]:
        raise AssertionError("output plugin SHA-256 mismatch")
    masters, records = parse_plugin(PLUGIN, contract["plugin_name"])
    if masters != contract["expected_masters"]:
        raise AssertionError(f"master mismatch: {masters}")
    if len(records) != contract["expected_lvli_records"]:
        raise AssertionError(f"record count mismatch: {len(records)}")
    if set(records) != set(contract["base_semantic_sha256"]):
        raise AssertionError("output and merged base FormKey sets differ")
    if set(r["signature"] for r in records.values()) != {"LVLI"}:
        raise AssertionError("output contains a non-LVLI data record")

    additions = contract["constellations_additions"]
    addition_count = 0
    for key, record in records.items():
        entries = list(record["entries"])
        for reference in additions.get(key, []):
            wanted = expected_entry(reference)
            if entries.count(wanted) != 1:
                raise AssertionError(f"{key}: expected exactly one added {reference}")
            entries.remove(wanted)
            addition_count += 1
        base_count = contract["base_counts"][key]
        expected_count = base_count + len(additions.get(key, []))
        if len(record["entries"]) != expected_count:
            raise AssertionError(f"{key}: entry count {len(record['entries'])} != {expected_count}")
        if record["llct"] != [expected_count]:
            raise AssertionError(f"{key}: LLCT {record['llct']} != {[expected_count]}")
        if semantic_hash(record, entries=entries) != contract["base_semantic_sha256"][key]:
            raise AssertionError(f"{key}: base semantics changed outside declared additions")

    expected_counts = contract["expected_final_counts"]
    actual_counts = {key: len(records[key]["entries"]) for key in expected_counts}
    if actual_counts != expected_counts:
        raise AssertionError(f"four-way merge counts differ: {actual_counts}")
    if addition_count != 162 or len(additions) != 93:
        raise AssertionError(f"addition coverage {addition_count}/{len(additions)} != 162/93")
    print(
        "PASS merge: exact plugin hash; 184 LVLI base semantics preserved "
        "(95 AVE/Thaumaturgy + 89 Thaumaturgy); 162 Constellations entries added across 93 lists"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-contract-from-donor", type=Path)
    parser.add_argument("--thaumaturgy", type=Path)
    parser.add_argument("--constellations", type=Path)
    args = parser.parse_args()
    if args.emit_contract_from_donor:
        if not args.thaumaturgy or not args.constellations:
            parser.error("contract emission requires --thaumaturgy and --constellations")
        emit_contract(args.emit_contract_from_donor, args.thaumaturgy, args.constellations)
    else:
        verify()


if __name__ == "__main__":
    main()
