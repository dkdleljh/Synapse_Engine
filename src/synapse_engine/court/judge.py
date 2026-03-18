from __future__ import annotations

from ..models.proofs import ProofBundle
from ..models.schema import EngineInput
from ..utils.ids import stable_id
from . import prosecutor


def evaluate_scores(
    failures: list, context: EngineInput
) -> tuple[float, float, float, float, float]:
    fail_count = len(failures)
    feasibility = max(0.0, 1.0 - 0.2 * fail_count)
    risk = min(1.0, 0.1 * fail_count + 0.2)
    fragility = 0.0
    utility = 0.5
    if context.goal_function.primary in {"maximize_information_gain", "minimize_risk"}:
        utility = 0.7
    documentation = 0.7 if fail_count == 0 else 0.4
    return feasibility, risk, utility, fragility, documentation


def evaluate_patch(graph, scenario_id: str, context: EngineInput) -> ProofBundle:
    failures = prosecutor.collect_attacks(graph, context)
    feasibility, risk, utility, fragility, documentation = evaluate_scores(
        failures, context
    )
    proof = ProofBundle(
        patch_id=graph.graph_id or stable_id(scenario_id),
        passed=(len(failures) == 0),
        feasibility_score=feasibility,
        risk_score=risk,
        utility_score=utility,
        fragility_score=fragility,
        documentation_score=documentation,
        scoring_weights={
            "feasibility_weight": context.solver_config.feasibility_weight,
            "risk_weight": context.solver_config.risk_weight,
            "utility_weight": context.solver_config.utility_weight,
            "fragility_weight": context.solver_config.fragility_weight,
        },
        proof_level="PoP-L1" if len(failures) == 0 else "PoP-L0",
        proof_notes=[f"failure_count={len(failures)}"],
        failures=failures,
        checks={"graph_id": bool(graph.graph_id)},
        constraints=graph.constraint_status,
        graph_summary={
            "nodes": [n.id for n in graph.nodes],
            "edges": [(e.source, e.target) for e in graph.edges],
            "total_budget": graph.total_budget,
        },
    )
    graph.proof_status = "passed" if proof.passed else "failed"
    return proof
