from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path("outputs")


@dataclass
class ScoringConfig:
    feasibility_weight: float = 0.35
    risk_weight: float = -0.20
    utility_weight: float = 0.25
    fragility_weight: float = -0.20
    documentation_weight: float = 0.0

    @property
    def total_score_formula(self) -> str:
        return (
            "patch_score = 0.35*feasibility_score - 0.20*risk_score + "
            "0.25*utility_score - 0.20*fragility_score"
        )

    def compute_score(
        self, feasibility: float, risk: float, utility: float, fragility: float
    ) -> float:
        return (
            self.feasibility_weight * feasibility
            + self.risk_weight * risk
            + self.utility_weight * utility
            + self.fragility_weight * fragility
        )

    def to_dict(self) -> dict[str, float | int | str]:
        return asdict(self)


class SynapseError(Exception):
    pass


class SchemaValidationError(SynapseError):
    pass


class PipelineError(SynapseError):
    pass
