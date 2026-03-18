from __future__ import annotations

import hashlib


def stable_id(*parts: str) -> str:
    text = "|".join(parts)
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
