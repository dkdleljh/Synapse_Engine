from __future__ import annotations

from pydantic import BaseModel, Field


class BudgetLedger(BaseModel):
    energy: tuple[float, float] = (0.0, 0.0)
    entropy: tuple[float, float] = (0.0, 0.0)
    information: tuple[float, float] = (0.0, 0.0)

    def as_dict(self) -> dict[str, tuple[float, float]]:
        return {
            "energy": self.energy,
            "entropy": self.entropy,
            "information": self.information,
        }


class Bounds(BaseModel):
    min: float
    max: float

    def contains(self, value_range: tuple[float, float]) -> bool:
        lo, hi = value_range
        return self.min <= hi and self.max >= lo
