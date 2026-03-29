from pydantic import BaseModel, EmailStr

from app.models.models import UserRole


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole
    skills: str = ""


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
