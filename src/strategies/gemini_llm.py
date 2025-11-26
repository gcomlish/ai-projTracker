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
        self.model = genai.GenerativeModel('gemini-1.5-flash')

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
        
        Output JSON only.
        """
        response = self.model.generate_content(prompt)
        # Clean up code blocks if present
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
            
        return text

    def extract_tasks(self, context: str) -> List[Task]:
        """Extract actionable tasks from a context."""
        prompt = f"""
        Analyze the following text and extract actionable tasks.
        
        Context:
        {context}
        
        Return a JSON list of strings, where each string is a clear, concise task description.
        Example: ["Fix bug in login", "Update documentation"]
        
        Output JSON only.
        """
        response = self.model.generate_content(prompt)
        
        # Clean up code blocks if present
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
            
        try:
            task_strings = json.loads(text)
            tasks = []
            for task_str in task_strings:
                tasks.append(Task(
                    id=str(uuid.uuid4()),
                    title=task_str,
                    description="Extracted from context"
                ))
            return tasks
        except json.JSONDecodeError:
            print(f"Failed to parse JSON from LLM: {text}")
            return []
