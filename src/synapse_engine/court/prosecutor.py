from __future__ import annotations

from ..models.failures import FailureReason, build_failure_reason, FailureCode
from ..validators import (
    dag_validator,
    conservation,
    entropy_ledger,
    lightcone,
    sensitivity,
)
from ..compiler.annotator import annotate_patch_totals
from ..compiler.type_checker import validate_input_types


def collect_attacks(patch_graph, context) -> list[FailureReason]:
    policy = context.domain_policy
    failures: list[FailureReason] = []

    for code in validate_input_types(context):
        failures.append(
            build_failure_reason(
                code,
                component="type_checker",
                details="지원되지 않는 이벤트 타입",
            )
        )

    failures.extend(
        dag_validator.validate_dag(
            patch_graph.nodes, patch_graph.edges, strict=policy.no_causal_loop
        )
    )
    totals = annotate_patch_totals(patch_graph.nodes)
    failures.extend(
        conservation.check_budget_bounds(
            totals=totals.as_dict(),
            bounds=context.observation_summary.bounds,
        )
    )
    failures.extend(
        entropy_ledger.check_entropy_policy(
            entropy_ledger.build_entropy_ledger(patch_graph.nodes, patch_graph.edges),
            non_decrease=policy.entropy_non_decrease,
        )
    )
    failures.extend(lightcone.validate_lightcone(patch_graph.nodes, patch_graph.edges))
    sensitivity_score, sensitivity_failures = (
        sensitivity.calculate_observation_sensitivity(
            context.observation_summary.uncertainties,
            context.domain_policy.sensitivity_threshold,
        )
    )
    failures.extend(sensitivity_failures)

    if policy.external_output_zero:
        for edge in patch_graph.edges:
            if getattr(edge, "relation_type", "") == "external_output":
                failures.append(
                    build_failure_reason(
                        FailureCode.F012_EXTERNAL_OUTPUT_POLICY_RISK,
                        component="prosecutor",
                        details="relation_type=external_output",
                    )
                )

    patch_graph.total_budget = totals.as_dict()
    patch_graph.constraint_status = {
        "sensitivity": sensitivity_score <= policy.sensitivity_threshold
    }

    return failures
