from __future__ import annotations

from ..models.failures import FailureCode, build_failure_reason
from ..models.failures import FailureReason


def validate_lightcone(nodes: list[object], edges: list[object]) -> list[FailureReason]:
    by_id = {n.id: n for n in nodes}
    reasons: list[FailureReason] = []
    for edge in edges:
        if edge.source not in by_id or edge.target not in by_id:
            reasons.append(
                build_failure_reason(
                    FailureCode.F005_LIGHTCONE_CONFLICT,
                    component="lightcone",
                    details="존재하지 않는 노드 참조",
                )
            )
            continue

        source_cone = by_id[edge.source].cone
        target_cone = by_id[edge.target].cone
        if source_cone not in {"local", "regional", "global"} or target_cone not in {
            "local",
            "regional",
            "global",
        }:
            reasons.append(
                build_failure_reason(
                    FailureCode.F005_LIGHTCONE_CONFLICT,
                    component="lightcone",
                    details=f"유효하지 않은 cone 값: {source_cone}/{target_cone}",
                )
            )
            continue

        if source_cone == "local" and target_cone == "global":
            reasons.append(
                build_failure_reason(
                    FailureCode.F005_LIGHTCONE_CONFLICT,
                    component="lightcone",
                    details="local 이벤트가 global 결과로 즉시 전파되는 간선",
                )
            )

    return reasons
