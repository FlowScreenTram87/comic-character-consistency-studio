"""Locks character identity across panels via embedding drift checks.

Given a CharacterFingerprint and a candidate panel embedding, this service
decides whether the panel preserves identity within tolerance. It is the
single source of truth for the "same character, different pose" contract.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from comic_consistency.models.character import CharacterFingerprint

IDENTITY_DRIFT_TOLERANCE: float = 0.085


@dataclass(frozen=True, slots=True)
class DriftVerdict:
    panel_id: str
    character_id: str
    drift: float
    accepted: bool


class IdentityLockService:
    """Cosine-drift gate for character consistency across panels."""

    def __init__(self, tolerance: float = IDENTITY_DRIFT_TOLERANCE) -> None:
        if not 0.0 < tolerance < 1.0:
            raise ValueError("tolerance must be in (0, 1)")
        self._tolerance = tolerance

    def score(
        self,
        panel_id: str,
        fingerprint: CharacterFingerprint,
        candidate: np.ndarray,
    ) -> DriftVerdict:
        if candidate.shape != fingerprint.embedding.shape:
            raise ValueError(
                f"shape mismatch: fingerprint {fingerprint.embedding.shape} "
                f"vs candidate {candidate.shape}"
            )
        drift = self._cosine_drift(fingerprint.embedding, candidate)
        return DriftVerdict(
            panel_id=panel_id,
            character_id=fingerprint.character_id,
            drift=drift,
            accepted=drift <= self._tolerance,
        )

    @staticmethod
    def _cosine_drift(a: np.ndarray, b: np.ndarray) -> float:
        denom = float(np.linalg.norm(a) * np.linalg.norm(b))
        if denom == 0.0:
            return math.inf
        cosine = float(np.dot(a, b) / denom)
        return 1.0 - max(-1.0, min(1.0, cosine))