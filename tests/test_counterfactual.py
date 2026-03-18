from pathlib import Path

from synapse_engine.compiler.parser import parse_input_file
from synapse_engine.synthesis import patch_fabricator
from synapse_engine.counterfactual.engine import analyze_counterfactuals


def test_counterfactual_report_has_summary_and_cases(tmp_path: Path) -> None:
    source = (
        Path(__file__).resolve().parents[1] / "examples" / "basic_patch.yaml"
    ).read_text(encoding="utf-8")
    input_file = tmp_path / "basic.yaml"
    input_file.write_text(source, encoding="utf-8")
    payload = parse_input_file(input_file)
    proofs = patch_fabricator.synthesis_mode(payload, max_patches=2)
    report = analyze_counterfactuals(payload, proofs)
    assert "cases" in report
    assert isinstance(report["cases"], list)
    assert "summary" in report
