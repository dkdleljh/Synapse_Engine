from __future__ import annotations

from ..models.proofs import ProofBundle, RiskRegister


def archive(
    proofs: list[ProofBundle],
) -> tuple[list[ProofBundle], list[ProofBundle], RiskRegister]:
    accepted = [p for p in proofs if p.passed]
    rejected = [p for p in proofs if not p.passed]
    risks = RiskRegister(
        items=[
            {
                "risk_id": f"risk_{idx}",
                "description": "파라미터 임계 초과",
                "severity": "medium",
                "likelihood": 0.4,
                "impacted_component": p.patch_id,
                "mitigation": "민감도 임계치와 정보 예산 점검",
            }
            for idx, p in enumerate(rejected)
        ]
    )
    return accepted, rejected, risks
