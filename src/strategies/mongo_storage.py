import os
from typing import List, Optional
from datetime import datetime, timedelta
from pymongo import MongoClient
from src.interfaces.storage import StorageStrategy
from src.models.types import Project, ProjectStatus

class MongoStorage(StorageStrategy):
    def __init__(self):
        mongo_uri = os.environ.get("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set")
        # Add timeout to fail fast if connection is bad
        self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Verify connection immediately
        try:
            self.client.admin.command('ping')
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")
            
        self.db = self.client.get_database()
        self.projects = self.db.projects

    def upsert_project(self, project: Project) -> None:
        """Create or update a project."""
        project_dict = project.model_dump()
        self.projects.update_one(
            {"id": project.id},
            {"$set": project_dict},
            upsert=True
        )

    def get_project(self, project_id: str) -> Optional[Project]:
        """Retrieve a project by ID."""
        data = self.projects.find_one({"id": project_id})
        if data:
            return Project(**data)
        return None

    def get_stale_projects(self, days_threshold: int = 7) -> List[Project]:
        """Retrieve projects that haven't been updated in a while."""
        threshold_date = datetime.now() - timedelta(days=days_threshold)
        cursor = self.projects.find({"updated_at": {"$lt": threshold_date}})
        return [Project(**data) for data in cursor]

    def get_all_active(self) -> List[Project]:
        """Retrieve all active projects."""
        cursor = self.projects.find({"status": ProjectStatus.ACTIVE.value})
        return [Project(**data) for data in cursor]
