#!/usr/bin/env python3
"""Check inline local links in the parent repo's tracked Markdown files."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")
SETEXT_RE = re.compile(r"^\s{0,3}(?:=+|-+)\s*$")
EXPLICIT_ANCHOR_RE = re.compile(
    r"<(?:a|span)\b[^>]*(?:id|name)\s*=\s*['\"]([^'\"]+)['\"][^>]*>",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class LocalTarget:
    display: str
    path: str
    fragment: str | None


def repo_root() -> Path:
    output = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    )
    return Path(output.strip()).resolve()


def _ls_files(cwd: Path, pattern: str) -> list[str]:
    output = subprocess.check_output(["git", "ls-files", "-z", "--", pattern], cwd=cwd)
    return [name.decode() for name in output.rstrip(b"\0").split(b"\0") if name]


def tracked_markdown(root: Path) -> list[Path]:
    """Every tracked .md, submodules included.

    `git ls-files` stops at the gitlink, so a plain listing covers only the
    parent repo. The four lines split out on 2026-08-23 carried 87 links that
    no longer resolved and nothing was looking at them.
    """
    # `git ls-files` also returns tracked files deleted from a dirty worktree.
    # They have no links left to validate and trying to read them aborts the
    # whole check. Keep broken symlinks, though: check_file reports those.
    sources = [
        source
        for name in _ls_files(root, "*.md")
        if (source := root / name).exists() or source.is_symlink()
    ]
    for gitlink in _ls_files(root, "*"):
        # projects/* are independent software repos with their own link
        # conventions (line-number references that are not links at all) and
        # their own CI. The four workspace lines are woven into this repo's
        # docs, so they are in scope.
        if gitlink.startswith("projects/"):
            continue
        sub = root / gitlink
        if (sub / ".git").exists():
            sources += [
                source
                for name in _ls_files(sub, "*.md")
                if (source := sub / name).exists() or source.is_symlink()
            ]
    return sources


def link_target(raw: str) -> LocalTarget | None:
    value = raw.strip()
    if value.startswith("<"):
        closing = value.find(">")
        if closing < 0:
            return LocalTarget(value, value, None)
        value = value[1:closing]
    else:
        value = value.split(maxsplit=1)[0]
    value = unquote(value)
    if not value or value.startswith("//"):
        return None
    parts = urlsplit(value)
    if parts.scheme:
        return None
    if not parts.path and not parts.fragment:
        return None
    return LocalTarget(value, parts.path, parts.fragment or None)


def github_heading_slug(text: str) -> str:
    """Approximate GitHub's rendered-heading slug for local Markdown links."""
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    # Backticks and asterisks need no special case: the ASCII-punctuation rule
    # below drops them like every other ASCII symbol.
    text = unicodedata.normalize("NFKC", text).strip().lower()
    text = "".join(
        char
        for char in text
        if (
            (not unicodedata.category(char).startswith("P") or char in "-_")
            and not (
                char.isascii()
                and not char.isalnum()
                and not char.isspace()
                and char not in "-_"
            )
        )
    )
    return re.sub(r"\s+", "-", text)


def markdown_anchors(markdown: Path) -> set[str]:
    anchors: set[str] = set()
    duplicate_counts: dict[str, int] = defaultdict(int)
    fence: str | None = None
    previous_line: str | None = None
    for line in markdown.read_text(encoding="utf-8").splitlines():
        marker = FENCE_RE.match(line)
        if marker:
            current = marker.group(1)[0]
            if fence is None:
                fence = current
            elif fence == current:
                fence = None
            previous_line = None
            continue
        if fence is not None:
            continue
        anchors.update(unquote(anchor) for anchor in EXPLICIT_ANCHOR_RE.findall(line))
        heading = HEADING_RE.match(line)
        if heading:
            text = re.sub(r"\s+#+\s*$", "", heading.group(1))
        elif previous_line and SETEXT_RE.match(line):
            text = previous_line.strip()
        else:
            previous_line = line
            continue
        base = github_heading_slug(text)
        if not base:
            continue
        count = duplicate_counts[base]
        duplicate_counts[base] += 1
        anchors.add(base if count == 0 else f"{base}-{count}")
        previous_line = None
    return anchors


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


def check_file(source: Path, root: Path) -> tuple[int, list[tuple[int, str, Path, str]]]:
    if source.is_symlink():
        try:
            markdown = source.resolve(strict=True)
        except FileNotFoundError:
            return 0, [(1, str(source.readlink()), source.resolve(), "")]
    else:
        markdown = source.resolve()

    checked = 0
    # Each entry carries the missing fragment, so an anchor failure can name the
    # anchor instead of pointing at a file that plainly does exist.
    broken: list[tuple[int, str, Path, str]] = []
    for line_number, target in markdown_links(markdown):
        checked += 1
        candidate = Path(target.path)
        if candidate.is_absolute():
            resolved = root / target.path.lstrip("/")
        elif not target.path:
            resolved = markdown
        else:
            resolved = markdown.parent / candidate
        resolved = resolved.resolve()
        if not resolved.exists():
            broken.append((line_number, target.display, resolved, ""))
            continue
        if (
            target.fragment
            and resolved.is_file()
            and resolved.suffix.lower() in {".md", ".markdown"}
            and target.fragment not in markdown_anchors(resolved)
        ):
            broken.append((line_number, target.display, resolved, target.fragment))
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
    missing_files = 0
    missing_anchors = 0
    for source in sources:
        try:
            display = source.resolve().relative_to(root)
        except ValueError:
            display = source
        checked, broken = check_file(source, root)
        total_links += checked
        for line_number, target, resolved, fragment in broken:
            if fragment:
                missing_anchors += 1
                print(
                    f"{display}:{line_number}: broken anchor: {target} -> "
                    f'{resolved} has no "#{fragment}"'
                )
            else:
                missing_files += 1
                print(
                    f"{display}:{line_number}: broken local link: {target} -> {resolved}"
                )

    broken_count = missing_files + missing_anchors
    if broken_count:
        print(
            f"Markdown links FAILED: {broken_count} broken local link(s) "
            f"({missing_files} missing file(s), {missing_anchors} missing anchor(s))"
        )
        return 1
    suffix = f", {skipped_symlinks} symlink(s) skipped" if skipped_symlinks else ""
    print(f"Markdown links OK: {len(sources)} file(s), {total_links} local link(s){suffix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
