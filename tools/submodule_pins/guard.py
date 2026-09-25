"""Check changed submodule pins and report push guidance."""

from __future__ import annotations

from pathlib import Path
from typing import TextIO

from .pins import Pin, PushUpdate, _git, pins_for_update
from .branches import (
    _is_git_worktree, _has_commit, _reachable_from_remote,
    push_target, warn_if_pin_depends_on_side_branch,
)


# `push.recurseSubmodules` values that make git publish the submodule commits
# itself, as part of the very push this hook is gating. `on-demand` pushes each
# changed submodule then the parent; `only` pushes the submodules and skips the
# parent. In both cases refusing here is refusing the fix -- the hook runs
# BEFORE git recurses, so it never gets to see that git was about to do exactly
# what the error message asks the user to do by hand. Verified 2026-08-26 on a
# throwaway parent/submodule pair: with the hook off, one `git push` published
# both; with the hook on and no awareness of this setting, it blocked.
#
# `check` is deliberately not in this set: it makes git perform its own version
# of this check, and this hook's message is the more actionable of the two.
RECURSE_PUBLISHES = ("on-demand", "only")


def _push_recurse_mode(repo: Path) -> str:
    result = _git(repo, "config", "--get", "push.recurseSubmodules", check=False)
    return result.stdout.strip() if result.returncode == 0 else ""


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

    mode = _push_recurse_mode(repo)
    if mode in RECURSE_PUBLISHES:
        print(
            f"push.recurseSubmodules={mode}: git will publish the unpublished pin(s) "
            "as part of this push; allowing.",
            file=output,
        )
        for pin, _sub_remote, _branch in blocked:
            print(f"  - {pin.path} @ {pin.sha[:12]}", file=output)
        return 0

    print("ERROR: refusing parent-repo push; changed submodule pin(s) are unpublished:", file=output)
    for pin, sub_remote, branch in blocked:
        print(f"  - {pin.path} @ {pin.sha[:12]}", file=output)
        print(f"    git -C {pin.path} push {sub_remote} {branch}", file=output)
    print("Push the submodule commit(s), then retry this push.", file=output)
    print(
        "Or stop doing this by hand: `git config push.recurseSubmodules on-demand`\n"
        "makes one `git push` publish the submodule commits and then the parent.",
        file=output,
    )
    print("Emergency bypass: git push --no-verify ...", file=output)
    return 1


