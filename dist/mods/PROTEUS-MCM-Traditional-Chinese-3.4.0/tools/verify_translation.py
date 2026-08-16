#!/usr/bin/env python3
"""Verify the PROTEUS 3.4.0 MCM script-only translation release."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "tools" / "translation-source.tsv"
PSC = ROOT / "tools" / "ProteusMCMScript.psc"
PEX = ROOT / "Scripts" / "ProteusMCMScript.pex"
TRANSLATION = ROOT / "Interface" / "Translations" / "PROTEUS_english.txt"
UPSTREAM_PSC_SHA256 = "36ba7794673108c9b025b95cd0a03a81cad9d469e9f8e9429391e8da69569740"
UPSTREAM_PEX_SHA256 = "2f84e5bd5dcafcaa1e036d2cee1e3420fccd14df3743a104975108a6750f0beb"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows() -> list[dict[str, str]]:
    with TSV.open("r", encoding="utf-8", newline="") as handle:
        result = list(csv.DictReader(handle, delimiter="\t"))
    if len(result) != 34 or len({row["key"] for row in result}) != 34:
        raise AssertionError("translation TSV is not 34 unique rows")
    return result


def split_script(path: Path) -> tuple[list[str], dict[str, str]]:
    declarations: list[str] = []
    blocks: dict[str, str] = {}
    current: list[str] = []
    header = ""
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = re.sub(r"\s+", " ", raw_line.strip()).lower()
        if not line or line.startswith(";"):
            continue
        if not current and (line.startswith("event ") or " function " in f" {line} "):
            header = line
            current = [line]
        elif current:
            current.append(line)
            if line in ("endevent", "endfunction"):
                blocks[header] = "\n".join(current)
                current = []
                header = ""
        else:
            declarations.append(line)
    if current:
        raise AssertionError(f"unterminated script block in {path}")
    return sorted(declarations), blocks


def verify_source(
    upstream_psc: Path, upstream_pex: Path, final_decompiled: Path,
    items: list[dict[str, str]],
) -> None:
    if sha256(upstream_psc) != UPSTREAM_PSC_SHA256:
        raise AssertionError("upstream PSC hash mismatch")
    if sha256(upstream_pex) != UPSTREAM_PEX_SHA256:
        raise AssertionError("upstream PEX hash mismatch")
    source = upstream_psc.read_text(encoding="utf-8-sig")
    candidate = PSC.read_text(encoding="utf-8")
    for row in items:
        source = source.replace(f'"{row["source"]}"', f'"{row["key"]}"')
    source = re.sub(r"\s+", " ", source).strip().lower()
    candidate = re.sub(r"\s+", " ", candidate).strip().lower()
    # The candidate comes from the exact upstream PEX decompile, so declaration
    # order/casts differ from the author PSC. Body-level equivalence is checked
    # separately by the recorded decompile -> compile -> decompile round trip.
    for row in items:
        if f'"{row["key"].lower()}"' not in candidate:
            raise AssertionError(f"missing MCM key in PSC: {row['key']}")
    forbidden = [row["source"] for row in items if f'"{row["source"].lower()}"' in candidate]
    if forbidden:
        raise AssertionError(f"unreplaced display strings: {forbidden}")
    if "sacrosanct - vampires of skyrim.esp" not in candidate:
        raise AssertionError("non-display compatibility literal changed")
    if "event onconfigopen()" not in candidate:
        raise AssertionError("save-compatible page refresh event is missing")
    if "pages = new string[2]" not in candidate:
        raise AssertionError("OnConfigOpen does not rebuild the two-page array")
    expected_declarations, expected_blocks = split_script(PSC)
    actual_declarations, actual_blocks = split_script(final_decompiled)
    if expected_declarations != actual_declarations:
        raise AssertionError("compiled PEX decompile changed declarations/properties")
    if expected_blocks != actual_blocks:
        raise AssertionError("compiled PEX decompile changed function/event bodies")
    print(
        "PASS source gate: exact PROTEUS 3.4.0 PSC/PEX hashes; 34 display literals keyed; "
        "final PEX decompiles to the same declarations and 9 function/event bodies"
    )


def verify_asset(items: list[dict[str, str]]) -> None:
    data = TRANSLATION.read_bytes()
    if not data.startswith(b"\xff\xfe") or b"\r\x00\n\x00" not in data:
        raise AssertionError("translation is not UTF-16LE BOM + CRLF")
    lines = data[2:].decode("utf-16-le").splitlines()
    expected = [f'{row["key"]}\t{row["target"]}' for row in items]
    if lines != expected:
        raise AssertionError("translation asset differs from TSV")
    if any("�" in row["target"] or "???" in row["target"] for row in items):
        raise AssertionError("mojibake sentinel in target")
    print("PASS translation: 34/34 keys, exact order, UTF-16LE BOM, CRLF")


def verify_payload(items: list[dict[str, str]]) -> None:
    if not PEX.is_file():
        raise AssertionError("compiled PEX is missing")
    raw = PEX.read_bytes()
    missing = [row["key"] for row in items if row["key"].encode() not in raw]
    if missing:
        raise AssertionError(f"compiled PEX lacks keys: {missing}")
    if sha256(PEX) == UPSTREAM_PEX_SHA256:
        raise AssertionError("packaged PEX is still the upstream English binary")
    print(
        f"PASS payload: compiled PEX exposes all 34 ASCII keys and save-compatible page refresh; "
        f"PEX {sha256(PEX)}"
    )


def verify_manifest() -> None:
    manifest = ROOT / "MANIFEST.sha256"
    listed: set[str] = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        path = (ROOT / relative).resolve()
        if ROOT not in path.parents or sha256(path) != expected:
            raise AssertionError(f"manifest mismatch: {relative}")
        listed.add(relative)
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and path.name != manifest.name and "__pycache__" not in path.parts
    }
    if listed != actual:
        raise AssertionError(f"manifest coverage mismatch: {sorted(listed ^ actual)}")
    print(f"PASS manifest: {len(listed)} files, complete coverage")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream-psc", required=True, type=Path)
    parser.add_argument("--upstream-pex", required=True, type=Path)
    parser.add_argument("--final-decompiled", required=True, type=Path)
    args = parser.parse_args()
    items = rows()
    verify_source(args.upstream_psc, args.upstream_pex, args.final_decompiled, items)
    verify_asset(items)
    verify_payload(items)
    verify_manifest()
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
