from enum import Enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class ProjectStatus(str, Enum):
    ACTIVE = "ACTIVE"
    WARNING = "WARNING"
    STALE = "STALE"
    ARCHIVED = "ARCHIVED"

class LogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    content: str
    author: str = "System"

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

class Project(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.ACTIVE
    logs: List[LogEntry] = Field(default_factory=list)
    tasks: List[Task] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
