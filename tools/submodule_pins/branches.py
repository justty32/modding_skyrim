"""Inspect remote availability and infer branch push targets."""

from __future__ import annotations

from pathlib import Path
from typing import TextIO

from .pins import Pin, _git, remote_default_tip


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


