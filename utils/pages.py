from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Sequence, Union

from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text
from rich.console import Group, RenderableType

from .markdown_pages import load_markdown_pages

PageKind = Literal["lines", "markdown", "composite"]


@dataclass(slots=True)
class PageData:
    kind: PageKind
    content: Union[str, List[str], List[RenderableType]]
    title: str | None = None
    padding: int = 2


def lines_page(lines: Sequence[str], *, padding: int = 2, title: str | None = None) -> PageData:
    return PageData("lines", [str(line) for line in lines], title=title, padding=padding)


def markdown_page(markdown: str, *, padding: int = 2, title: str | None = None) -> PageData:
    return PageData("markdown", markdown.rstrip("\n"), title=title, padding=padding)


def markdown_file(path: Path, *, padding: int = 2, title: str | None = None) -> List[PageData]:
    pages = []
    for page_lines in load_markdown_pages(path):
        pages.append(markdown_page("\n".join(page_lines), padding=padding, title=title))
    return pages


def syntax_block(code: str, language: str = "bash") -> RenderableType:
    return Syntax(code, language, theme="monokai", word_wrap=True)


def prompt_block(text: str) -> RenderableType:
    return Panel(Text(text), title="Prompt", border_style="cyan", padding=(0, 1))


def composite_page(*blocks: RenderableType, padding: int = 2, title: str | None = None) -> PageData:
    flat: List[RenderableType] = []
    for b in blocks:
        if isinstance(b, Group):  # pragma: no cover
            flat.extend(b.renderables)
        else:
            flat.append(b)
    return PageData("composite", flat, title=title, padding=padding)


__all__ = [
    "PageData",
    "lines_page",
    "markdown_page",
    "markdown_file",
    "syntax_block",
    "prompt_block",
    "composite_page",
]
