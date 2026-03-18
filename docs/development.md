# 개발 노트

## 구현 레이어

- `compiler`: 입력 파싱 및 DAG 구성
- `validators`: 물리/인과 제약 검사
- `synthesis`: 수동/합성 패치 구성
- `court`: prosecutor(실패 후보 수집), judge(채점), archivist(채택/거부 분리)
- `counterfactual`: 최소 원인 후보 추정
- `reporting`: JSON/YAML/Markdown/HTML 산출
- `cli`: validate/synthesize/analyze/export/demo 명령

## 실행 흐름

1. `validate/synthesize/analyze/export`에서 입력 파싱
2. 수동 또는 합성 모드로 `ProofBundle` 생성
3. 정렬/필터 후 리포트 생성
4. counterfactual 분석은 `analyze`에서만 기본 활성화

## 확장 포인트

- 판별 규칙 추가: `court/prosecutor.py`
- 점수 가중치 조정: `solver_config`와 `ProofBundle.scoring_weights`
- 새로운 리포트 포맷: `reporting/*_reporter.py`
