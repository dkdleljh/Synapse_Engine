from __future__ import annotations

from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FailureCode(str, Enum):
    F001_CAUSAL_LOOP = "F001_CAUSAL_LOOP"
    F002_SELF_CAUSATION = "F002_SELF_CAUSATION"
    F003_CONSERVATION_VIOLATION = "F003_CONSERVATION_VIOLATION"
    F004_ENTROPY_REVERSAL = "F004_ENTROPY_REVERSAL"
    F005_LIGHTCONE_CONFLICT = "F005_LIGHTCONE_CONFLICT"
    F006_MISSING_CAUSE = "F006_MISSING_CAUSE"
    F007_OBSERVATION_OVER_SENSITIVITY = "F007_OBSERVATION_OVER_SENSITIVITY"
    F008_INFORMATION_BUDGET_EXCEEDED = "F008_INFORMATION_BUDGET_EXCEEDED"
    F009_UNSUPPORTED_EVENT_TYPE = "F009_UNSUPPORTED_EVENT_TYPE"
    F010_INVALID_INPUT_SCHEMA = "F010_INVALID_INPUT_SCHEMA"
    F011_DECOHERENCE_POLICY_CONFLICT = "F011_DECOHERENCE_POLICY_CONFLICT"
    F012_EXTERNAL_OUTPUT_POLICY_RISK = "F012_EXTERNAL_OUTPUT_POLICY_RISK"


FAILURE_CODEBOOK = {
    FailureCode.F001_CAUSAL_LOOP: {
        "title": "인과 루프",
        "technical_description": "네트워크 그래프에서 순환 간선이 발견되어 인과성 위반",
        "human_explanation": "이벤트가 서로를 원인으로 호출해 시간 순서를 해치고 있습니다.",
        "severity": Severity.CRITICAL,
        "remediation_hint": "엣지 방향을 재설계하거나 루프를 제거하세요.",
    },
    FailureCode.F002_SELF_CAUSATION: {
        "title": "자기인과",
        "technical_description": "이벤트가 자기 자신을 대상으로 인과 관계를 가집니다.",
        "human_explanation": "한 이벤트가 자기 자신을 직접 또는 간접적으로 유발할 수 없습니다.",
        "severity": Severity.HIGH,
        "remediation_hint": "source와 target이 동일한 간선을 제거하세요.",
    },
    FailureCode.F003_CONSERVATION_VIOLATION: {
        "title": "보존법칙 위반",
        "technical_description": "에너지/정보/엔트로피 누계가 허용 범위를 벗어났습니다.",
        "human_explanation": "입력/출력 예산 제약을 만족하지 못했습니다.",
        "severity": Severity.HIGH,
        "remediation_hint": "보충 이벤트 추가 또는 기존 이벤트의 delta 범위를 조정하세요.",
    },
    FailureCode.F004_ENTROPY_REVERSAL: {
        "title": "엔트로피 역전",
        "technical_description": "엔트로피가 감소하는 구간이 확인되었습니다.",
        "human_explanation": "시간 진행 방향에서 엔트로피가 낮아져 물리 제약을 위반합니다.",
        "severity": Severity.HIGH,
        "remediation_hint": "순서를 조정하거나 비가역적 손실을 더하는 이벤트를 추가하세요.",
    },
    FailureCode.F005_LIGHTCONE_CONFLICT: {
        "title": "광원뿔/전파 제약 충돌",
        "technical_description": "인과 도달 가능 범위를 벗어난 연결이 존재합니다.",
        "human_explanation": "결과 이벤트가 원인 이벤트의 영향 범위를 벗어났습니다.",
        "severity": Severity.MEDIUM,
        "remediation_hint": "간선 연결의 lag와 cone 관계를 점검하세요.",
    },
    FailureCode.F006_MISSING_CAUSE: {
        "title": "원인 누락",
        "technical_description": "선행 사건이 없는데 결과 이벤트가 존재합니다.",
        "human_explanation": "초기 이벤트로만 시작될 수 없는 노드가 있습니다.",
        "severity": Severity.HIGH,
        "remediation_hint": "원인을 추가하거나 초기 이벤트 조건을 명확히 지정하세요.",
    },
    FailureCode.F007_OBSERVATION_OVER_SENSITIVITY: {
        "title": "관측 민감도 초과",
        "technical_description": "관측 오차 변화가 결과를 크게 흔들립니다.",
        "human_explanation": "입력 오차가 조금만 바뀌어도 결과가 불안정합니다.",
        "severity": Severity.MEDIUM,
        "remediation_hint": "안정성이 높은 이벤트만 선택하거나 감도 임계값을 완화하세요.",
    },
    FailureCode.F008_INFORMATION_BUDGET_EXCEEDED: {
        "title": "정보 예산 초과",
        "technical_description": "정보 누적이 정책 허용 범위를 초과합니다.",
        "human_explanation": "정보 획득/기록량이 너무 큽니다.",
        "severity": Severity.MEDIUM,
        "remediation_hint": "정보 집약형 이벤트 수를 줄이고 압축/필터를 추가하세요.",
    },
    FailureCode.F009_UNSUPPORTED_EVENT_TYPE: {
        "title": "지원되지 않는 이벤트 타입",
        "technical_description": "이벤트 타입 사전에 등록되지 않은 값이 사용됨",
        "human_explanation": "알 수 없는 이벤트 타입입니다.",
        "severity": Severity.HIGH,
        "remediation_hint": "지원 이벤트 타입 목록으로 정리하거나 이벤트 플러그인을 추가하세요.",
    },
    FailureCode.F010_INVALID_INPUT_SCHEMA: {
        "title": "입력 스키마 오류",
        "technical_description": "YAML/JSON 입력이 모델 스키마와 일치하지 않습니다.",
        "human_explanation": "필수 필드가 빠졌거나 값 형식이 잘못되었습니다.",
        "severity": Severity.CRITICAL,
        "remediation_hint": "README와 예제를 기반으로 입력 형식을 보정하세요.",
    },
    FailureCode.F011_DECOHERENCE_POLICY_CONFLICT: {
        "title": "디코히런스 정책 충돌",
        "technical_description": "감쇠/측정 충돌 정책이 동시 활성화되어 모순됩니다.",
        "human_explanation": "동시 측정/차폐 규칙이 충돌할 수 있습니다.",
        "severity": Severity.MEDIUM,
        "remediation_hint": "정책 조합을 완화하거나 정책 중단 구간을 추가하세요.",
    },
    FailureCode.F012_EXTERNAL_OUTPUT_POLICY_RISK: {
        "title": "외부 출력 정책 위험",
        "technical_description": "external_output_zero 정책 하에서 외부 출력을 생성하는 경로가 존재합니다.",
        "human_explanation": "외부 세계와 직접 연결되는 경로가 발견되어 제약을 깨뜨릴 수 있습니다.",
        "severity": Severity.CRITICAL,
        "remediation_hint": "관련 이벤트를 분리하고 외부 출력 경로를 제거하세요.",
    },
}


def build_failure_reason(
    code: FailureCode, component: str, details: str | None = None
) -> "FailureReason":
    meta = FAILURE_CODEBOOK[code]
    severity = meta["severity"]
    severity_value = severity.value if isinstance(severity, Severity) else str(severity)
    return FailureReason(
        code=code.value,
        title=meta["title"],
        technical_description=meta["technical_description"],
        human_explanation=meta["human_explanation"],
        severity=severity_value,
        remediation_hint=meta["remediation_hint"],
        impacted_component=component,
        details=details,
    )


from pydantic import BaseModel


class FailureReason(BaseModel):
    code: str
    title: str
    technical_description: str
    human_explanation: str
    severity: str
    remediation_hint: str
    impacted_component: str
    details: str | None = None
