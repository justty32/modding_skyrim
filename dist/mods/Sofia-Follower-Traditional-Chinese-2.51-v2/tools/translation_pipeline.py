#!/usr/bin/env python3
"""Rebuild and verify the Sofia 2.51 Traditional Chinese v2 text overlay."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

from opencc import OpenCC


ARTIFACT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
SHARED = REPO / "scripts/inline_translation_overlay.py"
IFD_PIPELINE = REPO / "dist/mods/Improved-Follower-Dialogue-Lydia-Traditional-Chinese-4.2.2/tools/translation_pipeline.py"
PLUGIN_NAME = "SofiaFollower.esp"
SOURCE_ESP_SHA256 = "8c70186252d0a4415e1ff02584b87adca4c685a4fc4d2dec94c09040ef3ec3c9"
SOURCE_BSA_SHA256 = "bc4b3bc004a95dd70681a7d4417ed6926c8ccf6fa38ade77069853d949ba0574"
SEED_ESP_SHA256 = "b748b0863cf0c21d937a6b74a7c8b160aa5e3616915fb8bddd50819aa2a62d87"
EXPECTED_RECORDS = 1742
EXPECTED_PLUGIN_FIELDS = 1665
EXPECTED_PEX_FIELDS = 105
SEED_PEX_SHA256 = {
    "qf_jjsofiadrunk_0201a866.pex": "62d6d3e43d2ad8776eac803695ce58ac1b620431a9bbe0b4596808d8032a2b48",
    "sofiacatchupnewscript.pex": "933c06a1a6893f8cbd84d77d45ca8a88b640d9c3ab66eceae71d53d631186b49",
    "sofialeadthewayscript.pex": "e5742f8a9bbfd01fe2fb7f1eb75ba54a6eedf4897ddfd9f3d1b403377c3cd2f1",
    "sofiamarriagescript.pex": "11afc9fe5d79e8380a1ff62ba6739cacef4e346de646473cd8df05de09d59168",
    "sofiamcmscript.pex": "5bbc3d112f6295bb95b4dcb0418590fe1e8bfd0825862b8c03fb9cb8a7538d0b",
    "sofiaplayergive.pex": "7f928f1ae17bdfcf25a9771684f08d8021dfd4d1c5da63dbe09f4a67aa5272c8",
    "tif__0205d40d.pex": "58b983cae3a0818279727490c5bd67d0bc5af64b7316e717575976e57d9d1442",
    "tif__02061f74.pex": "a3a9fadbd66667ae0218455cb16c72ace23edca09c14128b64e8c67d340250a2",
}
ELLIPSIS_IDENTITIES = {
    ("DIAL", 0x020285C1, "FULL", 0),
    ("INFO", 0x0203F13C, "NAM1", 0),
    ("INFO", 0x020690AB, "NAM1", 0),
    ("INFO", 0x020722F4, "NAM1", 0),
    ("INFO", 0x0203F12B, "NAM1", 0),
    ("INFO", 0x020722F3, "NAM1", 0),
    ("INFO", 0x02045D4A, "NAM1", 0),
    ("INFO", 0x020690AD, "NAM1", 0),
    ("INFO", 0x020722F6, "NAM1", 0),
    ("INFO", 0x020722F5, "NAM1", 0),
    ("INFO", 0x020063FE, "NAM1", 0),
    ("INFO", 0x0205D40D, "NAM1", 0),
}
TOKEN_RE = re.compile(r"<[^<>]+>|%[^%\s]+%|\$[A-Za-z0-9_]+|\\[nrt]|\{[^{}]+\}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load pipeline: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


OV = load_module("sofia_inline_overlay", SHARED)
IFD = load_module("sofia_ifd_pipeline", IFD_PIPELINE)
CONVERT = OpenCC("s2tw").convert


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def checked(path: Path, expected: str, label: str) -> bytes:
    data = path.read_bytes()
    actual = sha256(data)
    if actual != expected:
        raise AssertionError(f"unexpected {label} SHA-256: {actual}")
    return data


def load_inputs(source_esp: Path, source_bsa: Path, seed_dir: Path) -> tuple[bytes, bytes, bytes, dict[str, bytes]]:
    source = checked(source_esp, SOURCE_ESP_SHA256, "source ESP")
    bsa = checked(source_bsa, SOURCE_BSA_SHA256, "source BSA")
    seed = checked(seed_dir / PLUGIN_NAME, SEED_ESP_SHA256, "seed ESP")
    pex = {
        name: checked(seed_dir / "scripts" / name, digest, f"seed {name}")
        for name, digest in SEED_PEX_SHA256.items()
    }
    return source, bsa, seed, pex


def manual_ellipsis() -> dict[tuple[str, int, str, int], str]:
    return {identity: "……" for identity in ELLIPSIS_IDENTITIES}


def plugin_rows(source: bytes, seed: bytes) -> list[dict[str, object]]:
    rows = OV.collect_seed_rows(
        source,
        seed,
        provenance="Sofia Traditional Chinese Localization Patch v2; OpenCC s2tw normalization",
        manual=manual_ellipsis(),
        converter="s2tw",
    )
    if len(rows) != EXPECTED_PLUGIN_FIELDS:
        raise AssertionError(f"plugin coverage changed: {len(rows)} != {EXPECTED_PLUGIN_FIELDS}")
    return rows


def verify_seed_plugin(source: bytes, seed: bytes) -> None:
    left = OV.TP.iter_records(source)
    right = OV.TP.iter_records(seed)
    if len(left) != EXPECTED_RECORDS or len(right) != EXPECTED_RECORDS:
        raise AssertionError("record count changed")
    changed = 0
    for a, b in zip(left, right):
        if (a.signature, a.raw_form_id, a.path) != (b.signature, b.raw_form_id, b.path):
            raise AssertionError("seed record identity/order/group path changed")
        if OV.TP.semantic_header(a.header) != OV.TP.semantic_header(b.header):
            raise AssertionError(f"seed semantic header changed: {a.raw_form_id:08X}")
        if [item.tag for item in a.subrecords] != [item.tag for item in b.subrecords]:
            raise AssertionError(f"seed subrecord topology changed: {a.raw_form_id:08X}")
        for x, y in zip(a.subrecords, b.subrecords):
            if x.payload == y.payload:
                continue
            if x.tag not in OV.LOCALIZABLE_TAGS:
                raise AssertionError(
                    f"seed non-text payload changed: {a.signature.decode()}:{a.raw_form_id:08X}:{x.tag.decode()}"
                )
            changed += 1
    if changed != EXPECTED_PLUGIN_FIELDS:
        raise AssertionError(f"seed plugin delta count changed: {changed} != {EXPECTED_PLUGIN_FIELDS}")


def pex_rows(source_bsa: bytes, seed_pex: dict[str, bytes]) -> list[dict[str, object]]:
    rows = []
    for name in sorted(seed_pex):
        source = IFD.bsa_member(source_bsa, "scripts\\" + name)
        seed = seed_pex[name]
        source_pre, source_strings, _, source_tail = IFD.pex_parse(source)
        seed_pre, seed_strings, _, seed_tail = IFD.pex_parse(seed)
        if source[:16] != seed[:16] or source_pre != seed_pre:
            raise AssertionError(f"PEX header/prestrings changed: {name}")
        if len(source_strings) != len(seed_strings) or source_tail != seed_tail:
            raise AssertionError(f"PEX declaration/bytecode contract changed: {name}")
        for index, (left, right) in enumerate(zip(source_strings, seed_strings)):
            if left == right:
                continue
            source_text = left.decode("cp1252")
            seed_text = right.decode("utf-8")
            target = CONVERT(seed_text)
            if sorted(TOKEN_RE.findall(source_text)) != sorted(TOKEN_RE.findall(target)):
                raise AssertionError(f"PEX token mismatch: {name}:{index}")
            if source_text.count("\n") != target.count("\n"):
                raise AssertionError(f"PEX newline mismatch: {name}:{index}")
            if not target or "\ufffd" in target or "???" in target:
                raise AssertionError(f"invalid PEX target: {name}:{index}")
            rows.append({
                "path": f"scripts/{name}",
                "index": index,
                "source": source_text,
                "seed": seed_text,
                "target": target,
                "provenance": "Sofia Traditional Chinese Localization Patch v2; OpenCC s2tw normalization",
            })
    if len(rows) != EXPECTED_PEX_FIELDS:
        raise AssertionError(f"PEX coverage changed: {len(rows)} != {EXPECTED_PEX_FIELDS}")
    return rows


def build_pex(source: bytes, rows: list[dict[str, object]]) -> bytes:
    _, strings, count_position, tail = IFD.pex_parse(source)
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


def build_all_pex(source_bsa: bytes, rows: list[dict[str, object]]) -> dict[str, bytes]:
    by_name: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        name = Path(str(row["path"])).name
        by_name.setdefault(name, []).append(row)
    return {
        name: build_pex(IFD.bsa_member(source_bsa, "scripts\\" + name), by_name[name])
        for name in sorted(by_name)
    }


def verify_output_pex(source_bsa: bytes, output: dict[str, bytes], rows: list[dict[str, object]]) -> None:
    by_name: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_name.setdefault(Path(str(row["path"])).name, []).append(row)
    for name, wanted_rows in by_name.items():
        source = IFD.bsa_member(source_bsa, "scripts\\" + name)
        source_pre, source_strings, _, source_tail = IFD.pex_parse(source)
        out_pre, out_strings, _, out_tail = IFD.pex_parse(output[name])
        if source[:16] != output[name][:16] or source_pre != out_pre or source_tail != out_tail:
            raise AssertionError(f"output PEX executable contract changed: {name}")
        wanted = {int(row["index"]): row for row in wanted_rows}
        for index, (left, right) in enumerate(zip(source_strings, out_strings)):
            row = wanted.get(index)
            if row is None:
                if left != right:
                    raise AssertionError(f"unlisted PEX string changed: {name}:{index}")
            elif left.decode("cp1252") != row["source"] or right.decode("utf-8") != row["target"]:
                raise AssertionError(f"PEX ledger mismatch: {name}:{index}")


def ledger(plugin: list[dict[str, object]], pex: list[dict[str, object]]) -> dict[str, object]:
    return {
        "schema": 1,
        "plugin": PLUGIN_NAME,
        "source_esp_sha256": SOURCE_ESP_SHA256,
        "source_bsa_sha256": SOURCE_BSA_SHA256,
        "seed_esp_sha256": SEED_ESP_SHA256,
        "plugin_field_count": len(plugin),
        "pex_field_count": len(pex),
        "plugin_fields": plugin,
        "pex_fields": pex,
    }


def render_ledger(plugin: list[dict[str, object]], pex: list[dict[str, object]]) -> bytes:
    return (json.dumps(ledger(plugin, pex), ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def run_build(source_esp: Path, source_bsa: Path, seed_dir: Path) -> None:
    source, bsa, seed, seed_pex = load_inputs(source_esp, source_bsa, seed_dir)
    verify_seed_plugin(source, seed)
    prows = plugin_rows(source, seed)
    xrows = pex_rows(bsa, seed_pex)
    output_esp = OV.transform_plugin(source, prows)
    output_pex = build_all_pex(bsa, xrows)
    OV.verify_overlay(source, output_esp, prows)
    verify_output_pex(bsa, output_pex, xrows)
    (ARTIFACT / PLUGIN_NAME).write_bytes(output_esp)
    scripts = ARTIFACT / "scripts"
    scripts.mkdir(exist_ok=True)
    for name, data in output_pex.items():
        (scripts / name).write_bytes(data)
    (ARTIFACT / "tools/translation-source.json").write_bytes(render_ledger(prows, xrows))
    print(
        f"built {PLUGIN_NAME}: {len(prows)} fields; {len(output_pex)} PEX / {len(xrows)} strings; "
        f"sha256={sha256(output_esp)}"
    )


def run_verify(source_esp: Path, source_bsa: Path, seed_dir: Path) -> None:
    source, bsa, seed, seed_pex = load_inputs(source_esp, source_bsa, seed_dir)
    verify_seed_plugin(source, seed)
    prows = plugin_rows(source, seed)
    xrows = pex_rows(bsa, seed_pex)
    rebuilt_esp = OV.transform_plugin(source, prows)
    rebuilt_pex = build_all_pex(bsa, xrows)
    packaged_esp = (ARTIFACT / PLUGIN_NAME).read_bytes()
    packaged_pex = {name: (ARTIFACT / "scripts" / name).read_bytes() for name in rebuilt_pex}
    OV.verify_overlay(source, packaged_esp, prows)
    verify_output_pex(bsa, packaged_pex, xrows)
    if packaged_esp != rebuilt_esp or packaged_pex != rebuilt_pex:
        raise AssertionError("packaged ESP/PEX differ from fresh rebuild")
    if (ARTIFACT / "tools/translation-source.json").read_bytes() != render_ledger(prows, xrows):
        raise AssertionError("packaged ledger differs from fresh rebuild")
    print(
        f"PASS: {EXPECTED_RECORDS} records / {len(prows)} ESP fields; "
        f"8 PEX / {len(xrows)} strings; all non-text and executable payloads unchanged"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--source-esp", required=True, type=Path)
    parser.add_argument("--source-bsa", required=True, type=Path)
    parser.add_argument("--seed-dir", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "build":
        run_build(args.source_esp, args.source_bsa, args.seed_dir)
    else:
        run_verify(args.source_esp, args.source_bsa, args.seed_dir)


if __name__ == "__main__":
    main()
