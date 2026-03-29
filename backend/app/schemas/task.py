from datetime import datetime

from pydantic import BaseModel

from app.models.models import TaskStatus, UserRole


class TaskCreate(BaseModel):
    title: str
    description: str
    required_role: UserRole
    priority: str = "MEDIUM"


class TaskAssignRequest(BaseModel):
    assignee_id: int | None = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    required_role: UserRole
    status: TaskStatus
    priority: str
    project_id: int
    assignee_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True
