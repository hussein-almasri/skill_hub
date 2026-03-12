from pydantic import BaseModel, EmailStr
from typing import Optional

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    points: int = 0


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


class UserStats(BaseModel):
    username: str
    email: str
    points: int
    solved_challenges: int

    class Config:
        from_attributes = True