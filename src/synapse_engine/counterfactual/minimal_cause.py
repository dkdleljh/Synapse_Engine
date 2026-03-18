from __future__ import annotations

from ..models.proofs import ProofBundle


def estimate_minimal_cause_set(
    node_ids: list[str], edges: list[tuple[str, str]], proof: ProofBundle
) -> list[str]:
    if proof.passed:
        return [f"node:{node_ids[0]}"] if node_ids else []

    causes = []
    for source, target in edges[:2]:
        causes.append(f"edge:{source}->{target}")
    for node_id in node_ids[:2]:
        causes.append(f"node:{node_id}")
    return causes[:3]
