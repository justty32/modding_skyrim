#!/usr/bin/env python3
"""Check inline local links in the parent repo's tracked Markdown files."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


def repo_root() -> Path:
    output = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    )
    return Path(output.strip()).resolve()


def tracked_markdown(root: Path) -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--", "*.md"], cwd=root
    )
    return [root / name.decode() for name in output.rstrip(b"\0").split(b"\0") if name]


def link_target(raw: str) -> str | None:
    value = raw.strip()
    if value.startswith("<"):
        closing = value.find(">")
        if closing < 0:
            return value
        value = value[1:closing]
    else:
        value = value.split(maxsplit=1)[0]
    value = unquote(value)
    if not value or value.startswith(("#", "//")):
        return None
    if urlsplit(value).scheme:
        return None
    return value.split("#", 1)[0].split("?", 1)[0]


def markdown_links(markdown: Path):
    fence: str | None = None
    for line_number, line in enumerate(
        markdown.read_text(encoding="utf-8").splitlines(), 1
    ):
        marker = FENCE_RE.match(line)
        if marker:
            current = marker.group(1)[0]
            if fence is None:
                fence = current
            elif fence == current:
                fence = None
            continue
        if fence is not None:
            continue
        for match in LINK_RE.finditer(line):
            target = link_target(match.group(1))
            if target:
                yield line_number, target


def check_file(source: Path, root: Path) -> tuple[int, list[tuple[int, str, Path]]]:
    if source.is_symlink():
        try:
            markdown = source.resolve(strict=True)
        except FileNotFoundError:
            return 0, [(1, str(source.readlink()), source.resolve())]
    else:
        markdown = source.resolve()

    checked = 0
    broken: list[tuple[int, str, Path]] = []
    for line_number, target in markdown_links(markdown):
        checked += 1
        candidate = Path(target)
        if candidate.is_absolute():
            resolved = root / target.lstrip("/")
        else:
            resolved = markdown.parent / candidate
        resolved = resolved.resolve()
        if not resolved.exists():
            broken.append((line_number, target, resolved))
    return checked, broken


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-symlinks",
        action="store_true",
        help="skip tracked Markdown symlinks whose canonical files live in submodules",
    )
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args(argv)

    root = repo_root()
    sources = args.paths or tracked_markdown(root)
    skipped_symlinks = 0
    if args.skip_symlinks:
        skipped_symlinks = sum(source.is_symlink() for source in sources)
        sources = [source for source in sources if not source.is_symlink()]
    total_links = 0
    broken_count = 0
    for source in sources:
        try:
            display = source.resolve().relative_to(root)
        except ValueError:
            display = source
        checked, broken = check_file(source, root)
        total_links += checked
        for line_number, target, resolved in broken:
            broken_count += 1
            print(f"{display}:{line_number}: broken local link: {target} -> {resolved}")

    if broken_count:
        print(f"Markdown links FAILED: {broken_count} broken local link(s)")
        return 1
    suffix = f", {skipped_symlinks} symlink(s) skipped" if skipped_symlinks else ""
    print(f"Markdown links OK: {len(sources)} file(s), {total_links} local link(s){suffix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
