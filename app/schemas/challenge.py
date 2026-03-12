from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChallengeBase(BaseModel):
    title: str
    description: str
    difficulty: str
    points: int
    category: str


class ChallengeCreate(ChallengeBase):
    flag: str


class ChallengeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    points: Optional[int] = None
    category: Optional[str] = None


class ChallengeResponse(ChallengeBase):
    id: int
    status: str
    created_by: int
    created_at: datetime
    solved_count: int

    class Config:
        from_attributes = True