from pathlib import Path

from synapse_engine.compiler.parser import parse_input_file
from synapse_engine.models.failures import FailureCode
from synapse_engine.models.schema import SolverConfig
from synapse_engine.synthesis import patch_fabricator


def test_manual_and_synthesis_mode_counts(tmp_path: Path) -> None:
    source = (
        Path(__file__).resolve().parents[1] / "examples" / "basic_patch.yaml"
    ).read_text(encoding="utf-8")
    input_file = tmp_path / "example.yaml"
    input_file.write_text(source, encoding="utf-8")
    payload = parse_input_file(input_file)
    payload.solver_config = SolverConfig()

    manual = patch_fabricator.manual_mode(payload)
    synthesis = patch_fabricator.synthesis_mode(payload, max_patches=3)
    assert len(manual) >= 1
    assert len(synthesis) >= 1
    assert manual[0].patch_id
    assert synthesis[0].passed or not payload.solver_config.strict_mode


def test_synthesis_mode_unsupported_event_type_returns_rejected_proof(
    tmp_path: Path,
) -> None:
    source = (
        Path(__file__).resolve().parents[1] / "examples" / "unstable_case.yaml"
    ).read_text(encoding="utf-8")
    input_file = tmp_path / "unstable.yaml"
    input_file.write_text(source, encoding="utf-8")
    payload = parse_input_file(input_file)
    payload.solver_config = SolverConfig(strict_mode=False)

    proofs = patch_fabricator.synthesis_mode(payload, max_patches=10)

    assert len(proofs) == 1
    assert proofs[0].passed is False
    assert proofs[0].failures
    assert proofs[0].failures[0].code == FailureCode.F009_UNSUPPORTED_EVENT_TYPE
