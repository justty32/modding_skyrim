#!/usr/bin/env python3
"""Rewrite markdown links that point at moved files.

usage: fix_moved_links.py [--apply] [--prefix <subdir>] <moves.tsv> [[--prefix <subdir>] <moves.tsv> ...]
moves.tsv rows: <old>\t<new>  (paths relative to ROOT, or to ROOT/<subdir> when a
--prefix precedes that tsv — e.g. a submodule line reporting paths relative to its own root)
A row whose old path is a directory is treated as a prefix move.
Scans every git-tracked *.md under ROOT (including submodules) and rewrites
inline links [..](target) / images whose resolved target is a moved file.
"""
import os, re, subprocess, sys

ROOT = "/home/lorkhan/repo/moddings/skyrim"
LINK = re.compile(r'(!?\[[^\]]*\]\()([^)\s]+)(\s+"[^"]*")?(\))')

def tracked_md():
    out = subprocess.run(["git", "ls-files", "--recurse-submodules", "-z"], cwd=ROOT,
                         capture_output=True, check=True).stdout.decode()
    return [os.path.join(ROOT, p) for p in out.split("\0") if p.endswith(".md")]

def load_moves(specs):
    files, dirs = {}, {}
    for p, prefix in specs:
        base = os.path.join(ROOT, prefix) if prefix else ROOT
        for line in open(p, encoding="utf-8"):
            line = line.rstrip("\n")
            if not line or line.startswith("#") or "\t" not in line:
                continue
            old, new = line.split("\t")[:2]
            old = os.path.normpath(os.path.join(base, old.strip()))
            new = os.path.normpath(os.path.join(base, new.strip()))
            (dirs if os.path.isdir(new) else files)[old] = new
    # collapse chains: a -> b (round 1) then b -> c (round 2) becomes a -> c
    for table in (files, dirs):
        for old in list(table):
            seen, cur = {old}, table[old]
            while cur in table and cur not in seen:
                seen.add(cur); cur = table[cur]
            table[old] = cur
    return files, dirs

def remap(abs_target, files, dirs):
    if abs_target in files:
        return files[abs_target]
    for old_dir, new_dir in dirs.items():
        if abs_target == old_dir or abs_target.startswith(old_dir + os.sep):
            return new_dir + abs_target[len(old_dir):]
    return None

def main():
    apply, specs, prefix, args = False, [], None, sys.argv[1:]
    while args:
        a = args.pop(0)
        if a == "--apply":
            apply = True
        elif a == "--prefix":
            prefix = args.pop(0)
        else:
            specs.append((a, prefix))
            prefix = None
    files, dirs = load_moves(specs)
    changed, archived_hits = 0, []
    for md in tracked_md():
        try:
            text = open(md, encoding="utf-8").read()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        base = os.path.dirname(md)
        edits = []
        def sub(m):
            target = m.group(2)
            if re.match(r'^[a-z]+:', target) or target.startswith("#"):
                return m.group(0)
            path, frag = (target.split("#", 1) + [""])[:2]
            abs_t = os.path.normpath(os.path.join(base, path))
            new_abs = remap(abs_t, files, dirs)
            if not new_abs or not os.path.exists(new_abs):
                return m.group(0)
            if "/archive/" in new_abs + os.sep:
                # archived target: links to it must be removed by hand, never redirected
                archived_hits.append((os.path.relpath(md, ROOT), target))
                return m.group(0)
            new_rel = os.path.relpath(new_abs, base)
            if frag:
                new_rel += "#" + frag
            edits.append((target, new_rel))
            return m.group(1) + new_rel + (m.group(3) or "") + m.group(4)
        # rewrite outside fenced code blocks only
        parts, in_fence, out = text.split("\n"), False, []
        for line in parts:
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                out.append(line)
            else:
                out.append(line if in_fence else LINK.sub(sub, line))
        new_text = "\n".join(out)
        if edits:
            changed += 1
            rel = os.path.relpath(md, ROOT)
            print(f"{rel}: {len(edits)}")
            for a, b in edits[:3]:
                print(f"    {a} -> {b}")
            if apply:
                open(md, "w", encoding="utf-8").write(new_text)
    print(f"files changed: {changed} ({'applied' if apply else 'dry-run'})")
    if archived_hits:
        print(f"\nLINKS TO ARCHIVED FILES (remove by hand, do not redirect): {len(archived_hits)}")
        for f, t in archived_hits:
            print(f"  {f}: {t}")

if __name__ == "__main__":
    main()
