from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Interval:
    lo: float
    hi: float

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("interval min > max")

    def add(self, other: "Interval") -> "Interval":
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def overlap(self, other: "Interval") -> bool:
        return not (self.hi < other.lo or self.lo > other.hi)

    def contains(self, other: "Interval") -> bool:
        return self.lo <= other.lo and self.hi >= other.hi


def add_intervals(ranges: list[tuple[float, float]]) -> tuple[float, float]:
    if not ranges:
        return 0.0, 0.0
    lo = sum(r[0] for r in ranges)
    hi = sum(r[1] for r in ranges)
    return lo, hi


def interval_width(value_range: tuple[float, float]) -> float:
    return value_range[1] - value_range[0]
