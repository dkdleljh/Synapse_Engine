from pathlib import Path

import pytest

from synapse_engine.compiler.parser import parse_input_file
from synapse_engine.config import SchemaValidationError


def _write_basic_yaml(path: Path) -> None:
    path.write_text(
        """
observation_summary:
  relations: ["obs"]
  bounds:
    energy_input: [0.0, 10.0]
    entropy_delta_total: [0.0, 8.0]
    info_record_bits: [0.0, 6.0]
  uncertainties: {}
goal_function:
  primary: maximize_information_gain
  secondary: []
domain_policy:
  no_causal_loop: true
  entropy_non_decrease: true
  local_conservation: true
  external_output_zero: true
  sensitivity_threshold: 0.7
  bounded_information_operations: true
candidate_scenarios:
  - id: s1
    events:
      - id: E1
        type: EnergyInjection
        delta_e: [1.0, 2.0]
        delta_s: [0.1, 0.2]
        delta_i: [0.1, 0.4]
        cone: local
        preconditions: []
        postconditions: []
    edges: []
""".strip(),
        encoding="utf-8",
    )


def test_parse_yaml_file_valid(tmp_path: Path) -> None:
    file_path = tmp_path / "input.yaml"
    _write_basic_yaml(file_path)
    payload = parse_input_file(file_path)
    assert payload.goal_function.primary == "maximize_information_gain"
    assert payload.candidate_scenarios[0].id == "s1"


def test_parse_invalid_extension(tmp_path: Path) -> None:
    txt = tmp_path / "input.txt"
    txt.write_text("invalid", encoding="utf-8")
    with pytest.raises(SchemaValidationError):
        parse_input_file(txt)
