#!/usr/bin/env python3
"""Check that the Subtitles temporary-string lifetime bug stays fixed."""

from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_patch.py path/to/src/SubtitleManager.cpp", file=sys.stderr)
        return 2

    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    required = (
        "const auto subtitleText = bigSubtitle.str();",
        "if (!subtitleText.empty())",
        "RE::GFxValue asStr(subtitleText.c_str());",
    )
    forbidden = (
        "RE::GFxValue asStr(bigSubtitle.str().c_str());",
        "if (bigSubtitle.str().length() > 0)",
    )

    missing = [text for text in required if text not in source]
    present = [text for text in forbidden if text in source]
    if missing or present:
        for text in missing:
            print(f"missing: {text}", file=sys.stderr)
        for text in present:
            print(f"forbidden: {text}", file=sys.stderr)
        return 1

    print("Subtitles lifetime patch: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

