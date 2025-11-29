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

    def render_project_details(self, project: Project) -> None:
        """Display detailed view of a project."""
        self.console.print(f"\n[bold cyan]Project Details[/bold cyan]")
        self.console.print(f"ID: {project.id}")
        self.console.print(f"Name: [bold magenta]{project.name}[/bold magenta]")
        self.console.print(f"Status: [bold green]{project.status.value}[/bold green]")
        self.console.print(f"Last Updated: {project.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.console.print(f"\n[bold]Summary:[/bold]")
        self.console.print(project.description or "No summary available.")
        
        self.console.print(f"\n[bold]Log History:[/bold]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Timestamp", style="dim")
        table.add_column("Author", style="cyan")
        table.add_column("Content")
        
        for log in project.logs:
            table.add_row(
                log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                log.author,
                log.content
            )
        
        self.console.print(table)

    def get_input(self, prompt: str) -> str:
        """Get input from the user."""
        return Prompt.ask(prompt)
