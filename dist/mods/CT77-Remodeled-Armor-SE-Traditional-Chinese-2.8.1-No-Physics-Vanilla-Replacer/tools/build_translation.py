#!/usr/bin/env python3
"""Build the deterministic CT77 localized ESP and UTF-8 string tables."""

from __future__ import annotations

import argparse
from pathlib import Path

from plugin_localizer import (
    PLUGIN_NAME, SOURCE_SHA256, build_localized_plugin, encode_strings,
    read_translations, sha256,
)


ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "tools" / "translation-source.tsv"
STRINGS_DIR = ROOT / "Strings"
BASE = Path(PLUGIN_NAME).stem


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path, help="exact official English ESP")
    args = parser.parse_args()

    actual = sha256(args.source)
    if actual != SOURCE_SHA256:
        raise SystemExit(f"source SHA-256 mismatch: {actual}")
    rows = read_translations(TSV)
    plugin, full_entries, desc_entries = build_localized_plugin(args.source.read_bytes(), rows)

    STRINGS_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / PLUGIN_NAME).write_bytes(plugin)
    full_table = encode_strings(full_entries, length_prefixed=False)
    desc_table = encode_strings(desc_entries, length_prefixed=True)
    for language in ("English", "Chinese"):
        (STRINGS_DIR / f"{BASE}_{language}.STRINGS").write_bytes(full_table)
        (STRINGS_DIR / f"{BASE}_{language}.DLSTRINGS").write_bytes(desc_table)

    print(f"built {PLUGIN_NAME}: {len(full_entries)} FULL + {len(desc_entries)} empty DESC")
    print(f"output sha256: {sha256(ROOT / PLUGIN_NAME)}")


if __name__ == "__main__":
    main()

