from pathlib import Path

from synapse_engine.models.events import EventNode, EventType
from synapse_engine.models.graph import CausalEdge
from synapse_engine.validators import dag_validator, conservation


def test_dag_validator_detects_self_loop() -> None:
    nodes = [
        EventNode(
            id="A",
            name="A",
            event_type=EventType.MEASURE,
            delta_e_range=(0.0, 0.0),
            delta_s_range=(0.1, 0.1),
            delta_i_range=(0.1, 0.1),
            cone="local",
        )
    ]
    edges = [CausalEdge(source="A", target="A", lag=(0.0, 0.0))]
    failures = dag_validator.validate_dag(nodes, edges)
    assert failures, "자기인과 간선은 실패를 만들어야 합니다"
    assert failures[0].code == "F002_SELF_CAUSATION"


def test_conservation_out_of_bounds() -> None:
    totals = {
        "energy": (5.0, 9.0),
        "entropy": (0.5, 1.0),
        "information": (1.5, 2.0),
    }
    bounds = {
        "energy_input": (0.0, 4.0),
        "entropy_delta_total": (0.0, 3.0),
        "info_record_bits": (0.0, 1.0),
    }
    failures = conservation.check_budget_bounds(totals, bounds)
    codes = {f.code for f in failures}
    assert "F003_CONSERVATION_VIOLATION" in codes
