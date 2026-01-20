"""CLI commands for kraft."""

from pathlib import Path
from typing import Annotated

import typer

from kraft.renderer import TemplateRenderer
from kraft.ui import ui
from kraft.validators import validate_service_name


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        from kraft import __version__

        typer.echo(f"kraft {__version__}")
        raise typer.Exit()


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

        # Apply add-ons if specified
        if with_addons:
            from kraft.addon_manager import AddOnManager

            manager = AddOnManager()
            for addon_name in with_addons:
                ui.info(f"Applying add-on '{addon_name}'...")
                manager.apply_addon(addon_name, target_dir)

        ui.success(f"Created service '{name}' at {target_dir.resolve()}")
        ui.print("")
        ui.print("[bold]Next steps:[/bold]")
        ui.print(f"  cd {target_dir.resolve()}")
        ui.print("  uv sync --extra dev")
        ui.print(f"  uv run uvicorn {name.replace('-', '_')}.main:app --reload")
        ui.print("")
        ui.print("Or with Docker:")
        ui.print(f"  cd {target_dir.resolve()}")
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


@app.command()
def addons() -> None:
    """List available add-ons."""
    from kraft.addon_manager import AddOnManager

    manager = AddOnManager()
    addon_list = manager.list_addons()

    if not addon_list:
        ui.info("No add-ons available")
        return

    ui.table(
        "Available Add-ons",
        ["Name", "Description", "Dependencies"],
        [[a["name"], a["description"], ", ".join(a["dependencies"][:2])] for a in addon_list],
    )


@app.command()
def add(
    addon_names: Annotated[list[str], typer.Argument(help="Add-on(s) to apply")],
    project_dir: Annotated[
        Path | None, typer.Option("--dir", "-d", help="Project directory")
    ] = None,
) -> None:
    """Add one or more add-ons to an existing kraft project."""
    from kraft.addon_manager import AddOnManager

    target_dir = project_dir or Path.cwd()

    # Validate project
    if not (target_dir / ".kraft.yml").exists():
        ui.error(f"'{target_dir}' is not a kraft project (missing .kraft.yml)")
        ui.info("Run 'kraft create' first to create a project")
        raise typer.Exit(1)

    manager = AddOnManager()

    for addon_name in addon_names:
        # Check if add-on exists
        addon_info = manager.get_addon_info(addon_name)
        if not addon_info:
            ui.error(f"Unknown add-on: {addon_name}")
            available = [a["name"] for a in manager.list_addons()]
            if available:
                ui.info(f"Available add-ons: {', '.join(available)}")
            raise typer.Exit(1)

        ui.info(f"Applying add-on '{addon_name}'...")

        try:
            manager.apply_addon(addon_name, target_dir)
            ui.success(f"Applied add-on '{addon_name}'")
        except Exception as e:
            ui.error(f"Failed to apply add-on: {e}")
            raise typer.Exit(1) from None

    ui.print("")
    ui.print("[bold]Next steps:[/bold]")
    ui.print("  uv sync  # Install new dependencies")
    ui.print("  docker-compose up -d  # Start services")


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version", "-V",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit",
        ),
    ] = None,
) -> None:
    """Python service scaffolding with zero learning curve."""
    pass


def cli() -> None:
    """CLI entry point."""
    app()


if __name__ == "__main__":
    main()
