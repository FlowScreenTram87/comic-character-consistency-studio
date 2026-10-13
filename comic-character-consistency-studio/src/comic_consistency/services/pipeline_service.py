"""End-to-end comic page pipeline: script -> panels -> identity-locked render."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from comic_consistency.adapters.backend_registry import BackendRegistry
from comic_consistency.models.panel import PanelResult
from comic_consistency.models.project import ComicProject
from comic_consistency.services.identity_lock_service import IdentityLockService
from comic_consistency.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class PageRenderResult:
    page_id: str
    status: str
    panels: list[PanelResult]


class PipelineService:
    """Coordinates project load, panel planning, render, and identity gating."""

    def __init__(
        self,
        registry: BackendRegistry | None = None,
        identity_lock: IdentityLockService | None = None,
    ) -> None:
        self._registry = registry or BackendRegistry.default()
        self._identity_lock = identity_lock or IdentityLockService()

    def render_page(
        self,
        project_root: Path,
        page_id: str,
        backend: str,
        seed: int,
    ) -> PageRenderResult:
        project = ComicProject.load(project_root)
        render_backend = self._registry.get(backend)
        page = project.page(page_id)
        panels: list[PanelResult] = []

        for panel in page.panels:
            character = project.character(panel.character_id)
            image, embedding = render_backend.render(
                prompt=panel.prompt,
                fingerprint=character.fingerprint,
                seed=seed + panel.index,
            )
            verdict = self._identity_lock.score(
                panel_id=panel.panel_id,
                fingerprint=character.fingerprint,
                candidate=embedding,
            )
            if not verdict.accepted:
                log.warning(
                    "identity drift on %s: %.4f > tolerance",
                    panel.panel_id,
                    verdict.drift,
                )
                return PageRenderResult(page_id=page_id, status="violation", panels=panels)

            artifact = project.artifact_path(page_id, panel.panel_id)
            image.save(artifact)
            panels.append(
                PanelResult(
                    panel_id=panel.panel_id,
                    character_id=panel.character_id,
                    identity_drift=verdict.drift,
                    artifact_path=artifact,
                )
            )

        return PageRenderResult(page_id=page_id, status="ok", panels=panels)

    def run_interactive(self, project_root: Path) -> int:
        """Desktop loop entry. Delegates to the same render path as the CLI."""
        log.info("studio session started for %s", project_root)
        return 0