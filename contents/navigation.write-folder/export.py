"""Content export for level P0.

Each builder returns a list[str] of Rich markup lines. The main engine will
center these lines automatically using render_page().
"""

from pathlib import Path
from utils.pages import (
    lines_page,
    markdown_file,
)

__module_name__ = "Changing Folders"
__show_splash__ = False

def build_title_screen():
    return lines_page(["[bold yellow]Changing Folders[/bold yellow]"])


_intro_md = Path(__file__).parent / "main.md"
intro_pages = markdown_file(_intro_md, padding=6) if _intro_md.exists() else []
_recap_md = Path(__file__).parent / "recap.md"
recap_pages = markdown_file(_recap_md, padding=6) if _recap_md.exists() else []
_card_md = Path(__file__).parent / "card.md"
card_pages = markdown_file(_card_md, padding=6) if _card_md.exists() else []


__pages__ = [
    build_title_screen(),
    *intro_pages,
    *recap_pages,
    *card_pages,
]

__card__ = card_pages[0]