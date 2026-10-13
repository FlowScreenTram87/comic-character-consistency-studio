"""Character bible + fingerprint contracts."""
from __future__ import annotations

import hashlib

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

EMBED_DIM: int = 128


class CharacterFingerprint(BaseModel):
    """A character's identity vector plus a revision hash of the bible."""

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    character_id: str
    embedding: np.ndarray = Field(description=f"L2-normalized float32[{EMBED_DIM}]")
    bible_revision: str

    @classmethod
    def stub(cls, character_id: str, seed: int = 6767) -> "CharacterFingerprint":
        rng = np.random.default_rng(seed + hash(character_id) % 10_000)
        vec = rng.standard_normal(EMBED_DIM, dtype=np.float32)
        vec /= np.linalg.norm(vec)
        revision = hashlib.sha256(character_id.encode()).hexdigest()[:12]
        return cls(character_id=character_id, embedding=vec, bible_revision=revision)


class CharacterBible(BaseModel):
    characters: list[CharacterFingerprint]

    def get(self, character_id: str) -> CharacterFingerprint:
        for fp in self.characters:
            if fp.character_id == character_id:
                return fp
        raise KeyError(f"character '{character_id}' not in bible")