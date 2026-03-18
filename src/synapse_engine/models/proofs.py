from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .failures import FailureReason


class ProofBundle(BaseModel):
    patch_id: str
    passed: bool
    feasibility_score: float
    risk_score: float
    utility_score: float
    fragility_score: float
    documentation_score: float = 0.0
    proof_level: str = "PoP-L1"
    proof_notes: list[str] = Field(default_factory=list)
    scoring_weights: dict[str, float] = Field(default_factory=dict)
    failures: list[FailureReason] = Field(default_factory=list)
    checks: dict[str, bool] = Field(default_factory=dict)
    constraints: dict[str, Any] = Field(default_factory=dict)
    graph_summary: dict[str, Any] = Field(default_factory=dict)

    @property
    def patch_score(self) -> float:
        score = (
            self.scoring_weights.get("feasibility_weight", 0.35)
            * self.feasibility_score
            + self.scoring_weights.get("risk_weight", -0.20) * self.risk_score
            + self.scoring_weights.get("utility_weight", 0.25) * self.utility_score
            + self.scoring_weights.get("fragility_weight", -0.20) * self.fragility_score
        )
        return score


class RiskItem(BaseModel):
    risk_id: str
    description: str
    severity: str
    likelihood: float
    impacted_component: str
    mitigation: str


class RiskRegister(BaseModel):
    items: list[RiskItem] = Field(default_factory=list)
