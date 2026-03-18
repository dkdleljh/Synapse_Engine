from pathlib import Path

from typer.testing import CliRunner

from synapse_engine.cli import app


runner = CliRunner()


def test_cli_validate_basic(tmp_path: Path) -> None:
    source = (
        Path(__file__).resolve().parents[1] / "examples" / "basic_patch.yaml"
    ).read_text(encoding="utf-8")
    example = tmp_path / "basic.yaml"
    example.write_text(source, encoding="utf-8")
    result = runner.invoke(app, ["validate", str(example), "--mode", "manual"])
    assert result.exit_code in {0, 1}
    assert "결과 폴더" in result.stdout or "결과 폴더" in result.output


def test_cli_analyze_unstable_reports_rejected(tmp_path: Path) -> None:
    source = (
        Path(__file__).resolve().parents[1] / "examples" / "unstable_case.yaml"
    ).read_text(encoding="utf-8")
    example = tmp_path / "unstable.yaml"
    example.write_text(source, encoding="utf-8")

    result = runner.invoke(app, ["analyze", str(example)])

    assert result.exit_code == 0
    output = result.stdout or result.output
    assert "실패" in output
    assert "결과 폴더" in output
