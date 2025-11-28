import os
import json
import uuid
from typing import List
import google.generativeai as genai
from src.interfaces.llm import LLMStrategy
from src.models.types import Task

class GeminiLLM(LLMStrategy):
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def summarize_thread(self, context: str) -> str:
        """Summarize a conversation thread or log."""
        prompt = f"""
        You are an expert Project Manager. Your goal is to synthesize the following project history into a concise, actionable summary.
        
        Context:
        {context}
        
        Please provide a structured JSON response with the following keys:
        - summary: A concise narrative summary of the project status.
        - next_steps: A list of immediate next steps.
        - estimated_completion: A brief string estimating when the current phase might be done.
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return response.text
        except Exception as e:
            print(f"Error generating summary: {e}")
            # Fallback to a basic JSON if generation fails
            return json.dumps({
                "summary": "Error generating summary.",
                "next_steps": [],
                "estimated_completion": "Unknown"
            })

    def extract_tasks(self, context: str) -> List[Task]:
        """Extract actionable tasks from a context."""
        prompt = f"""
        Analyze the following text and extract actionable tasks.
        
        Context:
        {context}
        
        Return a JSON list of strings, where each string is a clear, concise task description.
        Example: ["Fix bug in login", "Update documentation"]
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            text = response.text
            task_strings = json.loads(text)
            
            # Handle case where LLM might return a dict instead of list
            if isinstance(task_strings, dict) and "tasks" in task_strings:
                task_strings = task_strings["tasks"]
            
            tasks = []
            if isinstance(task_strings, list):
                for task_str in task_strings:
                    if isinstance(task_str, str):
                        tasks.append(Task(
                            id=str(uuid.uuid4()),
                            title=task_str,
                            description="Extracted from context"
                        ))
            return tasks
        except Exception as e:
            print(f"Error extracting tasks: {e}")
            return []
