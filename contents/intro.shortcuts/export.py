"""Content export for level M0P0: intro/intro

Each builder returns a list[str] of Rich markup lines. The main engine will
center these lines automatically using render_page().
"""

from pathlib import Path
from utils.pages import (
    lines_page,
    markdown_file,
)

__module_name__ = "Taking a Shortcut"
__show_splash__ = True

def build_title_screen():
    return lines_page(["[bold yellow]Taking a Shortcut[/bold yellow]"])


_intro_md = Path(__file__).parent / "main.md"
intro_pages = markdown_file(_intro_md, padding=6) if _intro_md.exists() else []


__pages__ = [
    build_title_screen(),
    *intro_pages,
]
