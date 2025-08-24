import json
import os
from pathlib import Path
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
import re
import termios
import tty
import select
import importlib.util
from typing import List, Iterable, Sequence, cast
from utils.pages import PageData

ANSI_HIDE_CURSOR = "\033[?25l"
ANSI_SHOW_CURSOR = "\033[?25h"


def _read_keys_no_echo(stop_on_enter: bool = True):
    """Read keys in raw/cbreak mode without echo; yield key (or escape sequence) strings.

    Improvements over previous version:
      * Robust escape sequence parsing with short timeout to capture variable-length CSI sequences
      * Does not block indefinitely if user presses bare ESC
      * Uses select() to avoid over-reading which previously could desync rendering
    """
    if not sys.stdin.isatty():
        return
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        # cbreak gives immediate char delivery but retains ISIG so Ctrl-C still works
        tty.setcbreak(fd)
        while True:
            # Block until at least one byte
            select.select([fd], [], [])
            ch = os.read(fd, 1).decode(errors="ignore")
            if not ch:
                continue
            if ch == "\x03":  # Ctrl-C
                raise KeyboardInterrupt
            if ch in ("\r", "\n"):
                if stop_on_enter:
                    break
                yield "\n"
                continue
            if ch == "\x1b":  # start of escape sequence
                seq = ch
                # Collect remainder with tiny timeout windows
                while True:
                    r, _, _ = select.select([fd], [], [], 0.001)
                    if not r:
                        break
                    nxt = os.read(fd, 1).decode(errors="ignore")
                    if not nxt:
                        break
                    seq += nxt
                    # Heuristic: end when final char is alphabetic or tilde (typical CSI terminators)
                    if nxt.isalpha() or nxt == "~":
                        break
                yield seq
                continue
            yield ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def render_page(
    console: Console,
    lines: list[str],
    *,
    pause: bool = True,
    border_style: str = "yellow",
    clear: bool = True,
) -> None:
    """Render a *page* composed of provided markup lines centered in the terminal.

    Parameters:
        console: rich Console instance to render to.
        lines: List of markup strings (one per visual line) forming the body.
        pause: If True and stdin is a TTY, wait for Enter before returning.
        border_style: Rich style for the surrounding panel border.
        clear: Clear the screen first when True.
    """
    if clear:
        console.clear()

    # Clone so we never mutate caller-provided list
    content_lines = list(lines)

    size = console.size
    term_height = size.height - 1  # leave last row free for input (raw key reading)
    target_content_lines = max(term_height - 2, 0)
    cur = len(content_lines)
    if cur < target_content_lines:
        remaining = target_content_lines - cur
        top_pad = remaining // 2
        bottom_pad = remaining - top_pad
        content_lines = ([""] * top_pad) + content_lines + ([""] * bottom_pad)
    elif cur > target_content_lines:
        content_lines = content_lines[:target_content_lines]

    # Compute inner width once (panel width will be console width). Borders add 2 chars; padding=(0,2) adds 4.
    inner_width = max(size.width - 6, 10)
    panel_contents = Text()
    for idx, line in enumerate(content_lines):
        t = Text.from_markup(line) if line else Text("")
        cell_len = t.cell_len
        if cell_len > inner_width:
            t = Text(t.plain[:inner_width])
            cell_len = inner_width
        pad_total = inner_width - cell_len
        left = pad_total // 2
        right = pad_total - left
        line_render = Text(" " * left) + t + Text(" " * right)
        panel_contents.append(line_render)
        if idx != len(content_lines) - 1:
            panel_contents.append("\n")

    panel = Panel(panel_contents, border_style=border_style, expand=True, padding=(0, 2))
    console.print(panel)

    if pause and sys.stdin.isatty():
        try:
            for key in _read_keys_no_echo(stop_on_enter=True):
                # Ignore lateral arrow keys so user can wiggle without advancing
                if key in ("\x1b[D", "\x1b[C"):
                    continue
        except (EOFError, KeyboardInterrupt):
            pass


def show_splash(console: Console, *, pause: bool = True) -> None:
    """Display the splash screen using the generic page renderer."""
    resource_path = Path(__file__).parent / "resources" / "shell.ascaii"
    try:
        ascii_art = resource_path.read_text(encoding="utf-8")
    except OSError as e:
        console.print(f"[red]Failed to load splash screen ({e}).[/red]")
        return

    art_lines = [f"[bold]{line}[/bold]" for line in ascii_art.rstrip("\n").splitlines()]

    if pause and sys.stdin.isatty():
        art_lines.extend([
            "   [yellow bold]A crash course to Linux Shells and CLI tools [blink]█[/blink][/yellow bold]",
            "",
            "[dim]> Press [/dim][underline]Enter[/underline][dim] to continue...[/dim]",
        ])

    render_page(console, art_lines, pause=pause, clear=True)


def _import_module_from_path(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
        return module
    raise ImportError(f"Cannot import module from {path}")


def load_pages(contents_root: Path) -> tuple[list[PageData], bool]:
    """Discover export.py modules under contents and collect their pages.

    Returns (pages, any_show_splash_flag)
    """
    pages: list[PageData] = []
    show_splash_any = False
    global_index = 0
    if not contents_root.exists():
        return pages, show_splash_any
    export_files = set()
    export_files.update(contents_root.glob("export.py"))
    export_files.update(contents_root.glob("*/export.py"))  # nested version
    for export_file in sorted(export_files):
        try:
            mod = _import_module_from_path(export_file)
        except Exception as e:  # pragma: no cover - best effort
            print(f"Failed to import {export_file}: {e}", file=sys.stderr)
            continue
        module_name = getattr(mod, "__module_name__", export_file.parent.name)
        show_splash_any = show_splash_any or bool(getattr(mod, "__show_splash__", False))
        raw_pages = getattr(mod, "__pages__", [])
        if not isinstance(raw_pages, list):
            continue
        for idx, p in enumerate(raw_pages):
            if not p:
                continue
            if isinstance(p, PageData):
                pages.append(p)
                global_index += 1
                continue
            if isinstance(p, dict) and "__markdown__" in p:  # legacy dict form
                md_src = str(p["__markdown__"]).rstrip("\n")
                side_padding = int(p.get("padding", 2)) if str(p.get("padding", "")).isdigit() else 2
                pages.append(PageData("markdown", md_src, padding=side_padding, title=module_name))
                global_index += 1
                continue
            if isinstance(p, list):  # legacy list-of-lines
                safe_lines = [str(line) for line in p]
                pages.append(PageData("lines", safe_lines, title=module_name))
                global_index += 1
    return pages, show_splash_any


def _render_markdown_page(console: Console, md_src: str, *, side_padding: int = 2, border_style: str = "yellow") -> None:
    """Render a markdown page centered vertically within the panel.

    Enhancement: allows embedding Rich markup tags (e.g. [yellow]text[/yellow]) directly
    inside the markdown source. Rich's Markdown renderer does not interpret its own
    markup language within markdown blocks, so we post-process the rendered lines:
    
    1. Render markdown to segments (for layout & wrapping).
    2. Reconstruct each visual line as Text; if the original source line contained
       Rich markup tags we re-parse that plain text with Text.from_markup, otherwise
       we keep the styles produced by the Markdown renderer.
    3. Apply vertical centering similar to the classic page renderer.

    Limitations: markup inside fenced code blocks will not be interpreted (intentionally),
    and complex nested style overlaps between markdown and markup favor explicit
    markup tags (you *may* lose markdown-emphasis styling inside a tagged region).
    """
    console.clear()
    
    # Preprocess: insert a space after punctuation if missing (outside code blocks/spans)
    def _insert_space_after_punctuation(text: str) -> str:
        # Helper to process a single non-code segment safely
        def process_segment(seg: str) -> str:
            if not seg:
                return seg
            result_chars: list[str] = []
            i = 0
            L = len(seg)
            while i < L:
                ch = seg[i]
                # Skip obvious markdown image syntax: '![' should not become '! ['
                if ch == '!' and i + 1 < L and seg[i + 1] == '[':
                    result_chars.append(ch)
                    i += 1
                    continue
                # Candidate punctuation set
                if ch in ",.:;!?)]}，。":
                    nxt = seg[i + 1] if i + 1 < L else ""
                    # Do not alter markdown link dest opener: "](" should not become "] ("
                    if ch == ']' and nxt == '(':
                        result_chars.append(ch)
                        i += 1
                        continue
                    # Don't insert space if next is whitespace or end
                    if not nxt or nxt.isspace():
                        result_chars.append(ch)
                        i += 1
                        continue
                    prev = seg[i - 1] if i - 1 >= 0 else ""
                    # Special-case '.' to avoid breaking decimals and domains/file.ext
                    if ch == '.':
                        if (prev.isalnum() and nxt.isalnum()):
                            # e.g., example.com or 3.14
                            result_chars.append(ch)
                            i += 1
                            continue
                    # Special-case ':' to avoid breaking schemes like https://
                    if ch == ':':
                        # Look back to previous non-word separator for scheme
                        j = i - 1
                        while j >= 0 and (seg[j].isalnum() or seg[j] in ['+', '-', '.']):
                            j -= 1
                        scheme = seg[j + 1:i]
                        if scheme in ("http", "https", "ftp") and nxt == '/':
                            result_chars.append(ch)
                            i += 1
                            continue
                    # Insert a single space if the next char is not punctuation we intentionally allow to stick
                    result_chars.append(ch)
                    # Avoid adding extra space before closing quotes or similar, keep simple: always add one space
                    result_chars.append(' ')
                    i += 1
                    continue
                # Default: copy
                result_chars.append(ch)
                i += 1
            return "".join(result_chars)

        # Process line by line with code-fence and inline-code awareness
        lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        out_lines: list[str] = []
        in_fence = False
        fence_ticks = ""
        for line in lines:
            stripped = line.lstrip()
            # toggle code fence if encountering starting/ending fence (support ``` or ~~~)
            if stripped.startswith("```") or stripped.startswith("~~~"):
                if not in_fence:
                    in_fence = True
                    fence_ticks = stripped[:3]
                else:
                    # only close if matching fence
                    if stripped.startswith(fence_ticks):
                        in_fence = False
                        fence_ticks = ""
                out_lines.append(line)
                continue
            if in_fence:
                out_lines.append(line)
                continue

            # Handle inline code spans with backticks of any length
            i = 0
            L = len(line)
            rebuilt: list[str] = []
            while i < L:
                if line[i] == '`':
                    # count backticks
                    start = i
                    tick_count = 1
                    i += 1
                    while i < L and line[i] == '`':
                        tick_count += 1
                        i += 1
                    # find closing run of same length
                    end = i
                    close_idx = line.find('`' * tick_count, end)
                    if close_idx == -1:
                        # no closing, treat rest as normal text
                        rebuilt.append(process_segment(line[start:]))
                        i = L
                        break
                    # keep the code span unchanged
                    rebuilt.append(line[start:close_idx + tick_count])
                    i = close_idx + tick_count
                else:
                    # accumulate until next backtick or end
                    next_bt = line.find('`', i)
                    chunk = line[i:] if next_bt == -1 else line[i:next_bt]
                    rebuilt.append(process_segment(chunk))
                    i = L if next_bt == -1 else next_bt
            out_lines.append("".join(rebuilt))
        return "\n".join(out_lines)

    md_src = _insert_space_after_punctuation(md_src)
    size = console.size
    term_height = size.height - 1
    # Detect code fence regions to avoid interpreting markup inside them
    code_fence_pattern = re.compile(r"^```")
    fence_lines: set[int] = set()
    in_fence = False
    # Pre-scan original source to mark fenced lines
    original_lines = md_src.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    for i, line in enumerate(original_lines):
        if code_fence_pattern.match(line.strip()):
            in_fence = not in_fence
            fence_lines.add(i)
        elif in_fence:
            fence_lines.add(i)

    md = Markdown(md_src, code_theme="monokai", hyperlinks=True, justify="left")
    inner_width = max(size.width - (2 + side_padding * 2), 20)
    # Render markdown to measure & get styled segments
    rendered_line_segments = console.render_lines(md, console.options.update(width=inner_width))

    # Pattern to detect presence of Rich markup tags
    markup_tag_pattern = re.compile(r"\[[a-zA-Z][^\]]*?\].*?\[/[a-zA-Z][^\]]*?\]")

    processed_lines: list[Text] = []
    for visual_index, seg_list in enumerate(rendered_line_segments):
        # Combine segments into Text preserving original styles as baseline
        base_text = Text()
        for seg in seg_list:
            base_text.append(seg.text, seg.style)
        # Heuristic: map visual lines back to original source lines (best-effort)
        # If line contains markup tags and it's NOT inside a code fence, reparse it.
        original_line = original_lines[visual_index] if visual_index < len(original_lines) else base_text.plain
        if visual_index < len(original_lines) and visual_index not in fence_lines and markup_tag_pattern.search(original_line):
            # Reparse markup; fallback to base_text on failure
            try:
                base_text = Text.from_markup(base_text.plain)
            except Exception:  # pragma: no cover
                pass
        processed_lines.append(base_text)

    content_h = len(processed_lines)
    avail = max(term_height - 2, 0)
    if content_h < avail:
        top_pad = (avail - content_h) // 2
        bottom_pad = avail - content_h - top_pad
        processed_lines = [Text("") for _ in range(top_pad)] + processed_lines + [Text("") for _ in range(bottom_pad)]

    from rich.console import Group
    body = Group(*processed_lines)
    panel = Panel(body, border_style=border_style, expand=True, padding=(0, side_padding))
    console.print(panel)

def _render_lines_page(console: Console, lines: Sequence[str], *, padding: int = 2, border_style: str = "yellow") -> None:
    render_page(console, list(lines), pause=False, border_style=border_style, clear=True)


def _render_composite_page(console: Console, blocks: Iterable, *, padding: int = 2, border_style: str = "yellow") -> None:
    console.clear()
    from rich.console import Group
    group = Group(*list(blocks))
    size = console.size
    term_height = size.height - 1
    inner_width = max(size.width - (2 + padding * 2), 20)
    lines = console.render_lines(group, console.options.update(width=inner_width))
    content_h = len(lines)
    avail = max(term_height - 2, 0)
    if content_h < avail:
        top_pad = (avail - content_h) // 2
        bottom_pad = avail - content_h - top_pad
        blanks_top = [Text("") for _ in range(top_pad)]
        blanks_bottom = [Text("") for _ in range(bottom_pad)]
        group = Group(*blanks_top, group, *blanks_bottom)
    panel = Panel(group, border_style=border_style, expand=True, padding=(0, padding))
    console.print(panel)


def interactive_page_loop(console: Console, pages: list[PageData]) -> None:
    if not pages:
        console.print("[red]No content pages found.[/red]")
        return

    current = 0
    total = len(pages)

    def render_current():
        os.system('cls' if os.name == 'nt' else 'clear')
        page = pages[current]
        if page.kind == "markdown":
            _render_markdown_page(console, page.content if isinstance(page.content, str) else "", side_padding=page.padding)
        elif page.kind == "lines":
            lines_content = cast(List[str], page.content) if isinstance(page.content, list) else []
            _render_lines_page(console, lines_content, padding=page.padding)
        else:  # composite
            blocks = page.content if isinstance(page.content, list) else []
            _render_composite_page(console, blocks, padding=page.padding)

    render_current()

    try:
        for key in _read_keys_no_echo(stop_on_enter=False):
            if key in ("q", "Q"):
                break
            if key in ("\x1b[D",):  # Left arrow
                if current > 0:
                    current -= 1
                    render_current()
                continue
            if key in ("\x1b[C", "\n", "\r"):  # Right arrow or Enter
                if current < total - 1:
                    current += 1
                    render_current()
                else:
                    break
                continue
            # Ignore all other input silently
    except KeyboardInterrupt:
        pass


def main():
    with open("contents/metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)
    os.system('cls' if os.name == 'nt' else 'clear')
    console = Console()
    hide_cursor = sys.stdout.isatty()
    try:
        if hide_cursor:
            sys.stdout.write(ANSI_HIDE_CURSOR)
            sys.stdout.flush()
        contents_root = Path(__file__).parent / "contents" / f"P{metadata['selected']}"
        pages, any_show_splash = load_pages(contents_root)
        if any_show_splash:
            show_splash(console)
        interactive_page_loop(console, pages)
    finally:
        if hide_cursor:
            sys.stdout.write(ANSI_SHOW_CURSOR)
            sys.stdout.flush()


if __name__ == "__main__":
    main()
