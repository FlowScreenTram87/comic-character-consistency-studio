"""Structural protocols adapters must satisfy. Keeps services decoupled."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np
from PIL.Image import Image

from comic_consistency.models.character import CharacterFingerprint


@runtime_checkable
class RenderBackend(Protocol):
    """A diffusion backend that can render a panel and return its embedding."""

    name: str

    def render(
        self,
        prompt: str,
        fingerprint: CharacterFingerprint,
        seed: int,
    ) -> tuple[Image, np.ndarray]:
        ...
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>