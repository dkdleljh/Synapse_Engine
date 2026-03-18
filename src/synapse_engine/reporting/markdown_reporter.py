from __future__ import annotations

from pathlib import Path

from ..utils.io import write_text


def render_proof_report(patch) -> str:
    lines = [
        f"# Patch {patch.patch_id}",
        "",
        f"- 통과: {patch.passed}",
        f"- 점수: {patch.patch_score:.3f}",
        f"- 증명수준: {patch.proof_level}",
        f"- 제약 통과 여부: {patch.checks}",
    ]
    if patch.failures:
        lines.extend(["", "## 실패 사유", ""])
        for f in patch.failures:
            lines.append(f"- {f.code}: {f.title}")
    return "\n".join(lines)


def write_proof_document(patch, path: str | Path) -> None:
    write_text(Path(path), render_proof_report(patch))


def write_risk_register(risks, path: str | Path) -> None:
    lines = ["# risk_register", ""]
    for item in risks.items:
        lines.append(f"- {item.risk_id} / {item.description} / 심각도 {item.severity}")
    write_text(Path(path), "\n".join(lines))


def write_failure_report(patches, path: str | Path) -> None:
    lines = ["# failure_report", ""]
    for patch in patches:
        if not patch.passed:
            lines.append(f"## {patch.patch_id}")
            for f in patch.failures:
                lines.append(f"- {f.code}: {f.human_explanation}")
            lines.append("")
    write_text(Path(path), "\n".join(lines))


def write_run_summary(passed: list, rejected: list, path: str | Path) -> None:
    lines = [
        "# run_summary",
        f"- 통과 패치 수: {len(passed)}",
        f"- 실패 패치 수: {len(rejected)}",
        "",
    ]
    for item in passed[:5]:
        lines.append(f"- PASS {item.patch_id}: {item.patch_score:.3f}")
    for item in rejected[:5]:
        lines.append(f"- FAIL {item.patch_id}: {item.patch_score:.3f}")
    write_text(Path(path), "\n".join(lines))
