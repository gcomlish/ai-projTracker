from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.types import Project

class StorageStrategy(ABC):
    @abstractmethod
    def upsert_project(self, project: Project) -> None:
        """Create or update a project."""
        pass

    @abstractmethod
    def get_project(self, project_id: str) -> Optional[Project]:
        """Retrieve a project by ID."""
        pass

    @abstractmethod
    def get_stale_projects(self, days_threshold: int = 7) -> List[Project]:
        """Retrieve projects that haven't been updated in a while."""
        pass

    @abstractmethod
    def get_all_active(self) -> List[Project]:
        """Retrieve all active projects."""
        pass
