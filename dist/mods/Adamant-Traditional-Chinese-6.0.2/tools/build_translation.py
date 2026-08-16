#!/usr/bin/env python3
"""Build the version-locked localized ESP and UTF-8 string tables."""

from __future__ import annotations

import argparse
from pathlib import Path

from plugin_localizer import (
    Contract, build_localized_plugin, encode_strings, read_translations, sha256,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "tools" / "contract.json"
TSV = ROOT / "tools" / "translation-source.tsv"
STRINGS_DIR = ROOT / "Strings"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path, help="exact official English ESP")
    args = parser.parse_args()
    contract = Contract.read(CONTRACT_PATH)
    actual = sha256(args.source)
    if actual != contract.source_sha256:
        raise SystemExit(f"source SHA-256 mismatch: {actual}")
    rows = read_translations(TSV, contract)
    plugin, tables = build_localized_plugin(args.source.read_bytes(), rows, contract)

    STRINGS_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / contract.plugin_name).write_bytes(plugin)
    base = Path(contract.plugin_name).stem
    emitted: list[str] = []
    for table, entries in tables.items():
        if not entries:
            continue
        encoded = encode_strings(entries, length_prefixed=table != "STRINGS")
        for language in ("English", "Chinese"):
            path = STRINGS_DIR / f"{base}_{language}.{table}"
            path.write_bytes(encoded)
            emitted.append(path.name)
    print(f"built {contract.plugin_name}: {len(rows)} localized fields")
    print(f"output sha256: {sha256(ROOT / contract.plugin_name)}")
    print("tables:", ", ".join(emitted))


if __name__ == "__main__":
    main()
