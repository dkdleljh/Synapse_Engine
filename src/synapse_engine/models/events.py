from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class EventType(str, Enum):
    ENERGY_INJECTION = "EnergyInjection"
    HEAT_DISSIPATION = "HeatDissipation"
    RECORD = "Record"
    ERASE = "Erase"
    MEASURE = "Measure"
    SIGNAL_TRANSMIT = "SignalTransmit"
    MOMENTUM_TRANSFER = "MomentumTransfer"
    MATERIAL_RECONFIGURATION = "MaterialReconfiguration"
    TRIGGER = "Trigger"
    FEEDBACK = "Feedback"
    GATE = "Gate"
    STABILIZE = "Stabilize"
    ISOLATE = "Isolate"
    SEAL = "Seal"
    FILTER = "Filter"
    TERMINATE = "Terminate"


Interval = tuple[float, float]


class EventNode(BaseModel):
    id: str
    name: str
    event_type: EventType
    delta_e_range: Interval
    delta_s_range: Interval
    delta_i_range: Interval
    cone: str
    preconditions: list[str] = Field(default_factory=list)
    postconditions: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)

    @field_validator("delta_e_range", "delta_s_range", "delta_i_range")
    @classmethod
    def normalize_interval(cls, value: Interval) -> Interval:
        lo, hi = value
        if lo > hi:
            raise ValueError("범위의 최소값이 최대값보다 큽니다.")
        return float(lo), float(hi)
