from __future__ import annotations

from datetime import datetime
from pathlib import Path

import typer

from rich.console import Console
from rich.table import Table

from .compiler.parser import parse_input_file
from .config import DEFAULT_OUTPUT_DIR
from .synthesis import patch_fabricator
from .synthesis.ranker import rank_patches
from .court.archivist import archive
from .reporting.json_exporter import export_json
from .reporting.yaml_exporter import export_yaml
from .models.schema import EngineInput
from .reporting.markdown_reporter import (
    write_failure_report,
    write_proof_document,
    write_risk_register,
    write_run_summary,
)
from .reporting.html_reporter import write_html_report
from .counterfactual.engine import analyze_counterfactuals
from .models.proofs import ProofBundle
from .utils.io import write_text


app = typer.Typer(help="Synapse Engine CLI", add_completion=False)
console = Console(highlight=False)


def _result_dir(seed: int | None = None) -> Path:
    suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    if seed is not None:
        suffix = f"{suffix}_seed{seed}"
    return Path(DEFAULT_OUTPUT_DIR) / f"run_{suffix}"


def _write_outputs(
    input_payload, proofs, out_dir: Path, include_counterfactual: bool = False
) -> None:
    accepted, rejected, risks = archive(proofs)
    out_dir.mkdir(parents=True, exist_ok=True)

    export_json([p.model_dump() for p in proofs], out_dir / "patch_bundle.json")
    export_yaml([p.model_dump() for p in proofs], out_dir / "patch_program.yaml")

    if proofs:
        write_proof_document(
            accepted[0] if accepted else proofs[0], out_dir / "proof_of_possibility.md"
        )
    write_risk_register(risks, out_dir / "risk_register.md")
    write_failure_report(proofs, out_dir / "failure_report.md")
    write_run_summary(accepted, rejected, out_dir / "run_summary.md")
    write_text(
        out_dir / "reality_safe_spec.md",
        "# reality_safe_spec\n\n로컬 기반 증거 기반 시나리오 검증 산출물을 외부 세계 실행 없이 설명한다.\n",
    )
    write_html_report(proofs, risks, out_dir / "html_report/index.html")

    if include_counterfactual:
        cfr = analyze_counterfactuals(input_payload, proofs)
        write_text(
            out_dir / "counterfactual_report.md",
            f"# counterfactual_report\n\n{cfr.get('summary', '')}\n",
        )
        import json

        with (out_dir / "cause_importance_ranking.json").open(
            "w", encoding="utf-8"
        ) as f:
            json.dump(cfr, f, ensure_ascii=False, indent=2)


def _print_summary(accepted, rejected) -> None:
    table = Table()
    table.add_column("구분")
    table.add_column("수")
    table.add_row("통과", str(len(accepted)))
    table.add_row("실패", str(len(rejected)))
    console.print(table)


def _process_payload(
    input_file: str, strict: bool, seed: int | None, max_patches: int
) -> EngineInput:
    payload = parse_input_file(input_file)
    payload.solver_config.strict_mode = strict
    payload.solver_config.seed = seed
    payload.solver_config.max_patches = max_patches
    return payload


def _run_pipeline(
    input_file: str,
    strict: bool,
    seed: int | None,
    max_patches: int,
    mode: str,
    verbose: bool,
    include_counterfactual: bool = False,
) -> tuple[Path, list[ProofBundle], list[ProofBundle]]:
    payload = _process_payload(input_file, strict, seed, max_patches)
    if mode == "synthesis":
        proofs = patch_fabricator.synthesis_mode(payload, max_patches=max_patches)
    elif mode == "manual":
        proofs = patch_fabricator.manual_mode(payload)
    else:
        raise typer.BadParameter("지원 모드는 manual 또는 synthesis 입니다.")

    proofs = rank_patches(proofs, top_n=max_patches)
    accepted, rejected, _ = archive(proofs)

    if verbose:
        console.print(f"[dim]입력: {input_file}[/dim]")
        console.print(
            f"[dim]모드={mode}, strict={strict}, seed={seed}, max_patches={max_patches}[/dim]"
        )

    out_dir = _result_dir(seed)
    _write_outputs(
        payload, proofs, out_dir, include_counterfactual=include_counterfactual
    )
    return out_dir, accepted, rejected


@app.command()
def validate(
    input_file: str,
    strict: bool = typer.Option(False, "--strict", help="엄격 모드"),
    seed: int | None = typer.Option(None, "--seed", help="재현 시드"),
    mode: str = typer.Option(
        "manual", "--mode", help="patch 생성 모드 manual|synthesis"
    ),
    verbose: bool = typer.Option(False, "--verbose", help="상세 로그 출력"),
):
    out_dir, accepted, rejected = _run_pipeline(
        input_file,
        strict=strict,
        seed=seed,
        max_patches=5,
        mode=mode,
        verbose=verbose,
    )
    _print_summary(accepted, rejected)
    console.print(f"결과 폴더: {out_dir}")
    if rejected:
        raise typer.Exit(code=1)


@app.command()
def synthesize(
    input_file: str,
    max_patches: int = typer.Option(10, "--max-patches", help="최대 채택 패치 수"),
    strict: bool = typer.Option(False, "--strict", help="엄격 모드"),
    seed: int | None = typer.Option(None, "--seed", help="재현 시드"),
    verbose: bool = typer.Option(False, "--verbose", help="상세 로그 출력"),
):
    out_dir, accepted, rejected = _run_pipeline(
        input_file,
        strict=strict,
        seed=seed,
        max_patches=max_patches,
        mode="synthesis",
        verbose=verbose,
    )
    _print_summary(accepted, rejected)
    console.print(f"결과 폴더: {out_dir}")


@app.command()
def analyze(
    input_file: str,
    counterfactual: bool = typer.Option(
        True, "--counterfactual", help="반사실 분석 수행"
    ),
    strict: bool = typer.Option(False, "--strict", help="엄격 모드"),
    seed: int | None = typer.Option(None, "--seed", help="재현 시드"),
    verbose: bool = typer.Option(False, "--verbose", help="상세 로그 출력"),
):
    out_dir, accepted, rejected = _run_pipeline(
        input_file,
        strict=strict,
        seed=seed,
        max_patches=10,
        mode="synthesis",
        verbose=verbose,
        include_counterfactual=counterfactual,
    )
    _print_summary(accepted, rejected)
    console.print(f"결과 폴더: {out_dir}")


@app.command()
def export(
    input_file: str,
    format: str = typer.Option("html", "--format", help="json | yaml | html | all"),
    strict: bool = typer.Option(False, "--strict", help="엄격 모드"),
    seed: int | None = typer.Option(None, "--seed", help="재현 시드"),
    verbose: bool = typer.Option(False, "--verbose", help="상세 로그 출력"),
):
    if format not in {"json", "yaml", "html", "all"}:
        raise typer.BadParameter("지원 형식은 json, yaml, html, all 입니다.")
    out_dir, _, _ = _run_pipeline(
        input_file,
        strict=strict,
        seed=seed,
        max_patches=10,
        mode="synthesis",
        verbose=verbose,
    )
    if format == "json":
        console.print(out_dir / "patch_bundle.json")
    elif format == "yaml":
        console.print(out_dir / "patch_program.yaml")
    elif format == "html":
        console.print(out_dir / "html_report/index.html")
    else:
        console.print(out_dir / "patch_bundle.json")
        console.print(out_dir / "patch_program.yaml")
        console.print(out_dir / "html_report/index.html")


@app.command()
def demo(name: str = typer.Argument(..., help="basic | policy | scifi")):
    examples = {
        "basic": "basic_patch.yaml",
        "policy": "research_design.yaml",
        "scifi": "hard_scifi_device.yaml",
    }
    file_name = examples.get(name)
    if file_name is None:
        raise typer.BadParameter("지원되는 데모는 basic, policy, scifi 입니다.")
    root = Path(__file__).resolve().parents[2] / "examples"
    out_dir, accepted, rejected = _run_pipeline(
        str(root / file_name),
        strict=False,
        seed=None,
        max_patches=10,
        mode="synthesis",
        verbose=False,
    )
    _print_summary(accepted, rejected)
    console.print(f"결과 폴더: {out_dir}")


def run() -> None:
    app()
