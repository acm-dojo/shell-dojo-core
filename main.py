import json
import os
from pathlib import Path
import sys
import signal
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import termios
import tty
import select
import importlib.util
from typing import cast, Callable, Optional, Dict, Any
from utils.pages import Page
import utils.pages as pages_mod

ANSI_HIDE_CURSOR = "\033[?25l"
ANSI_SHOW_CURSOR = "\033[?25h"


def _read_keys_no_echo(
    stop_on_enter: bool = True,
    *,
    resize_flag: Optional[Dict[str, Any]] = None,
    on_resize: Optional[Callable[[], None]] = None,
    poll_interval: float = 0.15,
):
    """Read keys in raw/cbreak mode without echo; yield key (or escape sequence) strings.

    Enhancements:
      * Robust escape sequence parsing with short timeout to capture variable-length CSI sequences
      * Does not block indefinitely if user presses bare ESC
      * Periodically polls (``poll_interval``) so that external events (e.g., terminal resize)
        can trigger a re-render via a shared ``resize_flag`` dict and ``on_resize`` callback.

    Parameters:
        stop_on_enter: If True, stop iteration upon Enter (used for paused screens)
        resize_flag: Mutable dict containing a boolean-like ``pending`` key when a resize occurred
        on_resize: Callback invoked (coalesced) when resize_flag["pending"] is truthy
        poll_interval: Seconds for select() timeout enabling responsive resize redraws
    """
    if not sys.stdin.isatty():
        return
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        # cbreak gives immediate char delivery but retains ISIG so Ctrl-C still works
        tty.setcbreak(fd)
        while True:
            # Wait for input or timeout to check resize flag
            try:
                rlist, _, _ = select.select([fd], [], [], poll_interval)
            except InterruptedError:  # pragma: no cover - interrupted by signal
                rlist = []
            if resize_flag and resize_flag.get("pending"):
                resize_flag["pending"] = False
                if on_resize:
                    try:
                        on_resize()
                    except Exception:  # pragma: no cover - defensive
                        pass
            if not rlist:
                continue
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
    resource_path = Path(__file__).parent / "resources" / "shell.ascii"
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


def load_pages(contents_root: Path) -> tuple[list[Page], bool]:
    """Discover export.py modules under contents and collect their pages.

    Returns (pages, any_show_splash_flag)
    """
    pages: list[Page] = []
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
        _module_name = getattr(mod, "__module_name__", export_file.parent.name)
        show_splash_any = show_splash_any or bool(getattr(mod, "__show_splash__", False))
        raw_pages = getattr(mod, "__pages__", [])
        if not isinstance(raw_pages, list):
            continue
        for idx, p in enumerate(raw_pages):
            if not p:
                continue
            # New protocol: object with a callable .render(width,height)
            if hasattr(p, "render") and callable(getattr(p, "render")):
                pages.append(cast(Page, p))
                global_index += 1
                continue
            if isinstance(p, dict) and "__markdown__" in p:  # legacy dict form
                md_src = str(p["__markdown__"]).rstrip("\n")
                pages.append(pages_mod.markdown_page(md_src))
                global_index += 1
                continue
            if isinstance(p, list):  # legacy list-of-lines
                safe_lines = [str(line) for line in p]
                pages.append(pages_mod.lines_page(safe_lines))
                global_index += 1
    return pages, show_splash_any


def _wrap_and_print(console: Console, renderable, *, border_style: str = "yellow") -> None:
    console.clear()
    panel = Panel(renderable, border_style=border_style, expand=True, padding=(0, 2))
    console.print(panel)


def interactive_page_loop(console: Console, pages: list[Page]) -> None:
    if not pages:
        console.print("[red]No content pages found.[/red]")
        return

    current = 0
    total = len(pages)

    def render_current():
        os.system('cls' if os.name == 'nt' else 'clear')
        size = console.size
        # Leave last row for raw-key input, subtract panel borders (2) and padding (0 vertically)
        inner_height = max(size.height - 1 - 2, 0)
        inner_width = max(size.width - 6, 10)  # borders (2) + padding (4)
        page = pages[current]
        try:
            renderable = page.render(inner_width, inner_height)
        except Exception as e:  # pragma: no cover - prevent crash on faulty page
            renderable = Text(f"[red]Error rendering page: {e}[/red]")
        _wrap_and_print(console, renderable)

    # --- Resize handling (SIGWINCH) ---
    resize_state: Dict[str, Any] = {"pending": False}

    def _sigwinch_handler(signum, frame):  # pragma: no cover - signal-driven
        resize_state["pending"] = True

    previous_handler = None
    try:
        previous_handler = signal.getsignal(signal.SIGWINCH)
        signal.signal(signal.SIGWINCH, _sigwinch_handler)
    except Exception:  # pragma: no cover - platform without SIGWINCH
        resize_state = {}

    render_current()

    try:
        for key in _read_keys_no_echo(
            stop_on_enter=False,
            resize_flag=resize_state,
            on_resize=render_current,
            poll_interval=0.12,
        ):
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
    finally:
        if previous_handler is not None:  # restore previous handler
            try:  # pragma: no cover - best effort restore
                signal.signal(signal.SIGWINCH, previous_handler)  # type: ignore[arg-type]
            except Exception:
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
