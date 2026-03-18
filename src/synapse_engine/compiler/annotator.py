from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..models.budgets import BudgetLedger
from ..utils.math_helpers import add_intervals


@dataclass
class AnnotationContext:
    source: str
    tags: list[str]
    metadata: dict[str, Any]


def annotate_patch_totals(events: list[Any]) -> BudgetLedger:
    energy = add_intervals([ev.delta_e_range for ev in events])
    entropy = add_intervals([ev.delta_s_range for ev in events])
    information = add_intervals([ev.delta_i_range for ev in events])
    return BudgetLedger(energy=energy, entropy=entropy, information=information)
