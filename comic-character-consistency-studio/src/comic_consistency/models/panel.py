"""Panel-level contracts."""
from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class PanelSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    panel_id: str
    index: int = Field(ge=0)
    character_id: str
    prompt: str
    camera: str = "medium"


class PanelResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    panel_id: str
    character_id: str
    identity_drift: float
    artifact_path: Path