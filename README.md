# Shell Dojo Core

An interactive crash course to Linux Shells and CLI tools featuring a rich terminal interface with navigation controls.

## Usage

### Prerequisites

Ensure you have `uv` installed. Then setup `venv` via

```bash
uv sync
```

Then activate the virtual environment
```bash
source .venv/bin/activate
```

### Running the Interactive Tutorial

To start the interactive tutorial interface:

```bash
export DOJO_CH_ID=<module_id> && python main.py
```

**Example:**
```bash
export DOJO_CH_ID=M0P0 && python main.py
```

### Creating New Content

Each module should have an `export.py` file with:

- `__module_name__`: Display name for the module
- `__show_splash__`: Whether to show splash screen
- `__pages__`: List of page objects

**Example:**
```python
from utils.pages import lines_page, markdown_file

__module_name__ = "My Module"
__show_splash__ = True

__pages__ = [
    lines_page(["[bold]Welcome![/bold]", "This is a page"]),
    markdown_file(Path("content.md")),
]
```

## What to teach

See [WHAT_TO_TEACH.md](WHAT_TO_TEACH.md) for guidelines on content creation.