#!/usr/bin/env python3
"""Check inline local links in this workspace's Markdown files.

Scope is "tracked, plus untracked-but-not-ignored" — not "tracked". Listing
only `git ls-files` made the check lie about brand-new documents: on
2026-10-23 the anlz line wrote four index files, ran this checker, got
`OK: 5532 file(s)`, and none of the four had been read. They only entered the
scan after `git add`. Ignored paths stay out either way, which is what keeps
third-party clones (analysis/tool-survey/repos/, external/frameworks/) from
being dragged in.
"""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import subprocess
import sys

from markdown_links.parsing import (
    LINK_RE, FENCE_RE, CODE_SPAN_RE, HEADING_RE, SETEXT_RE,
    EXPLICIT_ANCHOR_RE, LocalTarget, link_target, github_heading_slug,
    markdown_anchors, markdown_links, check_file,
)


def repo_root() -> Path:
    output = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    )
    return Path(output.strip()).resolve()


def _ls_files(cwd: Path, pattern: str) -> list[str]:
    output = subprocess.check_output(["git", "ls-files", "-z", "--", pattern], cwd=cwd)
    return [name.decode() for name in output.rstrip(b"\0").split(b"\0") if name]


def _ls_others(cwd: Path, pattern: str) -> list[str]:
    """Untracked and not ignored. `--exclude-standard` is what keeps the
    gitignored third-party clones and handoff scratch out of the scan."""
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--others", "--exclude-standard", "--", pattern],
        cwd=cwd,
    )
    return [name.decode() for name in output.rstrip(b"\0").split(b"\0") if name]


def _readable(base: Path, names: list[str]) -> list[Path]:
    # `git ls-files` also returns tracked files deleted from a dirty worktree.
    # They have no links left to validate and trying to read them aborts the
    # whole check. Keep broken symlinks, though: check_file reports those.
    return [
        source
        for name in names
        if (source := base / name).exists() or source.is_symlink()
    ]


def _markdown_under(root: Path, lister) -> list[Path]:
    """Walk the parent repo and every initialized workspace submodule.

    `git ls-files` stops at the gitlink, so a plain listing covers only the
    parent repo. The four lines split out on 2026-08-23 carried 87 links that
    no longer resolved and nothing was looking at them. `--others` stops at a
    nested repository too, so each submodule needs its own invocation and no
    path is listed twice.
    """
    sources = _readable(root, lister(root, "*.md"))
    for gitlink in _ls_files(root, "*"):
        # projects/* are independent software repos with their own link
        # conventions (line-number references that are not links at all) and
        # their own CI. The four workspace lines are woven into this repo's
        # docs, so they are in scope.
        if gitlink.startswith("projects/"):
            continue
        sub = root / gitlink
        if (sub / ".git").exists():
            sources += _readable(sub, lister(sub, "*.md"))
    return sources


def tracked_markdown(root: Path) -> list[Path]:
    """Every tracked .md, submodules included."""
    return _markdown_under(root, _ls_files)


def untracked_markdown(root: Path) -> list[Path]:
    """Every untracked-but-not-ignored .md, submodules included.

    Without this the checker goes green on files it never opened; see the
    module docstring.
    """
    return _markdown_under(root, _ls_others)


def uninitialized_submodules(root: Path) -> list[Path]:
    """Declared gitlinks absent from a public checkout, not arbitrary missing dirs."""
    entries = subprocess.check_output(
        ["git", "ls-files", "--stage", "-z"], cwd=root
    ).decode().split("\0")
    missing = []
    for entry in entries:
        if not entry.startswith("160000 "):
            continue
        path = root / entry.split("\t", 1)[1]
        if not (path / ".git").exists():
            missing.append(path.resolve())
    return missing


def source_is_excluded(source: Path, root: Path, patterns: list[str]) -> bool:
    try:
        relative = source.absolute().relative_to(root).as_posix()
    except ValueError:
        return False
    for raw_pattern in patterns:
        pattern = raw_pattern.replace("\\", "/")
        while pattern.startswith("./"):
            pattern = pattern[2:]
        path_pattern = pattern.rstrip("/")
        if relative == path_pattern or relative.startswith(f"{path_pattern}/"):
            return True
        if PurePosixPath(relative).match(pattern):
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-symlinks",
        action="store_true",
        help="skip tracked Markdown symlinks whose canonical files live in submodules",
    )
    parser.add_argument(
        "--exclude-source",
        action="append",
        default=[],
        metavar="PATH_OR_GLOB",
        help="skip source Markdown files matching a repo-relative path or glob",
    )
    parser.add_argument(
        "--skip-uninitialized-submodules",
        action="store_true",
        help="report but do not fail for targets inside uninitialized gitlinks",
    )
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args(argv)

    root = repo_root()
    if args.paths:
        sources = args.paths
        untracked_set: set[Path] | None = None
    else:
        untracked = untracked_markdown(root)
        sources = tracked_markdown(root) + untracked
        untracked_set = set(untracked)
    excluded_sources = sum(
        source_is_excluded(source, root, args.exclude_source) for source in sources
    )
    if excluded_sources:
        sources = [
            source
            for source in sources
            if not source_is_excluded(source, root, args.exclude_source)
        ]
    skipped_symlinks = 0
    if args.skip_symlinks:
        skipped_symlinks = sum(source.is_symlink() for source in sources)
        sources = [source for source in sources if not source.is_symlink()]
    unavailable = uninitialized_submodules(root) if args.skip_uninitialized_submodules else []
    skipped_targets = 0
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
            if any(resolved == sub or sub in resolved.parents for sub in unavailable):
                skipped_targets += 1
                total_links -= 1
                continue
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
    # Say what was scanned, so a green run cannot be mistaken for coverage it
    # does not have. `untracked 0` means "nothing new is sitting outside the
    # index", not "untracked files are skipped".
    breakdown = ""
    if untracked_set is not None:
        scanned_untracked = sum(source in untracked_set for source in sources)
        breakdown = (
            f" (tracked {len(sources) - scanned_untracked}, "
            f"untracked {scanned_untracked})"
        )
    suffixes = []
    if excluded_sources:
        suffixes.append(f"{excluded_sources} source(s) excluded")
    if skipped_symlinks:
        suffixes.append(f"{skipped_symlinks} symlink(s) skipped")
    if skipped_targets:
        suffixes.append(f"{skipped_targets} target(s) not checked in uninitialized submodules")
    suffix = f", {', '.join(suffixes)}" if suffixes else ""
    if broken_count:
        print(
            f"Markdown links FAILED: {broken_count} broken local link(s) "
            f"({missing_files} missing file(s), {missing_anchors} missing anchor(s))"
            f" in {len(sources)} file(s){breakdown}{suffix}"
        )
        return 1
    print(
        f"Markdown links OK: {len(sources)} file(s){breakdown}, "
        f"{total_links} local link(s){suffix}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
