from abc import ABC, abstractmethod
from typing import List
from src.models.types import Task

class LLMStrategy(ABC):
    @abstractmethod
    def summarize_thread(self, context: str) -> str:
        """Summarize a conversation thread or log."""
        pass

    @abstractmethod
    def extract_tasks(self, context: str) -> List[Task]:
        """Extract actionable tasks from a context."""
        pass
