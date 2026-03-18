from __future__ import annotations

import json
import datetime

from ..models.proofs import ProofBundle
from ..counterfactual.minimal_cause import estimate_minimal_cause_set


class CounterfactualResult(dict):
    pass


def analyze_counterfactuals(
    input_payload, proofs: list[ProofBundle]
) -> CounterfactualResult:
    cases: list[dict[str, object]] = []
    for proof in proofs:
        nodes = list(proof.graph_summary.get("nodes", []))
        edges = [tuple(edge) for edge in proof.graph_summary.get("edges", [])]
        case = {
            "patch_id": proof.patch_id,
            "status": "passed" if proof.passed else "failed",
            "budget_shock": {
                "default_fail_at_70": not proof.passed,
                "first_break": proof.failures[0].code if proof.failures else "none",
            },
            "cause_importance": estimate_minimal_cause_set(nodes, edges, proof),
            "risk_codes": [f.code for f in proof.failures],
        }
        cases.append(case)

    report = {
        "generated_at": datetime.datetime.now().isoformat(),
        "goal": input_payload.goal_function.primary,
        "cases": cases,
    }
    if cases:
        failed_count = sum(1 for c in cases if c["status"] == "failed")
        report["summary"] = (
            f"총 {len(cases)}개 패치 중 {failed_count}개가 실패했습니다."
            if failed_count
            else "모든 패치가 통과했습니다."
        )
    else:
        report["summary"] = "평가 가능한 패치가 없습니다."
    return CounterfactualResult(report)
