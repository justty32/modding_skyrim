#!/usr/bin/env python3
"""Reject pushes that introduce submodule pins unavailable from remotes."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
from typing import TextIO


from submodule_pins.pins import (
    PushUpdate,
    Pin,
    _git,
    _is_zero,
    parse_updates,
    _configured_remote,
    remote_default_tip,
    _pins_from_raw_diff,
    changed_gitlinks,
    _remote_refs,
    _gitlinks_in_tree,
    new_branch_gitlinks,
    pins_for_update,
)
from submodule_pins.branches import (
    _is_git_worktree,
    _has_commit,
    _all_remote_refs,
    _reachable_from_remote,
    _remotes,
    _remote_branches_containing,
    _remote_default_branch,
    _local_branches_containing,
    _current_branch,
    _remote_for_branch,
    _default_branch,
    push_target,
    warn_if_pin_depends_on_side_branch,
)
from submodule_pins.guard import (
    RECURSE_PUBLISHES,
    _push_recurse_mode,
    check_updates,
)


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
