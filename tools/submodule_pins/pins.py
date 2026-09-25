"""Read push updates and calculate changed gitlink pins with Git."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import TextIO


@dataclass(frozen=True)
class PushUpdate:
    local_ref: str
    local_sha: str
    remote_ref: str
    remote_sha: str


@dataclass(frozen=True)
class Pin:
    path: str
    sha: str


def _git(
    repo: Path,
    *args: str,
    check: bool = True,
    text: bool = True,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )


def _is_zero(sha: str) -> bool:
    return bool(sha) and set(sha) == {"0"}


def parse_updates(lines: TextIO) -> list[PushUpdate]:
    updates: list[PushUpdate] = []
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 4:
            raise ValueError(
                f"stdin line {number}: expected local_ref local_sha "
                "remote_ref remote_sha"
            )
        updates.append(PushUpdate(*fields))
    return updates


def _configured_remote(repo: Path, remote: str) -> bool:
    result = _git(repo, "remote", "get-url", remote, check=False)
    return result.returncode == 0


def remote_default_tip(repo: Path, remote: str) -> str | None:
    if not _configured_remote(repo, remote):
        return None
    result = _git(
        repo,
        "rev-parse",
        "--verify",
        f"refs/remotes/{remote}/HEAD^{{commit}}",
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _pins_from_raw_diff(data: bytes) -> set[Pin]:
    fields = data.split(b"\0")
    pins: set[Pin] = set()
    index = 0
    while index < len(fields) and fields[index]:
        header = fields[index].decode("ascii")
        if index + 1 >= len(fields):
            raise ValueError("incomplete git raw diff")
        path = fields[index + 1].decode("utf-8", errors="surrogateescape")
        parts = header.split()
        if len(parts) != 5:
            raise ValueError(f"unexpected git raw diff header: {header}")
        new_mode, new_sha, status = parts[1], parts[3], parts[4]
        if new_mode == "160000" and not status.startswith("D"):
            pins.add(Pin(path, new_sha))
        index += 2
    return pins


def changed_gitlinks(repo: Path, old_sha: str, new_sha: str) -> set[Pin]:
    result = _git(
        repo,
        "diff",
        "--raw",
        "--no-abbrev",
        "--no-renames",
        "--no-ext-diff",
        "-z",
        old_sha,
        new_sha,
        "--",
        text=False,
    )
    return _pins_from_raw_diff(result.stdout)


def _remote_refs(repo: Path, remote: str) -> list[str]:
    if not _configured_remote(repo, remote):
        return []
    result = _git(
        repo,
        "for-each-ref",
        "--format=%(refname)",
        f"refs/remotes/{remote}",
    )
    return [ref for ref in result.stdout.splitlines() if not ref.endswith("/HEAD")]


def _gitlinks_in_tree(repo: Path, commit: str) -> set[Pin]:
    result = _git(repo, "ls-tree", "-rz", commit, text=False)
    pins: set[Pin] = set()
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, _kind, sha = metadata.decode("ascii").split()
        if mode == "160000":
            pins.add(
                Pin(raw_path.decode("utf-8", errors="surrogateescape"), sha)
            )
    return pins


def new_branch_gitlinks(repo: Path, remote: str, new_sha: str) -> set[Pin]:
    """Return gitlinks present in commits that do not exist on the remote."""
    args = ["rev-list", new_sha]
    remote_refs = _remote_refs(repo, remote)
    if remote_refs:
        args.extend(["--not", *remote_refs])
    result = _git(repo, *args)
    pins: set[Pin] = set()
    for commit in result.stdout.splitlines():
        pins.update(_gitlinks_in_tree(repo, commit))
    return pins


def pins_for_update(repo: Path, remote: str, update: PushUpdate) -> set[Pin]:
    if _is_zero(update.local_sha):
        return set()
    if _is_zero(update.remote_sha):
        baseline = remote_default_tip(repo, remote)
        if baseline is None:
            return new_branch_gitlinks(repo, remote, update.local_sha)
        return changed_gitlinks(repo, baseline, update.local_sha)
    return changed_gitlinks(repo, update.remote_sha, update.local_sha)


