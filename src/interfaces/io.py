from abc import ABC, abstractmethod
from typing import List
from src.models.types import Project

class IOStrategy(ABC):
    @abstractmethod
    def render_dashboard(self, projects: List[Project]) -> None:
        """Display the project dashboard."""
        pass

    @abstractmethod
    def render_project_details(self, project: Project) -> None:
        """Display detailed view of a project."""
        pass

    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """Get input from the user."""
        pass
