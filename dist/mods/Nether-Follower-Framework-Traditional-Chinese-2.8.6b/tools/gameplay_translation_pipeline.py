#!/usr/bin/env python3
"""Audit/package exact-version NFF 2.8.6b Traditional Chinese gameplay files."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
PARSER = REPO / "dist/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/tools/translation_pipeline.py"
OVERLAY = REPO / "scripts/inline_translation_overlay.py"
OUTPUT_ESP = ROOT / "nwsFollowerFramework.esp"
OUTPUT_SCRIPTS = ROOT / "Scripts"
LEDGER = ROOT / "tools/gameplay-translation-source.json"
MANIFEST = ROOT / "MANIFEST.sha256"
SOURCE_ESP_SHA256 = "51601807aafe152c9504244492f39faf7411bc83bde3d2da0b8ecdf72ec7f299"
SEED_ESP_SHA256 = "5509f40b3b9af4b7711dbbe3e1818c47ddc4aa7a3872933cec58555b9b958dd8"
SEED_ARCHIVE_SHA256 = "be9e3a791f140deb1321e3d10f61ee3b81c9cae5f1f9bfbed1339079024b377a"
EXPECTED_RECORDS = 2917
EXPECTED_PLUGIN_FIELDS = 467
EXPECTED_PEX_FILES = 20
EXPECTED_PEX_FIELDS = 297
TOKEN_RE = re.compile(r"<[^<>]+>|%[^%\s]+%|\$[A-Za-z0-9_]+|\\[nrt]|\{[^{}]+\}")
ALLOWED_EMPTY_TARGETS = {"nwsFollower_Sparring.pex:220"}
RUNTIME_LITERAL_TARGETS = {
    "INFO:054B6F33:19": "我想給你設計一套服裝。",
    "DIAL:054CD45C:1": "我要佔用你一點時間。(NFF)",
}


def load_parser():
    spec = importlib.util.spec_from_file_location("nff_translation_parser", PARSER)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load the shared plugin/PEX parser")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TP = load_parser()


def load_overlay():
    spec = importlib.util.spec_from_file_location("nff_inline_translation_overlay", OVERLAY)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load the shared inline translation overlay engine")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


OVERLAY_ENGINE = load_overlay()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def assert_text_contract(source: str, target: str, identity: str) -> None:
    if (not target and identity not in ALLOWED_EMPTY_TARGETS) or "\ufffd" in target or "???" in target:
        raise AssertionError(f"invalid target text: {identity}")
    if (identity not in RUNTIME_LITERAL_TARGETS and
            sorted(TOKEN_RE.findall(source)) != sorted(TOKEN_RE.findall(target))):
        raise AssertionError(f"control-token mismatch: {identity}")
    if source.count("\n") != target.count("\n"):
        raise AssertionError(f"newline mismatch: {identity}")


def plugin_rows(source: bytes, target: bytes) -> list[dict[str, object]]:
    left = TP.iter_records(source)
    right = TP.iter_records(target)
    if len(left) != EXPECTED_RECORDS or len(right) != EXPECTED_RECORDS:
        raise AssertionError("unexpected ESP record count")
    rows = []
    for a, b in zip(left, right):
        if (a.signature, a.raw_form_id, a.path) != (b.signature, b.raw_form_id, b.path):
            raise AssertionError("ESP record identity/order/group path differs")
        if TP.semantic_header(a.header) != TP.semantic_header(b.header):
            raise AssertionError(f"ESP semantic header differs: {a.raw_form_id:08X}")
        if [item.tag for item in a.subrecords] != [item.tag for item in b.subrecords]:
            raise AssertionError(f"ESP subrecord topology differs: {a.raw_form_id:08X}")
        for index, (x, y) in enumerate(zip(a.subrecords, b.subrecords)):
            if x.payload == y.payload:
                continue
            source_text = TP.canonical_zstring(x.payload, "cp1252")
            target_text = TP.canonical_zstring(y.payload, "utf-8")
            identity = f"{a.signature.decode()}:{a.raw_form_id:08X}:{index}"
            assert_text_contract(source_text, target_text, identity)
            rows.append({
                "identity": identity,
                "signature": a.signature.decode(),
                "raw_form_id": f"{a.raw_form_id:08X}",
                "subrecord_index": index,
                "tag": x.tag.decode(),
                "source": source_text,
                "target": target_text,
                "provenance": (
                    "runtime QA: unresolved translation key replaced with the audited NFF CHT table literal"
                    if identity in RUNTIME_LITERAL_TARGETS
                    else "NFF Traditional Chinese 2.8.6b (Nexus 67680)"
                ),
            })
    if len(rows) != EXPECTED_PLUGIN_FIELDS:
        raise AssertionError(f"unexpected ESP text delta count: {len(rows)}")
    return rows


def pex_rows(source_dir: Path, target_dir: Path) -> list[dict[str, object]]:
    targets = sorted(target_dir.glob("*.pex"), key=lambda path: path.name.lower())
    if len(targets) != EXPECTED_PEX_FILES:
        raise AssertionError("unexpected translated PEX file count")
    rows = []
    for target in targets:
        source = source_dir / target.name
        source_data = source.read_bytes()
        target_data = target.read_bytes()
        pre_a, strings_a, tail_a = TP.pex_parse(source_data)
        pre_b, strings_b, tail_b = TP.pex_parse(target_data)
        if source_data[:16] != target_data[:16] or pre_a != pre_b:
            raise AssertionError(f"PEX header/prestrings differ: {target.name}")
        if len(strings_a) != len(strings_b) or tail_a != tail_b:
            raise AssertionError(f"PEX declaration/bytecode contract differs: {target.name}")
        for index, (a, b) in enumerate(zip(strings_a, strings_b)):
            if a == b:
                continue
            source_text = a.decode("cp1252")
            target_text = b.decode("utf-8")
            identity = f"{target.name}:{index}"
            assert_text_contract(source_text, target_text, identity)
            rows.append({
                "script": target.name,
                "index": index,
                "source": source_text,
                "target": target_text,
                "source_sha256": sha256_bytes(source_data),
                "target_sha256": sha256_bytes(target_data),
                "tail_sha256": sha256_bytes(tail_a),
                "provenance": "NFF Traditional Chinese 2.8.6b; existing string-table slot only",
            })
    if len(rows) != EXPECTED_PEX_FIELDS:
        raise AssertionError(f"unexpected PEX text delta count: {len(rows)}")
    return rows


def prepare(source_mod: Path, seed_dir: Path):
    source_esp = (source_mod / "nwsFollowerFramework.esp").read_bytes()
    seed_esp = (seed_dir / "nwsFollowerFramework.esp").read_bytes()
    if sha256_bytes(source_esp) != SOURCE_ESP_SHA256:
        raise AssertionError("installed NFF 2.8.6b ESP hash mismatch")
    if sha256_bytes(seed_esp) != SEED_ESP_SHA256:
        raise AssertionError("NFF CHT 2.8.6b seed ESP hash mismatch")
    literal_rows = [
        {
            "signature": identity.split(":", 1)[0],
            "raw_form_id": identity.split(":")[1],
            "tag": "RNAM" if identity.startswith("INFO:") else "FULL",
            "tag_occurrence": 0,
            "target": target,
        }
        for identity, target in RUNTIME_LITERAL_TARGETS.items()
    ]
    target_esp = OVERLAY_ENGINE.transform_plugin(seed_esp, literal_rows)
    scripts = {path.name: path.read_bytes() for path in (seed_dir / "Scripts").glob("*.pex")}
    ledger = {
        "schema": 1,
        "source": {
            "official_esp_sha256": SOURCE_ESP_SHA256,
            "cht_seed_esp_sha256": SEED_ESP_SHA256,
            "cht_seed_archive_sha256": SEED_ARCHIVE_SHA256,
        },
        "plugin": plugin_rows(source_esp, target_esp),
        "pex": pex_rows(source_mod / "Scripts", seed_dir / "Scripts"),
    }
    return target_esp, scripts, ledger


def artifact_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*") if path.is_file() and path != MANIFEST and "__pycache__" not in path.parts)


def write_manifest() -> None:
    MANIFEST.write_text("".join(f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}\n" for path in artifact_files()), encoding="utf-8")


def verify_manifest() -> None:
    listed = set()
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        if sha256(ROOT / relative) != digest:
            raise AssertionError(f"manifest mismatch: {relative}")
        listed.add(relative)
    actual = {path.relative_to(ROOT).as_posix() for path in artifact_files()}
    if listed != actual:
        raise AssertionError(f"manifest coverage mismatch: {sorted(listed ^ actual)}")


def build(args: argparse.Namespace) -> None:
    esp, scripts, ledger = prepare(args.source_mod, args.seed_dir)
    OUTPUT_ESP.write_bytes(esp)
    OUTPUT_SCRIPTS.mkdir(parents=True, exist_ok=True)
    for name, data in scripts.items():
        (OUTPUT_SCRIPTS / name).write_bytes(data)
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_manifest()
    print(f"built: {len(ledger['plugin'])} ESP fields, {len(ledger['pex'])} PEX slots")


def verify(args: argparse.Namespace) -> None:
    esp, scripts, ledger = prepare(args.source_mod, args.seed_dir)
    if OUTPUT_ESP.read_bytes() != esp:
        raise AssertionError("packaged ESP differs from audited seed plus runtime literal fixes")
    for name, data in scripts.items():
        if (OUTPUT_SCRIPTS / name).read_bytes() != data:
            raise AssertionError(f"packaged PEX differs: {name}")
    if json.loads(LEDGER.read_text(encoding="utf-8")) != ledger:
        raise AssertionError("packaged gameplay ledger differs")
    verify_manifest()
    print("PASS: 2,917 ESP records; only 467 canonical UTF-8 display strings changed")
    print("PASS: 20 PEX files; only 297 existing string slots changed; bytecode tails identical")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--source-mod", type=Path, required=True)
    parser.add_argument("--seed-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        (build if args.command == "build" else verify)(args)
    except (AssertionError, OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
