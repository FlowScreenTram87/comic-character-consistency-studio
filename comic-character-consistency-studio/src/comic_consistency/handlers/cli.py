"""CLI handler. Parses args, delegates to services, prints a rich table."""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from comic_consistency.services.pipeline_service import PipelineService
from comic_consistency.services.project_service import ProjectService

app = typer.Typer(
    name="ccs",
    help="AI consistent-character comic generator (CLI).",
    no_args_is_help=True,
)
console = Console()


@app.command("init")
def init_project(
    directory: Path = typer.Argument(..., help="Where to scaffold the comic project."),
    title: str = typer.Option("Untitled Series", "--title", "-t"),
) -> None:
    """Scaffold a new .ccstudio project with a starter character bible."""
    svc = ProjectService()
    project = svc.scaffold(directory=directory, title=title)
    console.print(f"[green]scaffolded[/] {project.root}")


@app.command("render")
def render_page(
    project: Path = typer.Argument(..., exists=True, file_okay=False),
    page_id: str = typer.Option(..., "--page", "-p"),
    backend: str = typer.Option("sdxl", "--backend", "-b"),
    seed: int = typer.Option(6767, "--seed"),
) -> None:
    """Render a single comic page with identity locking enabled."""
    svc = PipelineService()
    result = svc.render_page(project_root=project, page_id=page_id, backend=backend, seed=seed)
    table = Table(title=f"page {page_id} — {result.status}")
    table.add_column("panel")
    table.add_column("character")
    table.add_column("drift")
    table.add_column("artifact")
    for panel in result.panels:
        table.add_row(
            panel.panel_id,
            panel.character_id,
            f"{panel.identity_drift:.4f}",
            str(panel.artifact_path),
        )
    console.print(table)


def main() -> None:
    app()


if __name__ == "__main__":
    main()