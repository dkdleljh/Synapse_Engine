from __future__ import annotations

from ..models.proofs import ProofBundle


def rank_patches(patches: list[ProofBundle], top_n: int = 10) -> list[ProofBundle]:
    ordered = sorted(
        patches,
        key=lambda item: item.patch_score,
        reverse=True,
    )
    return ordered[:top_n]
