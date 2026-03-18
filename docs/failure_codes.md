# 실패 코드(F001~F012)

- F001_CASUAL_LOOP: 인과 루프
- F002_SELF_CAUSATION: 자기인과 간선
- F003_CONSERVATION_VIOLATION: 보존 예산 위반
- F004_ENTROPY_REVERSAL: 엔트로피 역전
- F005_LIGHTCONE_CONFLICT: cone 충돌/무효 참조
- F006_MISSING_CAUSE: 선행 원인 없는 고립 노드
- F007_OBSERVATION_OVER_SENSITIVITY: 민감도 초과
- F008_INFORMATION_BUDGET_EXCEEDED: 정보 예산 초과
- F009_UNSUPPORTED_EVENT_TYPE: 등록되지 않은 이벤트 타입
- F010_INVALID_INPUT_SCHEMA: 입력 스키마 오류
- F011_DECOHERENCE_POLICY_CONFLICT: 정책 충돌(확장 지점)
- F012_EXTERNAL_OUTPUT_POLICY_RISK: 외부 출력 정책 위반

각 실패는 `failure_report.md`와 JSON/YAML 산출물의 `failures` 항목에서 상세 사유, 제안 수정안을 함께 확인할 수 있습니다.
