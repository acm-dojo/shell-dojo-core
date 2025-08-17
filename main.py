import os
from pathlib import Path
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import termios
import tty

ANSI_HIDE_CURSOR = "\033[?25l"
ANSI_SHOW_CURSOR = "\033[?25h"


def _read_keys_no_echo(stop_on_enter: bool = True):
    """Read keys in raw mode without echo; yield sequences. Stops on Enter if requested."""
    if not sys.stdin.isatty():
        return
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch == "\x03":  # Ctrl-C
                raise KeyboardInterrupt
            if ch == "\r" or ch == "\n":
                if stop_on_enter:
                    break
                else:
                    yield ch
                    continue
            if ch == "\x1b":  # possible escape sequence
                seq = ch + sys.stdin.read(1) + sys.stdin.read(1)
                yield seq
            else:
                yield ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def show_splash(console: Console, *, pause: bool = True) -> None:
    """Clear the screen and display the splash ASCII art centered.

    Centers horizontally and vertically based on current terminal size.
    Falls back gracefully if the terminal is smaller than the art.
    """
    console.clear()
    resource_path = Path(__file__).parent / "resources" / "shell.ascaii"
    try:
        ascii_art = resource_path.read_text(encoding="utf-8")
    except OSError as e:
        console.print(f"[red]Failed to load splash screen ({e}).[/red]")
        return

    art_lines = ascii_art.rstrip("\n").splitlines()

    # Build base content with optional instructions
    content_lines = art_lines[:]
    content_lines = list(map(lambda x: f"[bold]{x}[/bold]", content_lines))
    if pause and sys.stdin.isatty():
        content_lines.append("   [yellow bold]A crash course to Linux Shells and CLI tools [blink]█[/blink][/yellow bold]")
        content_lines.append("")
        content_lines.append("[dim]> Press [/dim][underline]Enter[/underline][dim] to continue...[/dim]")

    # Determine terminal size
    size = console.size
    term_height = size.height - 1   # -1 to leave space for entering (invisible) text

    target_content_lines = max(term_height - 2, 0)
    cur = len(content_lines)
    if cur < target_content_lines:
        remaining = target_content_lines - cur
        top_pad = remaining // 2
        bottom_pad = remaining - top_pad
        content_lines = (["" ] * top_pad) + content_lines + (["" ] * bottom_pad)
    elif cur > target_content_lines:
        content_lines = content_lines[:target_content_lines]

    # Horizontal centering inside full-screen panel
    term_width = size.width
    padding_lr = 2  # from padding=(0,2)
    inner_width = max(term_width - 2 - (padding_lr * 2), 10)

    line_texts = []
    for line in content_lines:
        t = Text.from_markup(line) if line else Text("")
        line_texts.append(t)

    centered = Text()
    for idx, t in enumerate(line_texts):
        cell_len = t.cell_len
        if cell_len >= inner_width:
            truncated = t.copy()
            if cell_len > inner_width:
                truncated = Text(truncated.plain[:inner_width])
            line_render = truncated
        else:
            pad_total = inner_width - cell_len
            left = pad_total // 2
            right = pad_total - left
            line_render = Text(" " * left) + t + Text(" " * right)
        centered.append(line_render)
        if idx != len(line_texts) - 1:
            centered.append("\n")

    panel = Panel(centered, border_style="yellow", expand=True, padding=(0,2))
    # Suppress trailing newline so the bottom border sits on the last terminal row
    console.print(panel, overflow="crop", no_wrap=True, end="")

    if pause and sys.stdin.isatty():
        try:
            for key in _read_keys_no_echo(stop_on_enter=True):  # will break on Enter
                if key in ("\x1b[D", "\x1b[C"):
                    continue
        except (EOFError, KeyboardInterrupt):
            pass


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    console = Console()
    hide_cursor = sys.stdout.isatty()
    try:
        if hide_cursor:
            sys.stdout.write(ANSI_HIDE_CURSOR)
            sys.stdout.flush()
        show_splash(console, pause = True)
    finally:
        if hide_cursor:
            sys.stdout.write(ANSI_SHOW_CURSOR)
            sys.stdout.flush()


if __name__ == "__main__":
    main()
