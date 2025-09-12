from __future__ import annotations

from pathlib import Path
from typing import List, Sequence, Protocol

from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text
from rich.console import Group, RenderableType
from rich.markdown import Markdown

from .markdown_pages import load_markdown_pages


class Page(Protocol):
    """A renderable page. Implementations decide layout/content entirely.

    Contract:
      - render(width, height) returns a Rich renderable for the given inner area
        (i.e., excluding any outer border/padding which the engine manages).
    """

    def render(self, width: int, height: int) -> RenderableType:  # pragma: no cover - protocol
        ...


class LinesPage:
    """Simple page that centers provided markup lines vertically and horizontally."""

    def __init__(self, lines: Sequence[str]):
        self._lines = [str(line) for line in lines]

    def render(self, width: int, height: int) -> RenderableType:
        # Horizontal center by padding with spaces; vertical center by blank lines
        text = Text()
        inner_width = max(width, 1)
        # Post-process tokens then build Text
        processed_src_lines = [_replace_flag_tag(line) for line in self._lines]
        content_lines: List[Text] = [Text.from_markup(line) if line else Text("") for line in processed_src_lines]

        # compute vertical padding
        content_h = len(content_lines)
        avail = max(height, 0)
        if content_h < avail:
            top_pad = (avail - content_h) // 2
            bottom_pad = avail - content_h - top_pad
            content_lines = [Text("") for _ in range(top_pad)] + content_lines + [Text("") for _ in range(bottom_pad)]

        for i, t in enumerate(content_lines):
            cell_len = t.cell_len
            if cell_len > inner_width:
                t = Text(t.plain[:inner_width])
                cell_len = inner_width
            left = (inner_width - cell_len) // 2 if inner_width > cell_len else 0
            right = inner_width - cell_len - left if inner_width > cell_len else 0
            text.append(Text(" " * left) + t + Text(" " * right))
            if i != len(content_lines) - 1:
                text.append("\n")
        return text


def _insert_space_after_punctuation(text: str) -> str:
    # Mirrors the engine's previous behavior; safe around code/links/urls
    def process_segment(seg: str) -> str:
        if not seg:
            return seg
        out: list[str] = []
        i = 0
        L = len(seg)
        while i < L:
            ch = seg[i]
            if ch == '!' and i + 1 < L and seg[i + 1] == '[':
                out.append(ch)
                i += 1
                continue
            if ch in ",.:;!?)]}\uff0c\u3002":
                nxt = seg[i + 1] if i + 1 < L else ""
                if ch == ']' and nxt == '(':
                    out.append(ch)
                    i += 1
                    continue
                if not nxt or nxt.isspace():
                    out.append(ch)
                    i += 1
                    continue
                prev = seg[i - 1] if i - 1 >= 0 else ""
                if ch == '.':
                    if prev.isalnum() and nxt.isalnum():
                        out.append(ch)
                        i += 1
                        continue
                if ch == ':':
                    j = i - 1
                    while j >= 0 and (seg[j].isalnum() or seg[j] in ['+', '-', '.']):
                        j -= 1
                    scheme = seg[j + 1:i]
                    if scheme in ("http", "https", "ftp") and nxt == '/':
                        out.append(ch)
                        i += 1
                        continue
                out.append(ch)
                out.append(' ')
                i += 1
                continue
            out.append(ch)
            i += 1
        return "".join(out)

    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out_lines: list[str] = []
    in_fence = False
    fence_ticks = ""
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            if not in_fence:
                in_fence = True
                fence_ticks = stripped[:3]
            else:
                if stripped.startswith(fence_ticks):
                    in_fence = False
                    fence_ticks = ""
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        # inline code
        i = 0
        L = len(line)
        rebuilt: list[str] = []
        while i < L:
            if line[i] == '`':
                start = i
                n = 1
                i += 1
                while i < L and line[i] == '`':
                    n += 1
                    i += 1
                close = line.find('`' * n, i)
                if close == -1:
                    rebuilt.append(process_segment(line[start:]))
                    i = L
                    break
                rebuilt.append(line[start:close + n])
                i = close + n
            else:
                next_bt = line.find('`', i)
                chunk = line[i:] if next_bt == -1 else line[i:next_bt]
                rebuilt.append(process_segment(chunk))
                i = L if next_bt == -1 else next_bt
        out_lines.append("".join(rebuilt))
    return "\n".join(out_lines)


class MarkdownPage:
    """Markdown-driven page. Handles its own layout within the given area."""

    def __init__(self, source: str):
        self._src = source.rstrip("\n")

    def render(self, width: int, height: int) -> RenderableType:
        # Apply token replacement first, then spacing normalization
        src = _replace_flag_tag(self._src)
        src = _insert_space_after_punctuation(src)
        md = Markdown(src, code_theme="monokai", hyperlinks=True, justify="left")
        # Render to lines, then apply vertical centering to mimic previous behavior
        from rich.console import Console
        console = Console(width=width, record=True)
        seg_lines = console.render_lines(md, console.options.update(width=max(width, 1)))
        # Stitch lines back into Text
        out_lines: List[Text] = []
        for segs in seg_lines:
            t = Text()
            for seg in segs:
                t.append(seg.text, seg.style)
            out_lines.append(t)
        content_h = len(out_lines)
        avail = max(height, 0)
        if content_h < avail:
            top = (avail - content_h) // 2
            bottom = avail - content_h - top
            out_lines = [Text("") for _ in range(top)] + out_lines + [Text("") for _ in range(bottom)]
        return Group(*out_lines)


class CompositePage:
    def __init__(self, *blocks: RenderableType, center_vertically: bool = True):
        self._blocks = list(blocks)
        self._center = center_vertically

    def render(self, width: int, height: int) -> RenderableType:
        # We rely on the outer Console sizing for width wrapping; just Group blocks
        group = Group(*self._blocks)
        if not self._center:
            return group
        # Vertically center by measuring rendered lines
        from rich.console import Console
        console = Console(width=width, record=True)
        lines = console.render_lines(group, console.options.update(width=max(width, 1)))
        content_h = len(lines)
        avail = max(height, 0)
        if content_h >= avail:
            return group
        top = (avail - content_h) // 2
        bottom = avail - content_h - top
        blanks_top = [Text("") for _ in range(top)]
        blanks_bottom = [Text("") for _ in range(bottom)]
        return Group(*blanks_top, group, *blanks_bottom)


def lines_page(lines: Sequence[str], *, padding: int | None = None, title: str | None = None) -> Page:
    # padding/title ignored under new protocol; kept for backward compatibility
    return LinesPage(lines)


def markdown_page(markdown: str, *, padding: int | None = None, title: str | None = None) -> Page:
    # padding/title ignored
    return MarkdownPage(markdown)


def markdown_file(path: Path, *, padding: int | None = None, title: str | None = None) -> List[Page]:
    # padding/title ignored
    return [MarkdownPage("\n".join(lines)) for lines in load_markdown_pages(path)]


def syntax_block(code: str, language: str = "bash") -> RenderableType:
    return Syntax(code, language, theme="monokai", word_wrap=True)


def prompt_block(text: str) -> RenderableType:
    return Panel(Text(text), title="Prompt", border_style="cyan", padding=(0, 1))


def composite_page(*blocks: RenderableType, center_vertically: bool = True, padding: int | None = None, title: str | None = None) -> Page:
    # padding/title ignored
    return CompositePage(*blocks, center_vertically=center_vertically)


__all__ = [
    "Page",
    "lines_page",
    "markdown_page",
    "markdown_file",
    "syntax_block",
    "prompt_block",
    "composite_page",
    "LinesPage",
    "MarkdownPage",
    "CompositePage",
]

_FLAG_VALUE: str | None = None


def _read_flag_value() -> str | None:
    global _FLAG_VALUE
    if _FLAG_VALUE is not None:
        return _FLAG_VALUE
    try:
        flag_path = Path("/flag")
        if flag_path.exists():
            # Read and strip; keep single-line typical flag formats intact
            value = flag_path.read_text(encoding="utf-8").strip()
            _FLAG_VALUE = value
            return value
    except Exception as e:
        # Raise instead for debugging
        raise e
    _FLAG_VALUE = None
    return None


def _replace_flag_tag(text: str) -> str:
    if "[flag]" not in text:
        return text
    val = _read_flag_value()
    if not val:
        return text
    return text.replace("[flag]", val)
