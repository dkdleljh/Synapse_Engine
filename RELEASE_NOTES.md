# Synapse Engine 릴리스 노트

## 릴리스: v0.1.0 (MVP 초기 배포)

### 프로젝트 소개

Synapse Engine은 **관측 요약과 목표 함수를 기반으로 후보 시나리오를 평가하고, 패치 후보를 생성·합성·채택 점검하는 CLI 도구**입니다.

교육/게임/훈련/정책 실험은 "정답"보다 "가능성 탐색"이 중요합니다. Synapse Engine은 다양한 시나리오를 분석하고, 그 가능성을 평가하며, 최적의 패치 후보를 생성하는 강력한 도구입니다.

### 핵심 기능

- **입력 파서**: YAML/JSON을 `EngineInput` 스키마로 파싱
- **검증 파이프라인**
  - 인과성/루프 점검
  - 보존 예산(에너지/엔트로피/정보량) 검사
  - 엔트로피 감소 역전 탐지
  - 광원뿔(lightcone) 정합성 검사
  - 관측 민감도 검사
- **패치 생성**
  - 수동 모드(manual): `candidate_scenarios` 그대로 그래프를 구성
  - 합성 모드(synthesis): 이벤트 순차 합성 기반 자동 패치 생성
- **채점 및 판단**
  - PoP proof 객체(`ProofBundle`) 산출
  - 설정 가능한 가중치로 최종 점수 계산
- **반사실 분석**
  - 최소 원인 후보와 실패 케이스 목록 생성
- **산출물**
  - JSON, YAML, Markdown, HTML 보고서
  - 실패 리포트, 위험 레지스터, 실행 요약

### 기술 스택

- **언어**: Python 3.x
- **의존성**: PyYAML, pytest 등 (requirements.txt 참조)

### 폴더 구조

```
Synapse_Engine/
├── src/synapse_engine/
│   ├── compiler/          # 파서, DAG 빌더, 타입 체커
│   ├── counterfactual/    # 반사실 분석 엔진
│   ├── court/            # 판사, 검사, 기록관 모듈
│   ├── models/           # 데이터 모델
│   ├── reporting/        # HTML/JSON/YAML/MD 리포터
│   ├── synthesis/        # 패치 생성 및 순위화
│   ├── validators/       # 유효성 검사기
│   ├── visualization/    # 그래프 및 히트맵 시각화
│   └── main.py           # CLI 진입점
├── tests/                # 테스트 스위트
├── docs/                 # 기술 문서
├── examples/             # 예제 시나리오
└── outputs/              # 실행 결과물 디렉터리
```

### 빠른 시작

```bash
# 가상환경 설정
cd ~/Desktop/Synapse_Engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 도움말 확인
python3 -m synapse_engine.main --help

# 데모 실행
python3 -m synapse_engine.main demo basic
```

### 지원 명령

- `validate <input-file>`
  - 단일 또는 수동 패치 후보의 통과 여부를 먼저 확인
- `synthesize <input-file>`
  - 자동/기본 합성 모드로 패치 후보를 생성 후 채점
- `analyze <input-file>`
  - 반사실 분석까지 함께 생성
- `export <input-file>`
  - 출력물 위치를 생성하고 지정 형식 경로를 표시
- `demo <basic|policy|scifi>`
  - 기본 예제 실행

### 출력물 예시

모든 실행은 `outputs/run_YYYYMMDD_HHMMSS[_seedN]/` 아래에 결과를 남깁니다.

- `patch_bundle.json`
- `patch_program.yaml`
- `proof_of_possibility.md`
- `risk_register.md`
- `failure_report.md`
- `run_summary.md`
- `html_report/index.html`
- `counterfactual_report.md` (analyze에서 생성)

### 추가 문서

- [도입 가이드](docs/quickstart.md)
- [CLI 사용법](docs/cli.md)
- [입력 스키마](docs/input_schema.md)
- [검증 규칙](docs/validation_rules.md)
- [실패 코드](docs/failure_codes.md)
- [보고서 구조](docs/reports.md)
- [테스트 가이드](docs/testing.md)
- [개발 메모](docs/development.md)

### 검증 내역

- Git 상태 검증
  - 브랜치: `main`
  - 원격: `https://github.com/dkdleljh/Synapse_Engine.git`
