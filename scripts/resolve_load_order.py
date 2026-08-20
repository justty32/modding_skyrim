#!/usr/bin/env python3
"""Resolve an MO2 profile's enabled load order to real plugin file paths."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

DEFAULT_MO2 = Path("/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2")
DEFAULT_GAME_DATA = Path(
    "/home/lorkhan/.local/share/Steam/steamapps/common/Skyrim Special Edition/Data"
)


def lines(path: Path) -> list[str]:
    return [l.strip() for l in path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
            if l.strip() and not l.startswith("#")]


def resolve(profile: Path, mo2: Path, game_data: Path) -> tuple[list[tuple[str, Path]], list[str], int, int]:
    order = lines(profile / "loadorder.txt")
    # plugins.txt omits implicitly-always-on masters (vanilla + Creation Club)
    # and lists an explicitly disabled plugin without `*`. Absent therefore
    # means enabled; only a listed-but-unstarred entry is disabled.
    plugin_lines = lines(profile / "plugins.txt")
    listed = {line.lstrip("*").lower() for line in plugin_lines}
    starred = {line[1:].lower() for line in plugin_lines if line.startswith("*")}
    enabled = starred | {name.lower() for name in order if name.lower() not in listed}
    # modlist.txt is highest-priority-first.
    mods = [line[1:] for line in lines(profile / "modlist.txt") if line.startswith("+")]

    missing: list[str] = []
    resolved: list[tuple[str, Path]] = []
    for name in order:
        if name.lower() not in enabled:
            continue

        # MO2's shared overwrite is the virtual Data tree's highest-priority
        # provider. It must win before every named mod and the physical game
        # Data directory, even though it has no `+` line in modlist.txt.
        candidates = [mo2 / "overwrite" / name]
        candidates.extend(mo2 / "mods" / mod / name for mod in mods)
        candidates.append(game_data / name)
        hit = next((candidate for candidate in candidates if candidate.is_file()), None)
        if hit is None:
            missing.append(name)
        else:
            resolved.append((name, hit))
    return resolved, missing, len(order), len(enabled)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", default="Modpack-KR")
    parser.add_argument("--mo2-root", type=Path, default=DEFAULT_MO2)
    parser.add_argument("--game-data", type=Path, default=DEFAULT_GAME_DATA)
    args = parser.parse_args(argv)

    profile = args.mo2_root / "profiles" / args.profile
    resolved, missing, order_count, enabled_count = resolve(
        profile, args.mo2_root, args.game_data
    )
    for unused_name, path in resolved:
        print(path)
    print(
        f"-- {len(resolved)} resolved, {len(missing)} missing, "
        f"{order_count} in loadorder, {enabled_count} enabled",
        file=sys.stderr,
    )
    for name in missing:
        print(f"MISSING: {name}", file=sys.stderr)
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
