# CLI 사용 가이드

## 공통 인수

- `--strict`: 엄격 모드
- `--seed`: 결과 재현을 위한 시드 값
- `--verbose`: 상세 로그 출력

## 명령별 동작

- `validate`
  - 입력 파일을 읽고 수동(manual) 또는 합성(synthesis) 모드로 패치를 검사
  - 통과 패치가 없으면 종료 코드 1
- `synthesize`
  - 합성 모드로 여러 패치 생성 후 점수 순 정렬
  - 기본 `max_patches=10`
- `analyze`
  - 합성 모드 + 반사실 분석
  - 기본적으로 반사실 분석을 수행
- `export`
  - 합성 모드로 분석 후 지정 형식 경로 출력
  - `--format json|yaml|html|all`
- `demo`
  - `basic`, `policy`, `scifi` 예제를 실행

예시:

```bash
python3 -m synapse_engine.main synthesize examples/research_design.yaml --max-patches 8 --strict
python3 -m synapse_engine.main export examples/hard_scifi_device.yaml --format all --verbose
```
