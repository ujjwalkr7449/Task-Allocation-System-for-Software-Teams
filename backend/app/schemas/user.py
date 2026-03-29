from pydantic import BaseModel, EmailStr

from app.models.models import UserRole


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    skills: str

    class Config:
        from_attributes = True
