#!/usr/bin/env python3
"""Shared path guard for the BodySlide workflow tools (stdlib only, no writes).

Every BodySlide tool that writes (stage, sandbox runner) must refuse to put a
writable or tool path under the live MO2 tree. ``live_roots`` collects the live
roots from explicit arguments first, then environment variables; nothing about
this machine is hard-coded. ``check_isolated`` compares realpaths in both
directions: a path inside a live root is refused, and so is a path that
*contains* a live root (binding ``$HOME`` writable would expose ``mods/``).

Environment fallbacks (used only when the matching argument is omitted):
  MO2_DIR            -> <MO2_DIR>/mods, <MO2_DIR>/overwrite, <MO2_DIR>/profiles
  MO2_MODS_DIR       -> mods directory
  MO2_OVERWRITE_DIR  -> overwrite directory
  SKYRIM_GAME_DATA   -> game Data directory
  SKYRIM_REPO        -> <SKYRIM_REPO>/instance
When SKYRIM_REPO is unset, the instance directory is derived from git
(superproject of this file's repo, else this repo) -- never by counting
parent directories.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess

REQUIRED = ('mods', 'overwrite', 'game_data', 'instance')


def _git_root(start: Path) -> Path | None:
    for args in (('rev-parse', '--show-superproject-working-tree'), ('rev-parse', '--show-toplevel')):
        try:
            out = subprocess.run(['git', '-C', str(start), *args], capture_output=True,
                                 text=True, timeout=10, check=False).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None
        if out:
            return Path(out)
    return None


def live_roots(mo2_dir=None, mods=None, overwrite=None, game_data=None, instance=None,
               extra=(), env=None):
    """Return ({label: Path}, [missing labels]). Explicit arguments win over env."""
    env = os.environ if env is None else env
    base = mo2_dir or env.get('MO2_DIR')
    roots = {
        'mods': mods or env.get('MO2_MODS_DIR') or (base and Path(base) / 'mods'),
        'overwrite': overwrite or env.get('MO2_OVERWRITE_DIR') or (base and Path(base) / 'overwrite'),
        'game_data': game_data or env.get('SKYRIM_GAME_DATA'),
        'instance': instance or (env.get('SKYRIM_REPO') and Path(env['SKYRIM_REPO']) / 'instance'),
    }
    if base:
        roots['profiles'] = Path(base) / 'profiles'
    if not roots['instance']:
        root = _git_root(Path(__file__).resolve().parent)
        roots['instance'] = root / 'instance' if root else None
    for i, path in enumerate(extra or ()):
        roots[f'extra{i}'] = path
    missing = [k for k in REQUIRED if not roots.get(k)]
    return {k: Path(v).expanduser() for k, v in roots.items() if v}, missing


def real(path) -> Path:
    return Path(os.path.realpath(Path(path).expanduser()))


def check_isolated(paths, roots):
    """Return a list of error strings; empty means every path is outside every live root."""
    errors = []
    live = {label: real(p) for label, p in roots.items()}
    for name, path in paths.items():
        p = real(path)
        if p == Path(p.anchor):
            errors.append(f'{name}: refusing filesystem root {p}')
            continue
        for label, root in live.items():
            if p == root or p.is_relative_to(root):
                errors.append(f'{name}: {p} is inside live {label} root {root}')
            elif root.is_relative_to(p):
                errors.append(f'{name}: {p} contains live {label} root {root}')
    return errors


def non_ascii(path) -> bool:
    return any(ord(c) > 127 for c in str(path))
