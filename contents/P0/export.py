"""Content export for level P0.

Each builder returns a list[str] of Rich markup lines. The main engine will
center these lines automatically using render_page().
"""

from pathlib import Path
from utils.markdown_pages import load_markdown_pages

__module_name__ = "Why Shell?"
__show_splash__ = True


def build_keybinding_page() -> list[str]:
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
    return lines


def build_title_screen() -> list[str]:
    return [
        "[bold yellow]Why Shell?[/bold yellow]"
    ]


_intro_md = Path(__file__).parent / "intro.md"
intro_pages_raw = load_markdown_pages(_intro_md) if _intro_md.exists() else []

# Convert list-of-lines pages into markdown string entries so core can render with Rich Markdown
intro_pages = [{"__markdown__": "\n".join(page), "padding": 6} for page in intro_pages_raw]

__pages__ = [
    build_keybinding_page(),
    build_title_screen(),
    *intro_pages,
]
