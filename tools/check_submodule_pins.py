#!/usr/bin/env python3
"""Reject pushes that introduce submodule pins unavailable from remotes."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
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


def _is_git_worktree(path: Path) -> bool:
    # An empty, deinitialized submodule directory otherwise makes `git -C`
    # walk upward and report the parent repository as its worktree.
    if not (path / ".git").exists():
        return False
    result = _git(path, "rev-parse", "--is-inside-work-tree", check=False)
    return result.returncode == 0 and result.stdout.strip() == "true"


def _has_commit(repo: Path, sha: str) -> bool:
    return _git(repo, "cat-file", "-e", f"{sha}^{{commit}}", check=False).returncode == 0


def _all_remote_refs(repo: Path) -> list[str]:
    result = _git(repo, "for-each-ref", "--format=%(refname)", "refs/remotes")
    return [ref for ref in result.stdout.splitlines() if not ref.endswith("/HEAD")]


def _reachable_from_remote(repo: Path, sha: str) -> bool:
    for ref in _all_remote_refs(repo):
        if _git(repo, "merge-base", "--is-ancestor", sha, ref, check=False).returncode == 0:
            return True
    return False


def _remotes(repo: Path) -> list[str]:
    result = _git(repo, "remote", check=False)
    return result.stdout.split() if result.returncode == 0 else []


def _remote_branches_containing(repo: Path, sha: str) -> list[str]:
    result = _git(
        repo,
        "for-each-ref",
        f"--contains={sha}",
        "--format=%(refname:short)",
        "refs/remotes",
    )
    # `refs/remotes/<remote>/HEAD` 的 refname:short 就是 `<remote>`（沒有 `/HEAD` 後綴），
    # 所以只濾後綴會讓它以「一個叫 fork 的分支」的樣子漏出來。真正的分支一定含 `/`。
    return [
        ref
        for ref in result.stdout.splitlines()
        if "/" in ref and not ref.endswith("/HEAD")
    ]


def _remote_default_branch(repo: Path, remote: str) -> str | None:
    result = _git(
        repo,
        "symbolic-ref",
        "--quiet",
        "--short",
        f"refs/remotes/{remote}/HEAD",
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _local_branches_containing(repo: Path, sha: str) -> list[str]:
    result = _git(
        repo,
        "for-each-ref",
        f"--contains={sha}",
        "--format=%(refname:short)",
        "refs/heads",
    )
    return result.stdout.splitlines()


def _current_branch(repo: Path) -> str | None:
    result = _git(repo, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def _remote_for_branch(repo: Path, branch: str | None) -> str:
    if branch:
        result = _git(repo, "config", "--get", f"branch.{branch}.remote", check=False)
        if result.returncode == 0 and result.stdout.strip() not in {"", "."}:
            return result.stdout.strip()
    remotes = _git(repo, "remote").stdout.splitlines()
    if "origin" in remotes:
        return "origin"
    return remotes[0] if remotes else "origin"


def _default_branch(repo: Path, remote: str) -> str:
    result = _git(
        repo,
        "symbolic-ref",
        "--quiet",
        "--short",
        f"refs/remotes/{remote}/HEAD",
        check=False,
    )
    if result.returncode == 0:
        return result.stdout.strip().removeprefix(f"{remote}/")
    return "main"


def push_target(repo: Path, sha: str) -> tuple[str, str]:
    branches = _local_branches_containing(repo, sha)
    current = _current_branch(repo)
    branch = current if current in branches else (branches[0] if branches else None)
    remote = _remote_for_branch(repo, branch)
    if branch:
        return remote, branch
    return remote, f"HEAD:{_default_branch(repo, remote)}"


def warn_if_pin_depends_on_side_branch(
    repo: Path,
    pin: Pin,
    output: TextIO,
) -> None:
    # 一個 submodule 可以有多個 remote（houseCARL：`origin` 是上游、`fork` 是自有 fork，
    # pin 住的是 fork 那邊）。只看 push_target 選中的那一個，會把「在另一個 remote 的
    # 預設分支上」誤判成「掛在側分支上」。**任何一個** remote 的預設分支含得到就夠了。
    default_branches: list[str] = []
    for candidate in _remotes(repo):
        tip = remote_default_tip(repo, candidate)
        branch = _remote_default_branch(repo, candidate)
        if tip is None or branch is None:
            continue
        default_branches.append(branch)
        if _git(
            repo,
            "merge-base",
            "--is-ancestor",
            pin.sha,
            tip,
            check=False,
        ).returncode == 0:
            return
    if not default_branches:
        return
    default_branch = ", ".join(default_branches)

    containing = _remote_branches_containing(repo, pin.sha)
    branches = ", ".join(containing) if containing else "(none found)"
    print(
        f"WARN: {pin.path} @ {pin.sha[:12]} is available remotely, but remote "
        f"default branch(es) {default_branch} do not contain this pin; remote "
        f"branches containing it: {branches}. This pin depends on those side "
        "branches remaining available.",
        file=output,
    )


def check_updates(
    repo: Path,
    remote: str,
    updates: list[PushUpdate],
    output: TextIO,
) -> int:
    pins: set[Pin] = set()
    for update in updates:
        pins.update(pins_for_update(repo, remote, update))

    if not pins:
        print("submodule-pin-guard: no gitlink changes in this push; allowing push.", file=output)
        return 0

    blocked: list[tuple[Pin, str, str]] = []
    for pin in sorted(pins, key=lambda item: (item.path, item.sha)):
        submodule = repo / pin.path
        short_sha = pin.sha[:12]
        if not _is_git_worktree(submodule):
            print(
                f"WARN: {pin.path} @ {short_sha}: submodule is not initialized; "
                "allowing this pin.",
                file=output,
            )
            continue
        if not _has_commit(submodule, pin.sha):
            print(
                f"WARN: {pin.path} @ {short_sha}: commit is not present locally; "
                "allowing this pin.",
                file=output,
            )
            continue
        if _reachable_from_remote(submodule, pin.sha):
            print(f"OK: {pin.path} @ {short_sha} is available remotely.", file=output)
            warn_if_pin_depends_on_side_branch(submodule, pin, output)
            continue

        sub_remote, branch = push_target(submodule, pin.sha)
        fetch = _git(submodule, "fetch", "--quiet", sub_remote, check=False)
        if _reachable_from_remote(submodule, pin.sha):
            print(
                f"OK: {pin.path} @ {short_sha} is available remotely after fetch.",
                file=output,
            )
            warn_if_pin_depends_on_side_branch(submodule, pin, output)
            continue
        if fetch.returncode != 0:
            print(
                f"WARN: git -C {pin.path} fetch --quiet {sub_remote} failed; "
                "the pin is still not available remotely.",
                file=output,
            )
        blocked.append((pin, sub_remote, branch))

    if not blocked:
        return 0

    print("ERROR: refusing parent-repo push; changed submodule pin(s) are unpublished:", file=output)
    for pin, sub_remote, branch in blocked:
        print(f"  - {pin.path} @ {pin.sha[:12]}", file=output)
        print(f"    git -C {pin.path} push {sub_remote} {branch}", file=output)
    print("Push the submodule commit(s), then retry this push.", file=output)
    print("Emergency bypass: git push --no-verify ...", file=output)
    return 1


def main(
    argv: list[str] | None = None,
    stdin: TextIO | None = None,
    stdout: TextIO | None = None,
) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hook_remote", nargs="?", help="remote name supplied by git")
    parser.add_argument("hook_url", nargs="?", help="remote URL supplied by git")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--remote", help="override the parent-repo remote name")
    parser.add_argument(
        "--update",
        nargs=4,
        action="append",
        metavar=("LOCAL_REF", "LOCAL_SHA", "REMOTE_REF", "REMOTE_SHA"),
        help="push update to check instead of reading stdin; may be repeated",
    )
    args = parser.parse_args(argv)
    input_stream = stdin if stdin is not None else sys.stdin
    output = stdout if stdout is not None else sys.stdout
    try:
        updates = (
            [PushUpdate(*fields) for fields in args.update]
            if args.update
            else parse_updates(input_stream)
        )
        repo = args.repo.resolve()
        remote = args.remote or args.hook_remote or "origin"
        return check_updates(repo, remote, updates, output)
    except (subprocess.CalledProcessError, ValueError) as exc:
        print(f"submodule-pin-guard: ERROR: {exc}", file=output)
        return 2


if __name__ == "__main__":
    sys.exit(main())
