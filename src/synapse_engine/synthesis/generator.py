from __future__ import annotations

from dataclasses import dataclass

from ..compiler.dag_builder import build_patch_from_scenario
from ..compiler.dag_builder import build_event_node
from ..models.graph import PatchGraph, CausalEdge
from ..models.schema import CandidateScenario
from ..utils.ids import stable_id


@dataclass
class GeneratedPatch:
    patch_id: str
    scenario_id: str
    nodes: list
    edges: list


def generate_from_scenario(scenario: CandidateScenario) -> PatchGraph:
    nodes, edges = build_patch_from_scenario(scenario)
    return PatchGraph(
        nodes=nodes,
        edges=edges,
        graph_id=stable_id(scenario.id, str(len(nodes)), str(len(edges))),
    )


def synthesize_from_events(scenario: CandidateScenario) -> PatchGraph:
    nodes = [build_event_node(ev) for ev in scenario.events]
    edges = []
    for i in range(len(nodes) - 1):
        edges.append(
            CausalEdge(
                source=nodes[i].id,
                target=nodes[i + 1].id,
                lag=(0.0, 1.0),
                confidence=0.8,
                relation_type="causes",
                justification="자동 조립",
            )
        )
    return PatchGraph(
        nodes=nodes,
        edges=edges,
        graph_id=stable_id(scenario.id, "synth"),
    )
