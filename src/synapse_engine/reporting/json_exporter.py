from __future__ import annotations

from pathlib import Path

from ..utils.io import write_text


def export_json(payload: object, path: str | Path) -> None:
    write_text(
        Path(path), __import__("json").dumps(payload, ensure_ascii=False, indent=2)
    )
