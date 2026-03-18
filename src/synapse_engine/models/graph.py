from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CausalEdge(BaseModel):
    source: str
    target: str
    lag: tuple[float, float]
    confidence: float = 1.0
    relation_type: str = "causes"
    justification: str = ""

    def __init__(self, **data: Any):
        lag = data.get("lag", (0.0, 0.0))
        lo, hi = lag
        if lo > hi:
            raise ValueError("lag의 최소값이 최대값보다 큽니다.")
        super().__init__(**data)


class PatchGraph(BaseModel):
    nodes: list[Any] = Field(default_factory=list)
    edges: list[CausalEdge] = Field(default_factory=list)
    is_dag: bool = True
    total_budget: dict[str, tuple[float, float]] = Field(default_factory=dict)
    constraint_status: dict[str, bool] = Field(default_factory=dict)
    proof_status: str = "pending"
    graph_id: str = ""
