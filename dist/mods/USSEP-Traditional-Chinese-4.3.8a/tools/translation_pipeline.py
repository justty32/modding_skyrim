#!/usr/bin/env python3
"""Build a version-locked USSEP 4.3.8a CHT overlay from the 4.3.6c CHS seed."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
ENGINE_PATH = REPO / "scripts/inline_translation_overlay.py"
OUTPUT = ROOT / "unofficial skyrim special edition patch.esp"
LEDGER = ROOT / "tools/translation-source.json"
MANIFEST = ROOT / "MANIFEST.sha256"
SOURCE_SHA256 = "2df73db3622005e04470e3603f804e2fd855ae932a9847073f386bd8013e9d98"
SEED_SHA256 = "f7b8ab9344e24b66ab0f02da3db0f6ca59def113d482e309ed809004abb9b812"
SEED_ARCHIVE_SHA256 = "746854c4b08a1bbb1fcf38cda29e9d94902a9d65a98fe48272606f14b6a60710"
EXPECTED_FIELDS = 17904
MANUAL = {
    ("CELL", 0x000165B7, "FULL", 0): "酩酊獵手",
    ("LCTN", 0x0001F872, "FULL", 0): "酩酊獵手",
    ("DIAL", 0x000C2464, "FULL", 0): "為什麼叫「酩酊獵手」？",
    ("INFO", 0x000C2469, "NAM1", 1): "這就是為什麼我兄弟和我開了家打獵用具店：酩酊獵手。就在城門附近。",
    ("INFO", 0x000C246A, "NAM1", 0): "很多人問這個問題。",
    ("INFO", 0x000C246A, "NAM1", 1): "我和我兄弟阿諾利亞斯想出來的，有天晚上我們喝了……太多蜂蜜酒。",
    ("INFO", 0x000C246A, "NAM1", 2): "喝完之後，我們打算出門來場月光下狩獵。我們走散了，而我兄弟在喝醉的狀態下誤把我當成了一隻鹿。",
    ("INFO", 0x000C246A, "NAM1", 3): "他射了一支箭穿透了我的……呃……臀部。在那次難忘的經歷後，我們就決定了我們店的名字。",
    ("DIAL", 0x000C368C, "FULL", 0): "要是我想工作該找誰？",
    ("INFO", 0x000C3695, "NAM1", 0): "試試胡爾達，母馬旗幟客棧的客棧老闆。就在前面，市場旁邊。",
    ("INFO", 0x000C3695, "NAM1", 1): "你也應該去龍臨堡看看。最近發生了許多事情，領主和他的總管可能需要幫助。",
}


def load_engine():
    spec = importlib.util.spec_from_file_location("ussep_inline_translation", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load inline translation engine")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ENGINE = load_engine()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def prepare(source_path: Path, seed_path: Path):
    source = source_path.read_bytes()
    seed = seed_path.read_bytes()
    if sha256_bytes(source) != SOURCE_SHA256:
        raise AssertionError("USSEP 4.3.8a source hash mismatch")
    if sha256_bytes(seed) != SEED_SHA256:
        raise AssertionError("USSEP 4.3.6c CHS seed hash mismatch")
    rows = ENGINE.collect_seed_rows(
        source, seed,
        provenance="USSEP CHS 4.3.6c (Nexus 143324) matched into exact 4.3.8a source",
        manual=MANUAL,
    )
    if len(rows) != EXPECTED_FIELDS:
        raise AssertionError(f"unexpected translated field count: {len(rows)}")
    output = ENGINE.transform_plugin(source, rows)
    ENGINE.verify_overlay(source, output, rows)
    ledger = {
        "schema": 1,
        "source": {
            "official_4_3_8a_esp_sha256": SOURCE_SHA256,
            "chs_4_3_6c_seed_esp_sha256": SEED_SHA256,
            "chs_4_3_6c_seed_archive_sha256": SEED_ARCHIVE_SHA256,
        },
        "coverage": {
            "current_records": 58965,
            "seed_records": 58330,
            "translated_fields": EXPECTED_FIELDS,
            "boundary": "Only stable record FormID + localizable tag occurrence matches; unmatched 4.3.8a text remains unchanged.",
        },
        "plugin": rows,
    }
    return output, ledger


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
    output, ledger = prepare(args.source, args.seed)
    OUTPUT.write_bytes(output)
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_manifest()
    print(f"built USSEP 4.3.8a overlay: {len(ledger['plugin'])} translated fields")


def verify(args: argparse.Namespace) -> None:
    output, ledger = prepare(args.source, args.seed)
    if OUTPUT.read_bytes() != output:
        raise AssertionError("packaged USSEP ESP differs from fresh rebuild")
    if json.loads(LEDGER.read_text(encoding="utf-8")) != ledger:
        raise AssertionError("packaged USSEP ledger differs")
    verify_manifest()
    print(f"PASS: 58,965 current records preserved; {len(ledger['plugin'])} text fields translated; every nontext payload unchanged")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    args = parser.parse_args()
    try:
        (build if args.command == "build" else verify)(args)
    except (AssertionError, OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
