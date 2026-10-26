"""waituser_count 的 markdown 解析：標題走訪、hub 計數表、子檔條目計數。

判準與版面假設見 `waituser_count.py` 模組 docstring；本模組只是從那裡拆出的實作。
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Iterator, NamedTuple, Sequence

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
