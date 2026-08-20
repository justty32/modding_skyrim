#!/usr/bin/env python3
"""Build the private VIGILANT BOOK.DESC Chinese completion layer.

The exact-version Traditional Chinese plugin is both the terminology source and
the structural seed.  Only the 45 known player-visible BOOK.DESC fields are
changed; inline_translation_overlay verifies that all other record payload and
topology remain untouched.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

import inline_translation_overlay as overlay


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--version", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.read_bytes()
    rows: list[dict[str, object]] = []
    english_word = re.compile(r"[A-Za-z]{3,}")

    for record in overlay.TP.iter_records(source):
        if record.signature != b"BOOK":
            continue

        decoded: dict[bytes, list[tuple[int, int, str]]] = collections.defaultdict(list)
        occurrences: collections.Counter[bytes] = collections.Counter()
        for index, subrecord in enumerate(record.subrecords):
            occurrence = occurrences[subrecord.tag]
            occurrences[subrecord.tag] += 1
            if subrecord.tag not in (b"FULL", b"DESC"):
                continue
            try:
                value = overlay.TP.canonical_zstring(subrecord.payload, "utf-8")
            except Exception:
                continue
            decoded[subrecord.tag].append((index, occurrence, value))

        full = decoded[b"FULL"][0][2] if decoded[b"FULL"] else ""
        for index, occurrence, description in decoded[b"DESC"]:
            visible = re.sub(r"<[^>]*>", " ", description)
            if overlay.has_han(description) or not english_word.search(visible):
                continue

            suffix = full.split("：", 1)[-1].strip()
            if suffix.startswith("召喚"):
                translated_line = suffix
            elif re.search(r"\bConjure\b", description):
                translated_line = f"召喚{suffix}"
            else:
                translated_line = suffix
            prefix = description[: description.rfind("\n") + 1] if "\n" in description else ""

            rows.append(
                {
                    "identity": f"BOOK:{record.raw_form_id:08X}:DESC:{occurrence}",
                    "signature": "BOOK",
                    "raw_form_id": f"{record.raw_form_id:08X}",
                    "tag": "DESC",
                    "tag_occurrence": occurrence,
                    "source_subrecord_index": index,
                    "seed_subrecord_index": None,
                    "source": description,
                    "target": prefix + translated_line,
                    "record_name": full,
                    "provenance": (
                        f"VIGILANT CHT {args.version} FULL terminology; "
                        "private local BOOK description completion"
                    ),
                }
            )

    if len(rows) != 45:
        raise SystemExit(f"expected exactly 45 BOOK descriptions, found {len(rows)}")

    output = overlay.transform_plugin(source, rows)
    overlay.verify_overlay(source, output, rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(output)
    args.ledger.parent.mkdir(parents=True, exist_ok=True)
    args.ledger.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "source": str(args.source),
                "source_sha256": hashlib.sha256(source).hexdigest(),
                "output": str(args.output),
                "output_sha256": hashlib.sha256(output).hexdigest(),
                "output_bytes": len(output),
                "ledger": str(args.ledger),
                "rows": len(rows),
                "version": args.version,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
