from pathlib import Path

from synapse_engine.compiler.parser import parse_input_file
from synapse_engine.synthesis import patch_fabricator
from synapse_engine.models.schema import SolverConfig


def test_solver_config_affects_score_formula(tmp_path: Path) -> None:
    source = (
        Path(__file__).resolve().parents[1] / "examples" / "basic_patch.yaml"
    ).read_text(encoding="utf-8")
    input_file = tmp_path / "input.yaml"
    input_file.write_text(source, encoding="utf-8")

    payload = parse_input_file(input_file)
    payload.solver_config = SolverConfig(
        feasibility_weight=1.0,
        risk_weight=-1.0,
        utility_weight=0.0,
        fragility_weight=-0.0,
    )
    proofs = patch_fabricator.synthesis_mode(payload, max_patches=1)
    assert len(proofs) >= 1
    proof = proofs[0]
    assert proof.scoring_weights["feasibility_weight"] == 1.0
