#!/usr/bin/env python3
"""核對 WAIT_USER.md hub 表的 open 計數與各子檔實際 open 條目（唯讀）。

判準出處：`wait-user/README.md`，本模組不自行發明規則。

- README「## 規則」：`WAIT_USER.md` 是 hub、**只放計數表**，各類 open 項的內容在
  `wait-user/` 子檔；hub 的計數變動敘述寫進 `hub-notes-closed.json`。
  → 所以 hub 那欄只能拿來跟子檔實數比對，hub 本身不是真相來源。
- README「## 規則」：「判定已完成的項目從 md 移到同名 `*-closed.json`……**不直接刪掉**」，
  而 README「## 子檔」表把 feature-runtime 的已完成項記為「檔內『已完成（封存）』節」。
  → 子檔裡標題含「封存」的那一節（及其後所有內容）一律**不計入 open**；
    其餘同層標題每個算一條 open 條目。見 ARCHIVE_MARKERS。
- 子檔的版面是「`#` 檔名標題 + 每條 open 項一個 `##` 標題」，
  也就是**條目標題比它的容器標題深一層**。本模組把這點抽象成 ITEM_LEVEL_OFFSET：
  - 子檔：容器＝`#`（level 1），條目＝level 2。
  - hub 自指列（`[本檔下節](#push-排程)`）：容器＝hub 自己的 `## Push 排程`（level 2），
    條目＝level 3。目前該節是一段敘述、零條目，所以 actual=0，與 hub 的 0 相符。

用法：

    python3 tools/waituser_count.py [--root PATH] [--check] [--json]

每個類別印一行 `<類別> hub=<N> actual=<M> <OK|MISMATCH>`。
`--check` 時只要有任一 MISMATCH 就 exit 1；任何解析/缺檔錯誤一律 exit 2。
`--fix` 本輪不實作（wu-stale 線正在改 wait-user/，本工具唯讀避讓）。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import NamedTuple, Sequence, TextIO

from waituser.parsing import (  # noqa: F401  （re-export：測試與外部呼叫沿用舊名）
    ARCHIVE_MARKERS, HUB_RELPATH, HUB_TABLE_HEADER_KEY, ITEM_LEVEL_OFFSET,
    CountError, Heading, Row, count_open_items, is_archive_title, iter_headings,
    parse_hub_table, slugify, _count_self_section, _count_subfile, _split_row,
)


class Result(NamedTuple):
    category: str
    hub_count: int
    actual: int | None
    status: str          # OK / MISMATCH / ERROR
    source: str          # 子檔相對路徑，或 hub 自指節的錨點
    self_reference: bool
    error: str | None

    def render(self) -> str:
        if self.status == "ERROR":
            return f"{self.category} hub={self.hub_count} actual=- ERROR: {self.error}"
        return f"{self.category} hub={self.hub_count} actual={self.actual} {self.status}"


def evaluate(root: Path) -> list[Result]:
    hub_path = root / HUB_RELPATH
    if not hub_path.is_file():
        raise CountError(f"找不到 hub：{hub_path}")
    hub_text = hub_path.read_text(encoding="utf-8")

    results: list[Result] = []
    for row in parse_hub_table(hub_text):
        self_ref = row.target.startswith("#")
        source = row.target.strip("`")
        try:
            if self_ref:
                actual, title = _count_self_section(hub_text, row.target)
                source = f"{HUB_RELPATH}#{slugify(title)}"
            else:
                sub_path = (hub_path.parent / source).resolve()
                if not sub_path.is_file():
                    raise CountError(f"子檔不存在：{sub_path}")
                actual = _count_subfile(sub_path)
        except CountError as exc:
            results.append(
                Result(row.category, row.hub_count, None, "ERROR", source, self_ref, str(exc))
            )
            continue
        status = "OK" if actual == row.hub_count else "MISMATCH"
        results.append(
            Result(row.category, row.hub_count, actual, status, source, self_ref, None)
        )
    return results


def _default_root() -> Path:
    return Path(__file__).resolve().parent.parent


def main(
    argv: Sequence[str] | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    parser = argparse.ArgumentParser(
        prog="waituser_count.py",
        description="核對 WAIT_USER.md hub 表的 open 計數與 wait-user/ 子檔實際條目（唯讀）。",
    )
    parser.add_argument("--root", type=Path, default=_default_root(), help="覆蓋 repo 根（測試用）")
    parser.add_argument("--check", action="store_true", help="有任一 MISMATCH 時 exit 1")
    parser.add_argument("--json", action="store_true", dest="as_json", help="結構化輸出")
    parser.add_argument("--fix", action="store_true", help="本輪未實作")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.fix:
        print(
            "--fix 未實作，見 agentctl/handoffs/home-2026-10-23/improve/PROPOSAL.md P1-1"
            "（wu-stale 線正在改 wait-user/，本工具唯讀避讓）",
            file=err,
        )
        return 2

    try:
        results = evaluate(Path(args.root))
    except CountError as exc:
        print(f"ERROR: {exc}", file=err)
        return 2

    errors = sum(1 for r in results if r.status == "ERROR")
    mismatches = sum(1 for r in results if r.status == "MISMATCH")
    if errors:
        exit_code = 2
    elif mismatches and args.check:
        exit_code = 1
    else:
        exit_code = 0

    if args.as_json:
        payload = {
            "root": str(Path(args.root)),
            "hub": HUB_RELPATH,
            "rows": [
                {
                    "category": r.category,
                    "hub": r.hub_count,
                    "actual": r.actual,
                    "status": r.status,
                    "source": r.source,
                    "self_reference": r.self_reference,
                    "error": r.error,
                }
                for r in results
            ],
            "mismatches": mismatches,
            "errors": errors,
            "exit_code": exit_code,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2), file=out)
    else:
        for result in results:
            print(result.render(), file=err if result.status == "ERROR" else out)

    return exit_code


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
