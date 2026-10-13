"""Desktop GUI handler. Thin wrapper over the same services the CLI uses."""
from __future__ import annotations

import sys
from pathlib import Path

from comic_consistency.services.pipeline_service import PipelineService


def run_studio(project_root: Path) -> int:
    """Launch the studio loop for a given project. Returns exit code."""
    svc = PipelineService()
    # GUI framework binding is injected at build time; this is the entry contract.
    return svc.run_interactive(project_root=project_root)


def main() -> None:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    raise SystemExit(run_studio(root))


if __name__ == "__main__":
    main()