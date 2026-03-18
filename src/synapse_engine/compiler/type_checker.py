from __future__ import annotations

from ..models.events import EventType
from ..models.failures import FailureCode
from ..models.schema import CandidateScenario, EngineInput


def validate_event_type(value: str) -> bool:
    return value in {v.value for v in EventType}


def validate_scenario_types(scenario: CandidateScenario) -> list[FailureCode]:
    codes: list[FailureCode] = []
    for ev in scenario.events:
        if not validate_event_type(ev.type):
            codes.append(FailureCode.F009_UNSUPPORTED_EVENT_TYPE)
    return codes


def validate_input_types(payload: EngineInput) -> list[FailureCode]:
    failures: list[FailureCode] = []
    for scenario in payload.candidate_scenarios:
        failures.extend(validate_scenario_types(scenario))
    return failures
