#!/usr/bin/env python3
"""find_big_lists — 找出 markdown 裡超過門檻的條列式區塊（表格或清單）。

用法: find_big_lists.py [--min 1024] [--exclude-dir archive ...] <path>...
輸出: 每個超標區塊一行  <bytes>\t<file>:<start>-<end>\t<table|list>\t<rows>
      區塊 = 連續的表格列（以 | 開頭）或連續的清單項（-、*、數字.），空行或其他行即中斷。
      code fence 內的內容不算。導航用的表（README 路由表、派發表）也會被列出——要不要抽由人判斷。
"""
import os
import re
import sys

ROW = re.compile(r"^\s*\|")
ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
CONT = re.compile(r"^\s{2,}\S")  # indented continuation of a list item


def scan(path, min_bytes):
    out = []
    try:
        lines = open(path, encoding="utf-8").read().split("\n")
    except (UnicodeDecodeError, OSError):
        return out
    kind, start, size, rows, fence = None, 0, 0, 0, False

    def flush(end):
        if kind and size >= min_bytes:
            out.append((size, f"{path}:{start + 1}-{end}", kind, rows))

    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            flush(i); kind = None; fence = not fence; continue
        if fence:
            continue
        this = "table" if ROW.match(line) else "list" if ITEM.match(line) else None
        if this is None and kind == "list" and CONT.match(line):
            size += len(line.encode()) + 1; continue
        if this != kind:
            flush(i)
            kind, start, size, rows = this, i, 0, 0
        if this:
            size += len(line.encode()) + 1
            rows += 1
    flush(len(lines))
    return out


def main(argv):
    min_bytes, exclude, paths = 1024, {"archive", ".git", "node_modules"}, []
    it = iter(argv)
    for a in it:
        if a == "--min":
            min_bytes = int(next(it))
        elif a == "--exclude-dir":
            exclude.add(next(it))
        else:
            paths.append(a)
    if not paths:
        print(__doc__); return 0
    hits = []
    for p in paths:
        if os.path.isfile(p):
            hits += scan(p, min_bytes); continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in exclude]
            for f in files:
                if f.endswith(".md"):
                    hits += scan(os.path.join(root, f), min_bytes)
    for size, loc, kind, rows in sorted(hits, reverse=True):
        print(f"{size}\t{loc}\t{kind}\t{rows}")
    print(f"# {len(hits)} block(s) >= {min_bytes} bytes", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
