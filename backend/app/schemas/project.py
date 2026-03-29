from datetime import datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str
    requirements_text: str


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str
    requirements_text: str
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True
