#!/usr/bin/env python3
"""Build the Skyrim translation asset from the reviewable UTF-8 TSV source."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "translation-source.tsv"
OUTPUT = ROOT / "Interface" / "Translations" / "BetterThirdPersonSelection_ENGLISH.txt"


def read_rows(path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    seen: set[str] = set()
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        if line.count("\t") != 1:
            raise ValueError(f"{path}:{number}: expected exactly one tab")
        key, value = line.split("\t")
        if not key.startswith("$") or not value:
            raise ValueError(f"{path}:{number}: expected a non-empty $key and translation")
        if key in seen:
            raise ValueError(f"{path}:{number}: duplicate key {key}")
        seen.add(key)
        rows.append((key, value))
    return rows


def main() -> None:
    rows = read_rows(SOURCE)
    text = "\r\n".join(f"{key}\t{value}" for key, value in rows)
    # Skyrim expects UTF-16LE with BOM. Deliberately no final CRLF, matching 0.8.9.
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(b"\xff\xfe" + text.encode("utf-16le"))
    print(f"Wrote {OUTPUT.relative_to(ROOT)}: {len(rows)} rows, UTF-16LE BOM, CRLF")


if __name__ == "__main__":
    main()
