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
import re
import sys
from typing import Iterator, NamedTuple, Sequence, TextIO

# hub 檔在 repo 根的相對路徑。
HUB_RELPATH = "WAIT_USER.md"

# 子檔中「已完成／已裁示（封存）」節的辨識字串；命中後該層之後都不算 open。
# 出處：wait-user/README.md「## 子檔」表 feature-runtime 列「檔內『已完成（封存）』節」，
# 四個子檔實際用的是「已完成（封存）」「已裁示／已完成（封存）」「已完成／作廢（封存）」。
ARCHIVE_MARKERS = ("封存",)

# 條目標題比容器標題深一層（見模組 docstring）。
ITEM_LEVEL_OFFSET = 1

# hub 表的表頭必須含這個欄名才被當成計數表。
HUB_TABLE_HEADER_KEY = "open"

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_LINK_RE = re.compile(r"\]\(([^)]+)\)")
_SEPARATOR_CELL_RE = re.compile(r"^:?-{2,}:?$")


class Heading(NamedTuple):
    level: int
    title: str
    line: int


class Row(NamedTuple):
    category: str
    hub_count: int
    target: str
    line: int


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


class CountError(Exception):
    """解析或缺檔錯誤；一律導向 exit 2。"""


def iter_headings(text: str) -> Iterator[Heading]:
    """走訪 markdown 標題，跳過 fenced code block 內的假標題。"""
    fence: str | None = None
    for lineno, raw in enumerate(text.splitlines(), start=1):
        fence_hit = _FENCE_RE.match(raw)
        if fence_hit:
            token = fence_hit.group(1)
            if fence is None:
                fence = token
            elif fence == token:
                fence = None
            continue
        if fence is not None:
            continue
        hit = _HEADING_RE.match(raw)
        if hit:
            yield Heading(len(hit.group(1)), hit.group(2), lineno)


def is_archive_title(title: str) -> bool:
    return any(marker in title for marker in ARCHIVE_MARKERS)


def count_open_items(
    headings: Sequence[Heading],
    container_level: int,
    start_index: int,
) -> int:
    """數 start_index 之後、同一個容器底下的 open 條目。

    容器結束於下一個 level <= container_level 的標題；
    條目是 level == container_level + ITEM_LEVEL_OFFSET 的標題；
    命中「封存」標題後停止計數（之後都是已關閉的歷史）。
    """
    item_level = container_level + ITEM_LEVEL_OFFSET
    count = 0
    for heading in headings[start_index:]:
        if heading.level <= container_level:
            break
        if heading.level != item_level:
            continue
        if is_archive_title(heading.title):
            break
        count += 1
    return count


def slugify(title: str) -> str:
    """GitHub 風格錨點：轉小寫、去標點、空白換連字號（CJK 保留）。"""
    slug = title.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug, flags=re.UNICODE)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def _split_row(line: str) -> list[str]:
    cells = line.split("|")
    if cells and not cells[0].strip():
        cells = cells[1:]
    if cells and not cells[-1].strip():
        cells = cells[:-1]
    return [cell.strip() for cell in cells]


def parse_hub_table(text: str) -> list[Row]:
    """抓 hub 的計數表，回傳每個類別一列。"""
    lines = text.splitlines()
    block: list[tuple[int, str]] = []
    blocks: list[list[tuple[int, str]]] = []
    for lineno, raw in enumerate(lines, start=1):
        if raw.lstrip().startswith("|"):
            block.append((lineno, raw))
        elif block:
            blocks.append(block)
            block = []
    if block:
        blocks.append(block)

    for candidate in blocks:
        header = _split_row(candidate[0][1])
        if not any(cell.lower() == HUB_TABLE_HEADER_KEY for cell in header):
            continue
        open_col = next(
            i for i, cell in enumerate(header) if cell.lower() == HUB_TABLE_HEADER_KEY
        )
        list_col = len(header) - 1
        rows: list[Row] = []
        for lineno, raw in candidate[1:]:
            cells = _split_row(raw)
            if all(_SEPARATOR_CELL_RE.match(cell or "-") for cell in cells):
                continue
            if len(cells) != len(header):
                raise CountError(
                    f"{HUB_RELPATH}:{lineno} 表格欄數 {len(cells)} 不等於表頭 {len(header)}"
                )
            try:
                hub_count = int(cells[open_col])
            except ValueError as exc:
                raise CountError(
                    f"{HUB_RELPATH}:{lineno} open 欄不是整數：{cells[open_col]!r}"
                ) from exc
            link = _LINK_RE.search(cells[list_col])
            if not link:
                raise CountError(f"{HUB_RELPATH}:{lineno} 清單欄沒有連結：{cells[list_col]!r}")
            rows.append(Row(cells[0], hub_count, link.group(1).strip(), lineno))
        if not rows:
            raise CountError(f"{HUB_RELPATH} 計數表沒有資料列")
        return rows
    raise CountError(f"{HUB_RELPATH} 找不到含 `{HUB_TABLE_HEADER_KEY}` 欄的計數表")


def _count_self_section(hub_text: str, anchor: str) -> tuple[int, str]:
    """自指列：在 hub 自己的那一節底下數條目。"""
    slug = anchor.lstrip("#")
    headings = list(iter_headings(hub_text))
    for index, heading in enumerate(headings):
        if slugify(heading.title) == slug:
            return count_open_items(headings, heading.level, index + 1), heading.title
    raise CountError(f"{HUB_RELPATH} 找不到錨點 #{slug} 對應的標題")


def _count_subfile(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    headings = list(iter_headings(text))
    if not headings:
        raise CountError(f"{path} 沒有任何標題")
    container = headings[0]
    return count_open_items(headings, container.level, 1)


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
