#!/usr/bin/env python3
"""tabledb_links — 資料檔（wf-table/1）裡連結欄位的抽取與解析。

CLI 入口在 tabledb.py（links / check / open / resolve），這裡只放實作。

規則（見 workflows/common/data-files.md）
  * 連結一律**相對資料檔所在目錄**解析；`#anchor` 解析時去掉。
  * `http(s):`／`mailto:`／`#` 開頭不算連結。
  * 所有欄位都掃 `[label](target)`；**連結欄**（meta `link_columns` ∪ 欄名結尾
    `_path` / `_link`）另外把裸值整個當路徑（該值本身沒有 `](` 時）。
  * 巢狀物件／陣列裡的字串也掃 md 連結，`column` 一律報最上層欄名。
"""
import os
import re

LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
EXT = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.\-]*:|#|<)")


def link_columns(table):
    """該表哪些欄位的裸值要當路徑。"""
    cols = set(table.meta.get("link_columns") or [])
    cols.update(c for c in table.columns
                if c.endswith("_path") or c.endswith("_link"))
    return cols


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _strings(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from _strings(v)


def targets(value, is_link_col=False):
    """一個 cell 裡的連結目標（含 #anchor），照出現順序。"""
    out = []
    for s in _strings(value):
        found = LINK.findall(s)
        out += found
        if is_link_col and s is value and not found:
            out.append(s.strip())
    return [t for t in out if t and not EXT.match(t)]


def entries(table, base=None):
    """每筆每欄的連結：[{index, column, target, resolved, exists}]。"""
    base = base or os.path.dirname(os.path.abspath(table.path))
    lcols = link_columns(table)
    out = []
    for i, row in enumerate(table.rows):
        cols = list(table.columns)
        cols += [c for c in row if c not in cols]
        for col in cols:
            if col not in row:
                continue
            for t in targets(row[col], col in lcols):
                path = t.split("#", 1)[0]
                if not path:
                    continue
                res = os.path.normpath(os.path.join(base, path))
                out.append({"index": i, "column": col, "target": t,
                            "resolved": res, "exists": os.path.exists(res)})
    return out


def broken(table, base=None):
    return [e for e in entries(table, base) if not e["exists"]]


def pick(table, i, col=None):
    """第 i 筆的第一個連結（給了 COL 就限定該欄）；沒有就 None。"""
    es = [e for e in entries(table) if e["index"] == i]
    if col:
        es = [e for e in es if e["column"] == col]
    return es[0] if es else None
