# 빠른 시작

이 문서는 Synapse Engine의 첫 실행 흐름을 설명합니다.

## 1) 환경 준비

```bash
cd ~/Desktop/Synapse_Engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) 예제 실행

```bash
python3 -m synapse_engine.main demo basic
```

성공/실패 무관하게 `outputs/run_...` 폴더가 생성되어 결과를 확인할 수 있습니다.

## 3) 입력 수정 후 실행

`examples/*.yaml` 중 하나를 복사해 수정하고 아래 명령으로 검증합니다.

```bash
python3 -m synapse_engine.main validate examples/basic_patch.yaml
```

`validate`는 실패 시 종료 코드 1을 반환하여 CI에서 실패를 감지할 수 있습니다.

## 4) 반사실 분석 확인

```bash
python3 -m synapse_engine.main analyze examples/basic_patch.yaml
```

`counterfactual_report.md`, `cause_importance_ranking.json` 파일을 확인합니다.
