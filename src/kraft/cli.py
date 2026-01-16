"""CLI commands for kraft."""

from pathlib import Path
from typing import Annotated

import typer

from kraft.renderer import TemplateRenderer
from kraft.ui import ui
from kraft.validators import validate_service_name

app = typer.Typer(
    name="kraft",
    help="Python service scaffolding with zero learning curve",
)


@app.command()
def version() -> None:
    """Display kraft version."""
    from kraft import __version__

    ui.print(f"[bold blue]kraft[/bold blue] version [green]{__version__}[/green]")


@app.command()
def create(
    name: Annotated[str, typer.Argument(help="Name of the service to create")],
    service_type: Annotated[str, typer.Option("--type", "-t", help="Service type")] = "rest",
    port: Annotated[int, typer.Option("--port", "-p", help="Port number")] = 8000,
    python_version: Annotated[str, typer.Option("--python", help="Python version")] = "3.11",
    with_addons: Annotated[
        list[str] | None, typer.Option("--with", "-w", help="Add-ons to include")
    ] = None,
    no_docker: Annotated[bool, typer.Option("--no-docker", help="Skip Docker files")] = False,
    no_tests: Annotated[bool, typer.Option("--no-tests", help="Skip test files")] = False,
    output_dir: Annotated[
        Path | None, typer.Option("--output", "-o", help="Output directory")
    ] = None,
) -> None:
    """Create a new service from a template."""
    # Validate service name
    validation = validate_service_name(name)
    if not validation.valid:
        ui.error(validation.error or "Invalid service name")
        if validation.suggestion:
            ui.info(f"Suggestion: {validation.suggestion}")
        raise typer.Exit(1)

    # Determine output directory
    target_dir = output_dir or Path.cwd() / name

    if target_dir.exists():
        ui.error(f"Directory '{target_dir}' already exists")
        raise typer.Exit(1)

    # Render template
    renderer = TemplateRenderer()

    # Check if template exists
    template_info = renderer.get_template_info(service_type)
    if not template_info:
        ui.error(f"Unknown service type: {service_type}")
        ui.info("Available types: rest")
        raise typer.Exit(1)

    ui.info(f"Creating {service_type} service '{name}'...")

    variables = {
        "project_name": name,
        "port": port,
        "python_version": python_version,
        "include_docker": not no_docker,
        "include_tests": not no_tests,
    }

    try:
        with ui.progress("Generating project...") as progress:
            task = progress.add_task("Rendering templates...", total=None)
            renderer.render(service_type, target_dir, variables)
            progress.update(task, completed=True)

        ui.success(f"Created service '{name}' at {target_dir}")
        ui.print("")
        ui.print("[bold]Next steps:[/bold]")
        ui.print(f"  cd {name}")
        ui.print("  uv sync --extra dev")
        ui.print(f"  uv run uvicorn {name.replace('-', '_')}.main:app --reload")
        ui.print("")
        ui.print("Or with Docker:")
        ui.print("  docker-compose up --build")

    except Exception as e:
        ui.error(f"Failed to create service: {e}")
        raise typer.Exit(1) from None


@app.command("list")
def list_templates() -> None:
    """List available service templates."""
    renderer = TemplateRenderer()
    templates = renderer.list_templates()

    if not templates:
        ui.info("No templates available")
        return

    ui.table(
        "Available Templates",
        ["Name", "Description", "Version"],
        [[t["name"], t["description"], t["version"]] for t in templates],
    )


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
