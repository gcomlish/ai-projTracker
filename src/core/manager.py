from datetime import datetime, timedelta
import uuid
from typing import Optional

from src.interfaces.storage import StorageStrategy
from src.interfaces.llm import LLMStrategy
from src.interfaces.io import IOStrategy
from src.models.types import Project, ProjectStatus, LogEntry

class ProjectManager:
    def __init__(
        self,
        storage: StorageStrategy,
        llm: LLMStrategy,
        io: IOStrategy
    ):
        self.storage = storage
        self.llm = llm
        self.io = io

    def check_stale_projects(self) -> None:
        """Check for stale projects and update their status."""
        active_projects = self.storage.get_all_active()
        now = datetime.now()
        
        for project in active_projects:
            days_since_update = (now - project.updated_at).days
            
            new_status = project.status
            if days_since_update > 7:
                new_status = ProjectStatus.STALE
            elif days_since_update > 3:
                new_status = ProjectStatus.WARNING
            
            if new_status != project.status:
                project.status = new_status
                self.storage.upsert_project(project)

    def add_log(self, project_name_or_id: str, text: str) -> None:
        """Add a log entry to a project and update its summary."""
        # Try to find by ID first
        project = self.storage.get_project(project_name_or_id)
        
        # If not found, create new project (assuming input is name)
        if not project:
            # Check if it might be a name search - for now, just create new
            # In a real app, we might search by name, but interface only has get_project(id)
            # Let's assume for this prompt that if ID lookup fails, we create a new project with that name
            project = Project(
                id=str(uuid.uuid4()),
                name=project_name_or_id,
                description="New project"
            )

        # Add log entry
        log_entry = LogEntry(content=text)
        project.logs.append(log_entry)
        
        # Rolling Summary Strategy
        # Combine current description (summary) with new log
        context = f"Current Summary: {project.description}\n\nNew Log: {text}"
        new_summary = self.llm.summarize_thread(context)
        project.description = new_summary
        
        # Update timestamp and persist
        project.updated_at = datetime.now()
        # Ensure status is active if it was stale
        if project.status in [ProjectStatus.STALE, ProjectStatus.WARNING]:
            project.status = ProjectStatus.ACTIVE
            
        self.storage.upsert_project(project)

    def daily_briefing(self) -> None:
        """Run daily maintenance and show dashboard."""
        self.check_stale_projects()
        active_projects = self.storage.get_all_active()
        self.io.render_dashboard(active_projects)

    def view_project(self, project_name_or_id: str) -> None:
        """View detailed status and logs of a project."""
        project = self.storage.get_project(project_name_or_id)
        if not project:
            # Try finding by name if ID lookup fails
            all_active = self.storage.get_all_active()
            matches = [p for p in all_active if p.name == project_name_or_id]
            
            if matches:
                # Sort by updated_at descending to get the most recent one
                matches.sort(key=lambda p: p.updated_at, reverse=True)
                project = matches[0]
                if len(matches) > 1:
                    print(f"Note: Found {len(matches)} projects with name '{project_name_or_id}'. Showing the most recent one (ID: {project.id}).")
        
        if project:
            self.io.render_project_details(project)
        else:
            print(f"Project '{project_name_or_id}' not found.")
