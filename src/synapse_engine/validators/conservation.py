from __future__ import annotations

from ..models.failures import FailureCode, build_failure_reason
from ..models.failures import FailureReason
from ..utils.math_helpers import add_intervals


def check_budget_bounds(
    totals: dict[str, tuple[float, float]],
    bounds: dict[str, tuple[float, float]],
) -> list[FailureReason]:
    reasons: list[FailureReason] = []
    for key in ["energy_input", "entropy_delta_total", "info_record_bits"]:
        if key not in bounds:
            continue
        lo, hi = bounds[key]
        if key == "energy_input":
            value_key = "energy"
        elif key == "entropy_delta_total":
            value_key = "entropy"
        else:
            value_key = "information"

        if value_key not in totals:
            continue

        t_lo, t_hi = totals[value_key]
        if t_hi < lo or t_lo > hi:
            reasons.append(
                build_failure_reason(
                    FailureCode.F003_CONSERVATION_VIOLATION,
                    component="conservation",
                    details=(
                        f"{key} 범위={lo}-{hi}, patch={t_lo}-{t_hi} (교집합 없음)"
                    ),
                )
            )

    return reasons


def check_information_budget(
    totals: tuple[float, float], policy_limit: float | None
) -> list[FailureReason]:
    if policy_limit is None:
        return []
    lo, hi = totals
    if hi > policy_limit:
        return [
            build_failure_reason(
                FailureCode.F008_INFORMATION_BUDGET_EXCEEDED,
                component="conservation",
                details=f"정보 상한({policy_limit}) 초과: {hi}",
            )
        ]
    if lo > policy_limit:
        return []
    return []
