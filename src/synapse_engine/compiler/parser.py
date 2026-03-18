from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ..config import SchemaValidationError
from ..models.schema import EngineInput


def parse_input_file(path: str | Path) -> EngineInput:
    path = Path(path)
    if not path.exists():
        raise SchemaValidationError(f"입력 파일을 찾을 수 없습니다: {path}")

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise SchemaValidationError("빈 입력 파일입니다.")

    if path.suffix.lower() in {".yaml", ".yml"}:
        payload = yaml.safe_load(text)
    elif path.suffix.lower() == ".json":
        import json

        payload = json.loads(text)
    else:
        raise SchemaValidationError("지원 형식은 yaml, yml, json만 허용합니다.")

    if not isinstance(payload, dict):
        raise SchemaValidationError("루트 객체가 객체 타입이 아닙니다.")

    try:
        return EngineInput.model_validate(payload)
    except Exception as exc:
        raise SchemaValidationError(f"스키마 검증 실패: {exc}") from exc


def as_plain_dict(payload: EngineInput) -> dict[str, Any]:
    return payload.model_dump()
