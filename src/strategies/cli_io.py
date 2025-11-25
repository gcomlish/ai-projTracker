from typing import List
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from src.interfaces.io import IOStrategy
from src.models.types import Project

class CliIO(IOStrategy):
    def __init__(self):
        self.console = Console()

    def render_dashboard(self, projects: List[Project]) -> None:
        """Display the project dashboard."""
        table = Table(title="Project Dashboard")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Last Updated", style="yellow")

        for project in projects:
            table.add_row(
                project.id,
                project.name,
                project.status.value,
                project.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            )

        self.console.print(table)

    def get_input(self, prompt: str) -> str:
        """Get input from the user."""
        return Prompt.ask(prompt)
