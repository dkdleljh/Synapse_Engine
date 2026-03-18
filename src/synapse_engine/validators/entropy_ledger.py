from __future__ import annotations

from collections import deque
from typing import Any

from ..models.events import EventNode
from ..models.failures import FailureCode, build_failure_reason
from ..models.failures import FailureReason


def build_entropy_ledger(
    nodes: list[EventNode], edges: list[Any]
) -> list[tuple[str, float, float]]:
    by_id = {n.id: n for n in nodes}
    indeg: dict[str, int] = {n.id: 0 for n in nodes}
    nexts: dict[str, list[str]] = {n.id: [] for n in nodes}
    for edge in edges:
        nexts[edge.source].append(edge.target)
        indeg[edge.target] += 1

    queue = deque([node_id for node_id, d in indeg.items() if d == 0])
    order: list[str] = []
    while queue:
        cur = queue.popleft()
        order.append(cur)
        for nxt in nexts[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    if len(order) != len(nodes):
        order = [n.id for n in nodes]

    total = 0.0
    ledger: list[tuple[str, float, float]] = []
    for node_id in order:
        node = by_id[node_id]
        lo, hi = node.delta_s_range
        total += lo
        ledger.append((node_id, total, hi))
    return ledger


def check_entropy_policy(
    ledger: list[tuple[str, float, float]], non_decrease: bool
) -> list[FailureReason]:
    if not non_decrease:
        return []
    reasons: list[FailureReason] = []
    prev = -1e18
    for node_id, min_total, max_total in ledger:
        if min_total < prev - 1e-9:
            reasons.append(
                build_failure_reason(
                    FailureCode.F004_ENTROPY_REVERSAL,
                    component="entropy_ledger",
                    details=f"노드 {node_id}에서 역전 감지",
                )
            )
        prev = min_total
    return reasons
