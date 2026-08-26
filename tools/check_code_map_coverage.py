#!/usr/bin/env python3
"""Fail when a workspace tool script is indexed nowhere an agent will look.

`AGENTS.md` sends every agent that touches source code to
`wf/workflows/common/code-map/CODE_MAP.md`, and that page states its own rule:

    新增／刪除原始碼檔案或改變職責時，先更新目標 repo 的 CODE_MAP；
    目標 repo 沒有細分 CODE_MAP 時，才維護本頁的快速圖或 README 入口。

The four workspace lines (`instance/`, `mod-library/`, `modpack-design/`,
`agentctl/`) were split out of the mother repo on 2026-08-23 and none of them
grew a CODE_MAP or a `tools/README.md`. By the rule above their scripts are the
mother CODE_MAP's responsibility -- but the page kept the handful it already
listed and never tracked the rest. A tool nobody indexes is a tool the next
agent rewrites from scratch.

This is the same failure mode `check_markdown_links.py` had: a checker whose
coverage stopped following the structure after a split. So this checker walks
the submodules explicitly instead of trusting the mother repo's `git ls-files`,
which stops at every gitlink.

The known gap is carried in `tools/code_map_coverage_baseline.txt` as a
ratchet: everything listed there is pre-existing debt and stays quiet, anything
new must be indexed. Deleting a line from the baseline is how the debt is paid
down; the checker also fails on baseline entries whose file is gone, so the
list cannot rot into a permanent excuse.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

# Lines whose tool scripts the mother CODE_MAP is responsible for indexing.
# `projects/*` is deliberately absent: those are code repos that carry their
# own README/CODE_MAP, and CODE_MAP links to their entry points rather than
# inventorying their files.
TOOL_ROOTS = (
    "tools",
    "instance/tools",
    # `check_profiles.py` lives here, not in `instance/tools` -- one submodule
    # deeper, inside `instance/profiles`. Leaving it out was this checker's own
    # first coverage hole, found the same day it was written.
    "instance/profiles/tools",
    "mod-library/db",
    "mod-library/l10n/tools",
    "agentctl/tools",
)

# Pages an entry may be indexed in. A basename mentioned in any of them counts.
INDEX_PAGES = (
    "wf/workflows/common/code-map/CODE_MAP.md",
    "instance/README.md",
    "mod-library/README.md",
    "modpack-design/README.md",
    "agentctl/README.md",
)

SCRIPT_SUFFIXES = (".py", ".sh")

BASELINE = Path("tools/code_map_coverage_baseline.txt")


@dataclass(frozen=True)
class Finding:
    path: str
    reason: str


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _tracked_scripts(repo: Path, root: str) -> list[str]:
    """Tracked scripts under `root`, asking the repo that actually owns them.

    `git ls-files` in the mother repo stops at a gitlink, so a root inside a
    submodule has to be listed by that submodule's own git. Splitting the root
    into (submodule, subpath) keeps the caller from having to know which is
    which.
    """
    parts = root.split("/")
    for depth in range(len(parts), 0, -1):
        candidate = repo / "/".join(parts[:depth])
        if (candidate / ".git").exists():
            inner = "/".join(parts[depth:])
            result = _git(candidate, "ls-files", inner or ".", check=False)
            if result.returncode != 0:
                return []
            prefix = "/".join(parts[:depth])
            return [
                f"{prefix}/{line}" if line else prefix
                for line in result.stdout.splitlines()
                if line
            ]

    result = _git(repo, "ls-files", root, check=False)
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line]


def _indexed_text(repo: Path) -> str:
    chunks = []
    for page in INDEX_PAGES:
        path = repo / page
        if path.is_file():
            chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def _read_baseline(repo: Path) -> set[str]:
    path = repo / BASELINE
    if not path.is_file():
        return set()
    entries = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            entries.add(line)
    return entries


def collect(repo: Path) -> tuple[list[Finding], list[Finding], int]:
    """Return (unindexed, stale_baseline, scripts_examined)."""
    indexed = _indexed_text(repo)
    baseline = _read_baseline(repo)

    unindexed: list[Finding] = []
    seen: set[str] = set()
    examined = 0

    for root in TOOL_ROOTS:
        for rel in _tracked_scripts(repo, root):
            if not rel.endswith(SCRIPT_SUFFIXES):
                continue
            examined += 1
            seen.add(rel)
            if Path(rel).name in indexed:
                continue
            if rel in baseline:
                continue
            unindexed.append(
                Finding(rel, "not named in any index page and not in the baseline")
            )

    stale = [
        Finding(entry, "baselined but no longer a tracked script")
        for entry in sorted(baseline - seen)
    ]
    return unindexed, stale, examined


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        default=".",
        type=Path,
        help="workspace root (default: current directory)",
    )
    parser.add_argument(
        "--list-unindexed",
        action="store_true",
        help="print every unindexed script, baseline included, and exit 0",
    )
    args = parser.parse_args(argv)
    repo = args.repo.resolve()

    unindexed, stale, examined = collect(repo)

    if args.list_unindexed:
        baseline = _read_baseline(repo)
        indexed = _indexed_text(repo)
        for root in TOOL_ROOTS:
            for rel in _tracked_scripts(repo, root):
                if rel.endswith(SCRIPT_SUFFIXES) and Path(rel).name not in indexed:
                    mark = "baselined" if rel in baseline else "NEW"
                    print(f"{mark:>9}  {rel}")
        return 0

    if not unindexed and not stale:
        print(f"code-map coverage OK: {examined} tool script(s) examined")
        return 0

    for finding in unindexed:
        print(f"UNINDEXED  {finding.path}\n           {finding.reason}")
    for finding in stale:
        print(f"STALE      {finding.path}\n           {finding.reason}")

    if unindexed:
        print(
            "\nA tool indexed nowhere is a tool the next agent rewrites. Add it to\n"
            f"  {INDEX_PAGES[0]}\n"
            "or to the owning line's README, then re-run. If it genuinely needs no\n"
            f"entry, say so explicitly in {BASELINE} with a reason."
        )
    if stale:
        print(
            f"\nRemove the stale line(s) from {BASELINE}; the file they excused\n"
            "is gone, so the excuse cannot be verified any more."
        )
    return 1


if __name__ == "__main__":
    sys.exit(main())
