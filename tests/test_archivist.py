from synapse_engine.models.proofs import ProofBundle
from synapse_engine.court.archivist import archive


def test_archive_returns_classified_lists() -> None:
    passed = ProofBundle(
        patch_id="p1",
        passed=True,
        feasibility_score=1,
        risk_score=0,
        utility_score=1,
        fragility_score=0,
        documentation_score=1,
    )
    failed = ProofBundle(
        patch_id="p2",
        passed=False,
        feasibility_score=0,
        risk_score=1,
        utility_score=0,
        fragility_score=1,
        documentation_score=0,
    )
    accepted, rejected, risks = archive([passed, failed])
    assert len(accepted) == 1
    assert len(rejected) == 1
    assert risks.items
