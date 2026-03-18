from __future__ import annotations

from ..models.failures import FailureCode, build_failure_reason


def calculate_observation_sensitivity(
    uncertainties: dict[str, dict[str, object]], threshold: float
) -> tuple[float, list]:
    if not uncertainties:
        return 0.0, []

    scores: list[float] = []
    for payload in uncertainties.values():
        if payload.get("type") == "gaussian":
            std = float(payload.get("std", 0.0))
            mean = float(payload.get("mean", 0.0))
            if mean == 0:
                score = min(1.0, std)
            else:
                score = min(1.0, abs(std / mean))
            scores.append(score)
        else:
            scores.append(0.2)

    worst = max(scores)
    reasons = []
    if worst > threshold:
        reasons.append(
            build_failure_reason(
                FailureCode.F007_OBSERVATION_OVER_SENSITIVITY,
                component="sensitivity",
                details=f"최대 민감도 {worst:.2f} > {threshold}",
            )
        )
    return worst, reasons
