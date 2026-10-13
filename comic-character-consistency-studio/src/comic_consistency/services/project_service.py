"""Scaffolds and migrates .ccstudio project trees."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from comic_consistency.models.character import CharacterBible, CharacterFingerprint
from comic_consistency.utils.paths import safe_join

STARTER_BIBLE = {
    "characters": [
        {
            "character_id": "hero_01",
            "display_name": "Sample Hero",
            "anchors": ["scar over left brow", "copper hair, chin-length"],
            "palette": ["#c96f4a", "#2b3a52", "#e8d9c5"],
        }
    ]
}


@dataclass(frozen=True, slots=True)
class ScaffoldResult:
    root: Path
    title: str


class ProjectService:
    """Creates the on-disk layout a comic project expects."""

    def scaffold(self, directory: Path, title: str) -> ScaffoldResult:
        root = directory.resolve()
        safe_join(root, "characters").mkdir(parents=True, exist_ok=True)
        safe_join(root, "pages").mkdir(parents=True, exist_ok=True)
        safe_join(root, "artifacts").mkdir(parents=True, exist_ok=True)

        manifest = {"schema": 1, "title": title, "version": "0.6.3"}
        safe_join(root, "project.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )
        safe_join(root, "characters", "bible.yaml").write_text(
            json.dumps(STARTER_BIBLE, indent=2), encoding="utf-8"
        )
        return ScaffoldResult(root=root, title=title)

    def load_bible(self, project_root: Path) -> CharacterBible:
        path = safe_join(project_root, "characters", "bible.yaml")
        import yaml

        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        fingerprints = [
            CharacterFingerprint.stub(entry["character_id"])
            for entry in raw.get("characters", [])
        ]
        return CharacterBible(characters=fingerprints)