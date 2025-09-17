"""Content export for level M0P0: intro/intro

Each builder returns a list[str] of Rich markup lines. The main engine will
center these lines automatically using render_page().
"""

from pathlib import Path
from utils.pages import (
    lines_page,
    markdown_file,
)

__module_name__ = "Why Shell?"
__show_splash__ = True


def build_keybinding_page():
    mapping = {
        "←": "Navigate previous page",
        "→": "Navigate next page",
        "Ctrl+C": "Exit tutorial",
    }
    lines = [
        "[bold white] Key Bindings [/bold white]",
        ""
    ]
    pad_pre_len = max(len(key) for key in mapping.keys()) + 2
    pad_post_len = max(len(description) for description in mapping.values()) + 2
    for key, description in mapping.items():
        pad_pre = ' ' * (pad_pre_len - len(key))
        pad_post = ' ' * (pad_post_len - len(description))
        lines.append(f"{pad_pre}[yellow]{key}[/yellow] {description}{pad_post}")
    
    lines.extend([
        "",
        "[dim]Use → to navigate to the next screen[/dim]"
    ])
    return lines_page(lines)


def build_title_screen():
    return lines_page(["[bold yellow]Why Shell?[/bold yellow]"])


_intro_md = Path(__file__).parent / "intro.md"
intro_pages = markdown_file(_intro_md, padding=6) if _intro_md.exists() else []


__pages__ = [
    build_keybinding_page(),
    build_title_screen(),
    *intro_pages,
]
