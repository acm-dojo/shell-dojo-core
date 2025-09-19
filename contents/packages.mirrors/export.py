"""
Each builder returns a list[str] of Rich markup lines. The main engine will
center these lines automatically using render_page().
"""

from pathlib import Path
from utils.pages import (
    lines_page,
    markdown_file,
)

__module_name__ = "Mirror Magic"
__show_splash__ = False

def build_title_screen():
    return lines_page([f"[bold yellow]{__module_name__}[/bold yellow]"])


_main_md = Path(__file__).parent / "main.md"
main_pages = markdown_file(_main_md, padding=6) if _main_md.exists() else []

__pages__ = [
    build_title_screen(),
    *main_pages,
]
