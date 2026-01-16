"""Rich console UI wrapper for kraft."""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table


class ConsoleUI:
    """Wrapper for Rich console with consistent styling."""

    def __init__(self) -> None:
        self.console = Console()

    def success(self, message: str) -> None:
        """Display success message with green checkmark."""
        self.console.print(f"[green]✅ {message}[/green]")

    def error(self, message: str) -> None:
        """Display error message with red X."""
        self.console.print(f"[red]❌ {message}[/red]")

    def info(self, message: str) -> None:
        """Display info message with blue icon."""
        self.console.print(f"[blue]ℹ️  {message}[/blue]")

    def warning(self, message: str) -> None:
        """Display warning message with yellow icon."""
        self.console.print(f"[yellow]⚠️  {message}[/yellow]")

    def progress(self, description: str = "Working...") -> Progress:
        """Return a progress context manager with spinner."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        )

    def table(self, title: str, columns: list[str], rows: list[list[str]]) -> None:
        """Display a formatted table."""
        table = Table(title=title)
        for col in columns:
            table.add_column(col, style="cyan")
        for row in rows:
            table.add_row(*row)
        self.console.print(table)

    def print(self, message: str) -> None:
        """Print a plain message."""
        self.console.print(message)


# Global UI instance
ui = ConsoleUI()
