"""Resolves backend names to concrete render adapters."""
from __future__ import annotations

from comic_consistency.adapters.flux_backend import FluxBackend
from comic_consistency.adapters.sdxl_backend import SDXLBackend
from comic_consistency.models.protocols import RenderBackend


class BackendRegistry:
    """Deterministic name -> adapter mapping with a default fallback."""

    def __init__(self, backends: dict[str, RenderBackend]) -> None:
        if "sdxl" not in backends:
            raise ValueError("registry must include a 'sdxl' backend")
        self._backends = dict(backends)

    @classmethod
    def default(cls) -> "BackendRegistry":
        return cls({"sdxl": SDXLBackend(), "flux": FluxBackend()})

    def get(self, name: str) -> RenderBackend:
        try:
            return self._backends[name]
        except KeyError as exc:
            raise KeyError(f"unknown backend '{name}'; known: {sorted(self._backends)}") from exc

    def names(self) -> list[str]:
        return sorted(self._backends)