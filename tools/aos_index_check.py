#!/usr/bin/env python3
"""Check the hand-written _index.json files (aos index_view format) under a root folder of the skyrim workspace.

Usage: python3 tools/aos_index_check.py [ROOT] [--config FILE] [--quiet]
ROOT defaults to the workspace root (the folder above tools/). Paths in the
config are relative to the workspace root.

Errors (exit 1):
  BAD-JSON      file is not valid JSON, or not a JSON object
  BAD-VALUE     an entry value is not an object, or has no non-empty "description"
  BAD-INDEX     an entry's "index" is not a string, or points at a missing file
  MISSING-KEY   a key names something that does not exist on disk
  UNLISTED-DIR  a direct child folder (not hidden, not git-ignored) has no key
                (skipped for folders listed in partial_dirs)
  OVERSIZE      the file is bigger than max_bytes
  FORBIDDEN     an _index.json sits inside a forbidden folder, or outside the workspace
Warnings (exit 0):
  LONG-DESC     description longer than max_description_chars
  NO-LINK       a child folder has its own _index.json but the parent entry has no "index"
  ORPHAN        an _index.json that no parent _index.json links to
  OUTSIDE-GONE  an extra table key (absolute path) does not exist right now
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.dirname(HERE)
INDEX = "_index.json"


def load_config(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def rel(p):
    return os.path.relpath(p, WS)


def inside(path, parent):
    path, parent = os.path.realpath(path), os.path.realpath(parent)
    return path == parent or path.startswith(parent + os.sep)


def ignored_children(folder, names):
    """Return the subset of names (direct children of folder) that git ignores."""
    if not names:
        return set()
    try:
        r = subprocess.run(
            ["git", "-C", folder, "check-ignore", "--stdin"],
            input="\n".join(names) + "\n", capture_output=True, text=True,
        )
    except OSError:
        return set()
    return {line.strip().rstrip("/") for line in r.stdout.splitlines() if line.strip()}


def find_indexes(root, skip):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        if INDEX in filenames:
            found.append(os.path.join(dirpath, INDEX))
    return sorted(found)


def check_table(path, data, cfg, out, keys_are_abs=False):
    folder = os.path.dirname(path)
    links = {}
    if not isinstance(data, dict):
        out.append(("E", "BAD-JSON", rel(path), "top level is not an object"))
        return links
    maxc = cfg.get("max_description_chars", 120)
    for key, val in data.items():
        where = "%s#/%s" % (rel(path), key)
        if not isinstance(val, dict):
            out.append(("E", "BAD-VALUE", where, "value is %s, must be an object" % type(val).__name__))
            continue
        desc = val.get("description")
        if not isinstance(desc, str) or not desc.strip():
            out.append(("E", "BAD-VALUE", where, "missing or empty description"))
        elif len(desc) > maxc:
            out.append(("W", "LONG-DESC", where, "%d chars > %d" % (len(desc), maxc)))
        target = key if keys_are_abs else os.path.join(folder, key)
        if keys_are_abs:
            if not os.path.isabs(key):
                out.append(("E", "MISSING-KEY", where, "key must be an absolute path"))
            elif not os.path.exists(key):
                out.append(("W", "OUTSIDE-GONE", where, "path does not exist now"))
        elif not os.path.lexists(target):
            out.append(("E", "MISSING-KEY", where, "no such file or folder"))
        if "index" in val:
            idx = val["index"]
            if not isinstance(idx, str) or not idx:
                out.append(("E", "BAD-INDEX", where, "index must be a non-empty string"))
            else:
                ipath = idx.split("#", 1)[0]
                ifull = os.path.normpath(os.path.join(folder, ipath))
                if not os.path.isfile(ifull):
                    out.append(("E", "BAD-INDEX", where, "index file not found: %s" % idx))
                else:
                    links[os.path.realpath(ifull)] = key
    return links


def main():
    ap = argparse.ArgumentParser(description="Check _index.json files for index_view.")
    ap.add_argument("root", nargs="?", default=WS)
    ap.add_argument("--config", default=os.path.join(HERE, "aos_index_check.json"))
    ap.add_argument("--quiet", action="store_true", help="print errors and the summary only")
    a = ap.parse_args()
    cfg = load_config(a.config)
    root = os.path.abspath(a.root)
    out = []
    if not inside(root, WS):
        out.append(("E", "FORBIDDEN", root, "root is outside the workspace"))
    forbidden = [os.path.join(WS, d) for d in cfg.get("forbidden_dirs", [])]
    partial = {os.path.realpath(os.path.join(WS, d)) for d in cfg.get("partial_dirs", [])}
    skip = set(cfg.get("skip_walk", []))
    maxb = cfg.get("max_bytes", 8192)

    files = find_indexes(root, skip)
    # forbidden folders are walked even if skip_walk would hide them
    for fd in forbidden:
        if os.path.isdir(fd) and inside(fd, root):
            for p in find_indexes(fd, {".git"}):
                if p not in files:
                    files.append(p)

    linked = {}
    for path in files:
        if any(inside(path, fd) for fd in forbidden):
            out.append(("E", "FORBIDDEN", rel(path), "index not allowed in this folder"))
            continue
        size = os.path.getsize(path)
        if size > maxb:
            out.append(("E", "OVERSIZE", rel(path), "%d bytes > %d" % (size, maxb)))
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (ValueError, OSError) as e:
            out.append(("E", "BAD-JSON", rel(path), str(e).splitlines()[0]))
            continue
        links = check_table(path, data, cfg, out)
        linked.update(links)
        folder = os.path.dirname(path)
        if not isinstance(data, dict):
            continue
        kids = sorted(n for n in os.listdir(folder)
                      if not n.startswith(".") and os.path.isdir(os.path.join(folder, n)))
        ign = ignored_children(folder, kids)
        is_partial = os.path.realpath(folder) in partial
        for n in kids:
            if n in ign:
                continue
            if n not in data and not is_partial:
                out.append(("E", "UNLISTED-DIR", rel(os.path.join(folder, n)), "child folder has no key in %s" % rel(path)))
            child_idx = os.path.join(folder, n, INDEX)
            if n in data and isinstance(data[n], dict) and os.path.isfile(child_idx) and "index" not in data[n]:
                out.append(("W", "NO-LINK", "%s#/%s" % (rel(path), n), "child has %s but entry has no index" % INDEX))

    top = os.path.realpath(os.path.join(root, INDEX))
    for path in files:
        rp = os.path.realpath(path)
        if rp != top and rp not in linked and not any(inside(path, fd) for fd in forbidden):
            out.append(("W", "ORPHAN", rel(path), "no parent index links here"))

    for t in cfg.get("extra_tables", []):
        tp = os.path.join(WS, t)
        if not os.path.isfile(tp) or not inside(tp, root):
            continue
        size = os.path.getsize(tp)
        if size > maxb:
            out.append(("E", "OVERSIZE", rel(tp), "%d bytes > %d" % (size, maxb)))
        try:
            with open(tp, encoding="utf-8") as f:
                data = json.load(f)
        except (ValueError, OSError) as e:
            out.append(("E", "BAD-JSON", rel(tp), str(e).splitlines()[0]))
            continue
        check_table(tp, data, cfg, out, keys_are_abs=True)
        files.append(tp)

    errs = [o for o in out if o[0] == "E"]
    warns = [o for o in out if o[0] == "W"]
    for kind, code, where, msg in out:
        if a.quiet and kind == "W":
            continue
        print("%s %s %s: %s" % ("ERROR" if kind == "E" else "WARN", code, where, msg))
    print("SUMMARY root=%s files=%d errors=%d warnings=%d" % (rel(root), len(files), len(errs), len(warns)))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
