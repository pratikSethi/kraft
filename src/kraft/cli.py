"""CLI commands for kraft."""

import typer
from rich.console import Console

app = typer.Typer(
    name="kraft",
    help="Python service scaffolding with zero learning curve",
)
console = Console()


@app.command()
def version() -> None:
    """Display kraft version."""
    from kraft import __version__

    console.print(f"[bold blue]kraft[/bold blue] version [green]{__version__}[/green]")


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
