from __future__ import annotations

from ..compiler.type_checker import validate_event_type
from ..court.judge import evaluate_scores
from ..models.proofs import ProofBundle
from ..models.failures import FailureCode, build_failure_reason
from ..models.schema import EngineInput
from ..utils.ids import stable_id
from ..synthesis.generator import generate_from_scenario, synthesize_from_events
from ..court.judge import evaluate_patch


def _build_type_failure_proof(
    scenario_id: str, payload: EngineInput, invalid_types: list[str]
) -> ProofBundle:
    failures = [
        build_failure_reason(
            FailureCode.F009_UNSUPPORTED_EVENT_TYPE,
            component="type_checker",
            details=f"지원되지 않는 이벤트 타입: {event_type}",
        )
        for event_type in invalid_types
    ]
    feasibility, risk, utility, fragility, documentation = evaluate_scores(
        failures, payload
    )
    return ProofBundle(
        patch_id=stable_id(scenario_id, "type_check"),
        passed=False,
        feasibility_score=feasibility,
        risk_score=risk,
        utility_score=utility,
        fragility_score=fragility,
        documentation_score=documentation,
        proof_level="PoP-L0",
        proof_notes=["event_type_validation_failed"],
        scoring_weights={
            "feasibility_weight": payload.solver_config.feasibility_weight,
            "risk_weight": payload.solver_config.risk_weight,
            "utility_weight": payload.solver_config.utility_weight,
            "fragility_weight": payload.solver_config.fragility_weight,
        },
        failures=failures,
        checks={"type_check": False},
        graph_summary={"nodes": [], "edges": [], "total_budget": {}},
    )


def _collect_invalid_types(payload: EngineInput, scenario_id: str) -> list[str]:
    scenario = next(
        (s for s in payload.candidate_scenarios if s.id == scenario_id),
        None,
    )
    if scenario is None:
        return []
    return [
        event.type for event in scenario.events if not validate_event_type(event.type)
    ]


def manual_mode(input_payload: EngineInput) -> list[ProofBundle]:
    proofs: list[ProofBundle] = []
    for scenario in input_payload.candidate_scenarios:
        invalid_types = _collect_invalid_types(input_payload, scenario.id)
        if invalid_types:
            proof = _build_type_failure_proof(scenario.id, input_payload, invalid_types)
            if proof.passed or not input_payload.solver_config.strict_mode:
                proofs.append(proof)
            continue

        patch_graph = generate_from_scenario(scenario)
        proof = evaluate_patch(patch_graph, scenario.id, input_payload)
        if proof.passed or not input_payload.solver_config.strict_mode:
            proofs.append(proof)
    return proofs


def synthesis_mode(
    input_payload: EngineInput, max_patches: int = 10
) -> list[ProofBundle]:
    proofs: list[ProofBundle] = []
    remaining = max_patches
    for scenario in input_payload.candidate_scenarios:
        if remaining <= 0:
            break

        invalid_types = _collect_invalid_types(input_payload, scenario.id)
        if invalid_types:
            proof = _build_type_failure_proof(scenario.id, input_payload, invalid_types)
            if proof.passed or not input_payload.solver_config.strict_mode:
                proofs.append(proof)
                remaining -= 1
            continue

        patch_graph = synthesize_from_events(scenario)
        proof = evaluate_patch(patch_graph, scenario.id, input_payload)
        if proof.passed or not input_payload.solver_config.strict_mode:
            proofs.append(proof)
            remaining -= 1
    return proofs
