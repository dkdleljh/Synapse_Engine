from __future__ import annotations

from ..models.failures import FailureReason


def run_constraint_kernel(context: dict) -> dict[str, bool]:
    return {
        "no_causal_loop": not bool(context.get("no_causal_loop", [])),
        "entropy_non_decrease": not bool(context.get("entropy_non_decrease", [])),
        "local_conservation": not bool(context.get("local_conservation", [])),
        "bounded_information_operations": not bool(
            context.get("bounded_information_operations", [])
        ),
        "observation_constraints": not bool(context.get("observation_constraints", [])),
    }


def gather_proof_lines(
    all_failures: list[FailureReason],
    failures_by_category: dict[str, list[FailureReason]],
) -> dict:
    return {
        "total_failures": len(all_failures),
        "by_category": {k: len(v) for k, v in failures_by_category.items()},
        "passed": len(all_failures) == 0,
    }
