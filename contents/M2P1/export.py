from pathlib import Path
from utils.pages import (
    lines_page,
    markdown_file,
)

__module_name__ = "Shells and Environments"
__show_splash__ = False

def build_title_screen():
    return lines_page([f"[bold yellow]{__module_name__}[/bold yellow]"])

_intro_md = Path(__file__).parent / "main.md"
intro_pages = markdown_file(_intro_md, padding=6) if _intro_md.exists() else []

__pages__ = [build_title_screen()] + intro_pages
