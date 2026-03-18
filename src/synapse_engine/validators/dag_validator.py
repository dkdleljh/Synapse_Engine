from __future__ import annotations

import networkx as nx

from ..models.failures import FailureCode, build_failure_reason
from ..models.failures import FailureReason


def validate_dag(
    nodes: list[object], edges: list[object], strict: bool = True
) -> list[FailureReason]:
    g = nx.DiGraph()
    for node in nodes:
        g.add_node(node.id)
    for edge in edges:
        if edge.source == edge.target:
            return [
                build_failure_reason(
                    FailureCode.F002_SELF_CAUSATION,
                    component="dag_validator",
                    details=f"{edge.source} -> {edge.target}",
                )
            ]
        g.add_edge(edge.source, edge.target)

    missing = {n for n in g.nodes if g.in_degree(n) == 0 and g.out_degree(n) == 0}
    reasons: list[FailureReason] = []
    if missing and strict:
        for node_id in sorted(missing):
            reasons.append(
                build_failure_reason(
                    FailureCode.F006_MISSING_CAUSE,
                    component="dag_validator",
                    details=f"고립 노드 {node_id}",
                )
            )

    if not nx.is_directed_acyclic_graph(g):
        reasons.append(
            build_failure_reason(
                FailureCode.F001_CAUSAL_LOOP,
                component="dag_validator",
                details="순환 간선이 탐지됨",
            )
        )

    return reasons
