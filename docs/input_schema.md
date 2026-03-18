# 입력 스키마

현재 엔진은 아래 구조를 `EngineInput`으로 사용합니다.

## 최상위 필드

- `observation_summary`
  - `relations`: 문자열 목록
  - `bounds`: 에너지/엔트로피/정보 경계치
  - `uncertainties`: 민감도 계산에 쓰이는 관측 불확실성
- `goal_function`
  - `primary`: 최우선 목표
  - `secondary`: 보조 목표 목록
- `domain_policy`
  - `no_causal_loop`: 인과 순환 허용 여부
  - `entropy_non_decrease`: 엔트로피 비감소 정책
  - `local_conservation`: 지역 보존 정책
  - `external_output_zero`: 외부 출력 경로 금지 여부
  - `sensitivity_threshold`: 민감도 임계치
- `candidate_scenarios`: 후보 시나리오 배열
- `solver_config`: 채점 가중치/동작 옵션

## 시나리오/이벤트

`candidate_scenarios`는 다음을 가집니다.

- `id`: 문자열 ID
- `events`: 이벤트 목록
- `edges`: 이벤트 간 인과 간선

이벤트의 핵심 값:

- `id`, `type`, `delta_e`, `delta_s`, `delta_i`
- `cone`: local / regional / global

간선의 핵심 값:

- `source`, `target`
- `lag`: 최소/최대 지연
- `relation_type`, `confidence`, `justification`
