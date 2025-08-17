from __future__ import annotations
from pathlib import Path
from typing import List

SPLIT_TOKEN = "---"


def load_markdown_pages(md_path: Path) -> List[list[str]]:
    """Load a markdown file and split into page line lists by SPLIT_TOKEN lines.

    Blank lines are preserved. The splitter line itself is removed.
    Each returned page is a list of markup-ready strings (we allow Rich markup inside).
    """
    text = md_path.read_text(encoding="utf-8")
    # Normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    raw_pages = []
    current: list[str] = []
    for raw_line in text.split("\n"):
        if raw_line.strip() == SPLIT_TOKEN:
            # Flush current page
            raw_pages.append(current)
            current = []
            continue
        current.append(raw_line)
    raw_pages.append(current)  # last page

    # Strip leading/trailing blank lines per page for cleaner centering
    pages: List[list[str]] = []
    for page in raw_pages:
        # remove leading blanks
        while page and page[0].strip() == "":
            page.pop(0)
        while page and page[-1].strip() == "":
            page.pop()
        pages.append(page)
    return pages

__all__ = ["load_markdown_pages", "SPLIT_TOKEN"]
