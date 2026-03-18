from __future__ import annotations

from rich.console import Console


def get_console() -> Console:
    return Console(highlight=False)
