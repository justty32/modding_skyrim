#!/usr/bin/env python3
"""Rewrite MANIFEST.sha256 with complete, deterministic package coverage."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"


def main() -> None:
    files = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and path != MANIFEST and "__pycache__" not in path.parts
    )
    lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT).as_posix()}"
        for path in files
    ]
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST}: {len(lines)} files")


if __name__ == "__main__":
    main()
