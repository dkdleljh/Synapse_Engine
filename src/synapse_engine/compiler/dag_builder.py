from __future__ import annotations

from ..models.events import EventNode
from ..models.graph import CausalEdge
from ..models.schema import CandidateEvent, CandidateScenario


def build_event_node(event: CandidateEvent) -> EventNode:
    return EventNode(
        id=event.id,
        name=event.name or event.id,
        event_type=event.type,
        delta_e_range=tuple(float(x) for x in event.delta_e),
        delta_s_range=tuple(float(x) for x in event.delta_s),
        delta_i_range=tuple(float(x) for x in event.delta_i),
        cone=event.cone,
        preconditions=list(event.preconditions),
        postconditions=list(event.postconditions),
        metadata=dict(event.metadata),
    )


def build_patch_from_scenario(
    scenario: CandidateScenario,
) -> tuple[list[EventNode], list[CausalEdge]]:
    nodes = [build_event_node(ev) for ev in scenario.events]
    edges = [
        CausalEdge(
            source=ed.source,
            target=ed.target,
            lag=tuple(float(v) for v in ed.lag),
            confidence=ed.confidence,
            relation_type=ed.relation_type,
            justification=ed.justification,
        )
        for ed in scenario.edges
    ]
    return nodes, edges
