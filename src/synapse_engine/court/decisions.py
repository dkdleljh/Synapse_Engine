from __future__ import annotations

from dataclasses import dataclass

from ..models.proofs import ProofBundle


@dataclass
class Decision:
    passed: bool
    proof: ProofBundle
