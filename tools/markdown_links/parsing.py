"""Parse local links and heading anchors, and validate link targets."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
# Inline code spans are not links (CommonMark: code spans win over links).
CODE_SPAN_RE = re.compile(r"(?<!`)(`+)(?!`).+?(?<!`)\1(?!`)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")
SETEXT_RE = re.compile(r"^\s{0,3}(?:=+|-+)\s*$")
EXPLICIT_ANCHOR_RE = re.compile(
    r"<(?:a|span)\b[^>]*(?:id|name)\s*=\s*['\"]([^'\"]+)['\"][^>]*>",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class LocalTarget:
    display: str
    path: str
    fragment: str | None


def link_target(raw: str) -> LocalTarget | None:
    value = raw.strip()
    if value.startswith("<"):
        closing = value.find(">")
        if closing < 0:
            return LocalTarget(value, value, None)
        value = value[1:closing]
    else:
        value = value.split(maxsplit=1)[0]
    value = unquote(value)
    if not value or value.startswith("//"):
        return None
    parts = urlsplit(value)
    if parts.scheme:
        return None
    if not parts.path and not parts.fragment:
        return None
    return LocalTarget(value, parts.path, parts.fragment or None)


def github_heading_slug(text: str) -> str:
    """Approximate GitHub's rendered-heading slug for local Markdown links."""
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    # Backticks and asterisks need no special case: the ASCII-punctuation rule
    # below drops them like every other ASCII symbol.
    text = unicodedata.normalize("NFKC", text).strip().lower()
    # github-slugger drops every punctuation AND symbol character (so "→", "✅", "+"
    # go too, not just ASCII ones) and keeps letters/marks/numbers.
    text = "".join(
        char
        for char in text
        if (
            unicodedata.category(char)[0] in "LMN"
            or char in "-_"
            or char.isspace()
        )
    )
    # github-slugger replaces EACH space with a "-"; it does NOT collapse runs. A title
    # like "A — B" loses the dash and keeps both spaces, so the real anchor is "a--b".
    return re.sub(r"\s", "-", text)


def markdown_anchors(markdown: Path) -> set[str]:
    anchors: set[str] = set()
    duplicate_counts: dict[str, int] = defaultdict(int)
    fence: str | None = None
    previous_line: str | None = None
    for line in markdown.read_text(encoding="utf-8").splitlines():
        marker = FENCE_RE.match(line)
        if marker:
            current = marker.group(1)[0]
            if fence is None:
                fence = current
            elif fence == current:
                fence = None
            previous_line = None
            continue
        if fence is not None:
            continue
        anchors.update(unquote(anchor) for anchor in EXPLICIT_ANCHOR_RE.findall(line))
        heading = HEADING_RE.match(line)
        if heading:
            text = re.sub(r"\s+#+\s*$", "", heading.group(1))
        elif previous_line and SETEXT_RE.match(line):
            text = previous_line.strip()
        else:
            previous_line = line
            continue
        base = github_heading_slug(text)
        if not base:
            continue
        count = duplicate_counts[base]
        duplicate_counts[base] += 1
        anchors.add(base if count == 0 else f"{base}-{count}")
        previous_line = None
    return anchors


def markdown_links(markdown: Path):
    fence: str | None = None
    for line_number, line in enumerate(
        markdown.read_text(encoding="utf-8").splitlines(), 1
    ):
        marker = FENCE_RE.match(line)
        if marker:
            current = marker.group(1)[0]
            if fence is None:
                fence = current
            elif fence == current:
                fence = None
            continue
        if fence is not None:
            continue
        for match in LINK_RE.finditer(CODE_SPAN_RE.sub("", line)):
            target = link_target(match.group(1))
            if target:
                yield line_number, target


def check_file(source: Path, root: Path) -> tuple[int, list[tuple[int, str, Path, str]]]:
    if source.is_symlink():
        try:
            markdown = source.resolve(strict=True)
        except FileNotFoundError:
            return 0, [(1, str(source.readlink()), source.resolve(), "")]
    else:
        markdown = source.resolve()

    checked = 0
    # Each entry carries the missing fragment, so an anchor failure can name the
    # anchor instead of pointing at a file that plainly does exist.
    broken: list[tuple[int, str, Path, str]] = []
    for line_number, target in markdown_links(markdown):
        checked += 1
        candidate = Path(target.path)
        if candidate.is_absolute():
            resolved = root / target.path.lstrip("/")
        elif not target.path:
            resolved = markdown
        else:
            resolved = markdown.parent / candidate
        resolved = resolved.resolve()
        if not resolved.exists():
            broken.append((line_number, target.display, resolved, ""))
            continue
        if (
            target.fragment
            and resolved.is_file()
            and resolved.suffix.lower() in {".md", ".markdown"}
            and target.fragment not in markdown_anchors(resolved)
        ):
            broken.append((line_number, target.display, resolved, target.fragment))
    return checked, broken


