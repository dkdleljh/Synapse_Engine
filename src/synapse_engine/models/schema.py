from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_validator

from .events import EventNode


class RelationRecord(BaseModel):
    source: str
    target: str
    text: str


class ObservationSummary(BaseModel):
    relations: list[str] = Field(default_factory=list)
    bounds: dict[str, tuple[float, float]] = Field(default_factory=dict)
    uncertainties: dict[str, dict[str, Any]] = Field(default_factory=dict)


class GoalFunction(BaseModel):
    primary: str
    secondary: list[str] = Field(default_factory=list)


class DomainPolicy(BaseModel):
    no_causal_loop: bool = True
    entropy_non_decrease: bool = True
    local_conservation: bool = True
    external_output_zero: bool = True
    sensitivity_threshold: float = 0.7
    bounded_information_operations: bool = True


class SolverConfig(BaseModel):
    strict_mode: bool = True
    max_patches: int = 10
    seed: int | None = None
    allow_partial: bool = False
    feasibility_weight: float = 0.35
    risk_weight: float = -0.20
    utility_weight: float = 0.25
    fragility_weight: float = -0.20
    documentation_weight: float = 0.0


class CandidateEvent(BaseModel):
    id: str
    type: str
    delta_e: tuple[float, float]
    delta_s: tuple[float, float]
    delta_i: tuple[float, float]
    cone: str = "local"
    preconditions: list[str] = Field(default_factory=list)
    postconditions: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    name: str | None = None

    @model_validator(mode="after")
    def _normalize(self) -> "CandidateEvent":
        de = self.delta_e
        ds = self.delta_s
        di = self.delta_i
        if de[0] > de[1] or ds[0] > ds[1] or di[0] > di[1]:
            raise ValueError("delta_ 계열 range 오더 오류")
        return self


class CandidateEdge(BaseModel):
    source: str
    target: str
    lag: tuple[float, float] = (0.0, 0.0)
    relation_type: str = "causes"
    confidence: float = 1.0
    justification: str = ""


class CandidateScenario(BaseModel):
    id: str
    events: list[CandidateEvent]
    edges: list[CandidateEdge] = Field(default_factory=list)


class EngineInput(BaseModel):
    observation_summary: ObservationSummary
    goal_function: GoalFunction
    domain_policy: DomainPolicy
    candidate_scenarios: list[CandidateScenario] = Field(default_factory=list)
    solver_config: SolverConfig = Field(default_factory=SolverConfig)

    @property
    def event_types(self) -> set[str]:
        out: set[str] = set()
        for sc in self.candidate_scenarios:
            for ev in sc.events:
                out.add(ev.type)
        return out


class ValidatedInput(BaseModel):
    data: EngineInput


class ParsedScenario(BaseModel):
    scenario_id: str
    events: list[object]
    edges: list[CandidateEdge]


class PatchCandidate(BaseModel):
    scenario_id: str
    events: list[EventNode]
    edges: list[CandidateEdge]


class PipelineResult(BaseModel):
    input: EngineInput
    valid: bool
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    failure_reasons: list[Any] = Field(default_factory=list)
