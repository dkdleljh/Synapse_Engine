# 산출물 설명

명령 실행 시 기본적으로 다음 파일이 생성됩니다.

- `patch_bundle.json`
  - 전체 `ProofBundle` 목록
- `patch_program.yaml`
  - 동일 내용 YAML 직렬화
- `proof_of_possibility.md`
  - 최고 통과/최상위 패치 증명 요약
- `risk_register.md`
  - 위험 레지스터 항목
- `failure_report.md`
  - 통과하지 못한 패치들의 실패 코드 목록
- `run_summary.md`
  - 통과/실패 카운트 및 점수 요약
- `html_report/index.html`
  - 패치 및 리스크 요약 HTML

`analyze` 실행 시 추가로 생성되는 파일

- `counterfactual_report.md`
- `cause_importance_ranking.json`

## 점수 체계

`ProofBundle` 점수는 아래 형식으로 계산됩니다.

`score = w_f * feasibility + w_r * risk + w_u * utility + w_fa * fragility`

`w_*` 값은 `solver_config`에서 조정할 수 있으며 기본값은 `0.35, -0.20, 0.25, -0.20`입니다.
