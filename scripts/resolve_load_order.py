#!/usr/bin/env python3
"""Resolve the MO2 profile's enabled load order to real plugin file paths.

MO2 on Linux has no live VFS to read, so the winner for each plugin filename is
found the way MO2 itself would: walk enabled mods from highest priority (first
line of modlist.txt) down, then fall back to the game's own Data directory.
"""
import sys
from pathlib import Path

MO2 = Path("/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2")
GAME_DATA = Path("/home/lorkhan/.local/share/Steam/steamapps/common/Skyrim Special Edition/Data")
PROFILE = MO2 / "profiles" / (sys.argv[1] if len(sys.argv) > 1 else "Play-KR")


def lines(path):
    return [l.strip() for l in path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
            if l.strip() and not l.startswith("#")]


order = lines(PROFILE / "loadorder.txt")
# plugins.txt omits the implicitly-always-on masters (vanilla + Creation Club)
# entirely, and lists an explicitly disabled plugin without its `*`. So absent
# means enabled, and only a listed-but-unstarred entry is really off.
listed = {l.lstrip("*").lower() for l in lines(PROFILE / "plugins.txt")}
starred = {l[1:].lower() for l in lines(PROFILE / "plugins.txt") if l.startswith("*")}
enabled = starred | {n.lower() for n in order if n.lower() not in listed}
# modlist.txt is highest-priority-first; MO2 resolves later (lower) mods first losing.
mods = [l[1:] for l in lines(PROFILE / "modlist.txt") if l.startswith("+")]

missing, resolved = [], []
for name in order:
    if name.lower() not in enabled:
        continue
    hit = None
    for mod in mods:                       # highest priority first == first hit wins
        cand = MO2 / "mods" / mod / name
        if cand.is_file():
            hit = cand
            break
    if hit is None:
        cand = GAME_DATA / name
        if cand.is_file():
            hit = cand
    if hit is None:
        missing.append(name)
    else:
        resolved.append((name, hit))

for name, path in resolved:
    print(path)

print(f"-- {len(resolved)} resolved, {len(missing)} missing, "
      f"{len(order)} in loadorder, {len(enabled)} enabled", file=sys.stderr)
for name in missing:
    print(f"MISSING: {name}", file=sys.stderr)
