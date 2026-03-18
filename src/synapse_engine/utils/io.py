from __future__ import annotations

from pathlib import Path

import yaml


def read_text(path: Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_yaml(path: Path, payload: object) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(payload, f, allow_unicode=True)
