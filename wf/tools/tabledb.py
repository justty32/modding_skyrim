#!/usr/bin/env python3
"""tabledb — 同質列表資料檔（.json / .csv）的統一 CRUD 與連結解析。

契約 `wf-table/1`（見 workflows/common/data-files.md）：md 裡每列同一組欄位、
超過 1 KB 的條列式區塊抽成資料檔，md 只留摘要與查法；讀寫都走這支，不整份讀進 context。

檔案格式
  .json  {"contract": "wf-table/1", "source": "<抽出自哪份 md>", "extracted": "YYYY-MM-DD",
          "columns": [...], "link_columns": [...], "rows": [{...}, ...]}
         rows 的值可以是多行字串或巢狀物件；缺的欄位視為空字串。舊檔沒有 contract 也讀得開。
  .csv   第一列是欄位名，其餘每列一筆；值一律字串。只適合扁平、無多行值的表；
         沒地方放 link_columns，改用欄名結尾 _path / _link 表示該欄是連結。

CLI（索引一律 0-based；所有輸出都是 JSON）
  tabledb.py FILE                       契約、列數與欄位
  tabledb.py FILE get I                 第 I 筆
  tabledb.py FILE find k=v [k=v ...]    所有欄位精確相等的筆（含索引）
  tabledb.py FILE grep REGEX            任一欄位符合 REGEX 的筆（含索引，不分大小寫）
  tabledb.py FILE add k=v [k=v ...]     追加一筆（未給的欄位補空字串）
  tabledb.py FILE update I k=v [...]    改第 I 筆的指定欄位
  tabledb.py FILE delete I              刪第 I 筆（之後的索引會前移）
  tabledb.py FILE columns               欄位列表
  tabledb.py FILE --slice A B           第 A 到 B-1 筆
  tabledb.py links FILE                 每筆每欄的連結 [{index, column, target, resolved, exists}]
  tabledb.py check FILE                 同上只印壞的（exists=false）；有壞的結束碼 1
  tabledb.py open FILE I [COL]          {path, content}：該筆連結指向的檔案內容
  tabledb.py resolve FILE I [COL]       同上只印 {index, column, target, resolved, exists}
  （後四個也接受 `tabledb.py FILE links` 這種順序。）

Python
  from tabledb import load
  t = load("x.json"); t.rows; t.columns; t.get(3); t.find(id="31472"); t.add({...}); t.update(3, status="GO"); t.delete(3); t.save()
  連結相關在 tabledb_links：entries(t) / broken(t) / pick(t, i, col) / link_columns(t)
"""
import csv
import json
import os
import re
import sys

import tabledb_links


class Table:
    def __init__(self, path, columns=None, rows=None, meta=None):
        self.path = path
        self.columns = list(columns or [])
        self.rows = list(rows or [])
        self.meta = dict(meta or {})

    # ---- read / write -------------------------------------------------
    @classmethod
    def load(cls, path):
        if path.endswith(".csv"):
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = [dict(r) for r in reader]
                return cls(path, reader.fieldnames or [], rows)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):  # bare list of dicts is tolerated
            data = {"rows": data}
        rows = data.get("rows", [])
        columns = data.get("columns") or (list(rows[0].keys()) if rows else [])
        meta = {k: v for k, v in data.items() if k not in ("rows", "columns")}
        return cls(path, columns, rows, meta)

    def save(self, path=None):
        path = path or self.path
        if path.endswith(".csv"):
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=self.columns, extrasaction="ignore")
                w.writeheader()
                for r in self.rows:
                    w.writerow({c: r.get(c, "") for c in self.columns})
            return
        data = dict(self.meta)
        data["columns"] = self.columns
        data["rows"] = self.rows
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
            f.write("\n")
        os.replace(tmp, path)

    # ---- CRUD ---------------------------------------------------------
    def get(self, i):
        return self.rows[i]

    def find(self, **kv):
        return [r for r in self.rows if all(str(r.get(k, "")) == str(v) for k, v in kv.items())]

    def find_indexed(self, **kv):
        return [(i, r) for i, r in enumerate(self.rows)
                if all(str(r.get(k, "")) == str(v) for k, v in kv.items())]

    def grep(self, pattern):
        rx = re.compile(pattern, re.I)
        return [(i, r) for i, r in enumerate(self.rows)
                if any(rx.search(str(v)) for v in r.values())]

    def add(self, row):
        full = {c: row.get(c, "") for c in self.columns}
        for k in row:
            if k not in self.columns:
                self.columns.append(k)
                full[k] = row[k]
        self.rows.append(full)
        return len(self.rows) - 1

    def update(self, i, **kv):
        for k in kv:
            if k not in self.columns:
                self.columns.append(k)
        self.rows[i].update(kv)
        return self.rows[i]

    def delete(self, i):
        return self.rows.pop(i)

    def __len__(self):
        return len(self.rows)


def load(path):
    return Table.load(path)


LINK_CMDS = ("links", "check", "open", "resolve")


# ---- CLI --------------------------------------------------------------
def _kv(args):
    out = {}
    for a in args:
        if "=" not in a:
            raise SystemExit(f"expected k=v, got {a!r}")
        k, v = a.split("=", 1)
        out[k] = v
    return out


def _emit(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=1))


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] in LINK_CMDS:  # links/check/open/resolve FILE ... 的順序
        if len(argv) < 2:
            raise SystemExit(f"{argv[0]}: missing FILE")
        argv = [argv[1], argv[0]] + argv[2:]
    path, cmd, rest = argv[0], (argv[1] if len(argv) > 1 else None), argv[2:]
    t = Table.load(path)
    if cmd is None:
        _emit({"file": path, "contract": t.meta.get("contract"), "count": len(t),
               "columns": t.columns,
               **{k: v for k, v in t.meta.items() if k != "contract"}})
    elif cmd == "columns":
        _emit(t.columns)
    elif cmd == "get":
        _emit(t.get(int(rest[0])))
    elif cmd == "--slice":
        a, b = int(rest[0]), int(rest[1])
        _emit([{"index": i, **t.rows[i]} for i in range(a, min(b, len(t)))])
    elif cmd == "find":
        _emit([{"index": i, **r} for i, r in t.find_indexed(**_kv(rest))])
    elif cmd == "grep":
        _emit([{"index": i, **r} for i, r in t.grep(rest[0])])
    elif cmd == "add":
        i = t.add(_kv(rest)); t.save(); _emit({"index": i, **t.rows[i]})
    elif cmd == "update":
        r = t.update(int(rest[0]), **_kv(rest[1:])); t.save(); _emit(r)
    elif cmd == "delete":
        r = t.delete(int(rest[0])); t.save(); _emit(r)
    elif cmd == "links":
        _emit(tabledb_links.entries(t))
    elif cmd == "check":
        bad = tabledb_links.broken(t)
        _emit(bad)
        return 1 if bad else 0
    elif cmd in ("open", "resolve"):
        col = rest[1] if len(rest) > 1 else None
        e = tabledb_links.pick(t, int(rest[0]), col)
        if e is None:
            _emit({"error": f"no link in row {rest[0]}"
                            + (f", column {col!r}" if col else "")})
            return 1
        if cmd == "resolve":
            _emit(e)
            return 0
        try:
            with open(e["resolved"], encoding="utf-8") as f:
                _emit({"path": e["resolved"], "content": f.read()})
        except OSError as exc:
            _emit({"error": str(exc)})
            return 1
    else:
        raise SystemExit(f"unknown command {cmd!r}; see --help")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
