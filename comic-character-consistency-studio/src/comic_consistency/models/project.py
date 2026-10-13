"""Project + page contracts and on-disk loader."""
from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from comic_consistency.models.character import CharacterBible, CharacterFingerprint
from comic_consistency.models.panel import PanelSpec


class Page(BaseModel):
    model_config = ConfigDict(frozen=True)

    page_id: str
    panels: list[PanelSpec]


class ComicProject(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    root: Path
    title: str
    pages: list[Page]
    bible: CharacterBible

    @classmethod
    def load(cls, root: Path) -> "ComicProject":
        root = root.resolve()
        manifest = json.loads((root / "project.json").read_text(encoding="utf-8"))
        pages_dir = root / "pages"
        pages: list[Page] = []
        for page_file in sorted(pages_dir.glob("*.json")):
            data = json.loads(page_file.read_text(encoding="utf-8"))
            pages.append(
                Page(
                    page_id=data["page_id"],
                    panels=[PanelSpec(**p) for p in data["panels"]],
                )
            )
        bible = CharacterBible(
            characters=[CharacterFingerprint.stub(c) for c in manifest.get("characters", ["hero_01"])]
        )
        return cls(root=root, title=manifest["title"], pages=pages, bible=bible)

    def page(self, page_id: str) -> Page:
        for page in self.pages:
            if page.page_id == page_id:
                return page
        raise KeyError(f"page '{page_id}' not found")

    def character(self, character_id: str) -> CharacterFingerprint:
        return self.bible.get(character_id)

    def artifact_path(self, page_id: str, panel_id: str) -> Path:
        return self.root / "artifacts" / f"{page_id}__{panel_id}.png"