from typing import List
from src.interfaces.llm import LLMStrategy
from src.models.types import Task

class MockLLM(LLMStrategy):
    def summarize_thread(self, context: str) -> str:
        """Summarize a conversation thread or log."""
        return "This is a mock summary of the provided context."

    def extract_tasks(self, context: str) -> List[Task]:
        """Extract actionable tasks from a context."""
        return [
            Task(id="mock-task-1", title="Mock Task 1", description="Extracted from context"),
            Task(id="mock-task-2", title="Mock Task 2", description="Another extracted task")
        ]
