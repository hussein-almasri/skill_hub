from pydantic import BaseModel
from datetime import datetime


class ChallengeBase(BaseModel):
    title: str
    description: str
    difficulty: str
    points: int
    category: str
    flag: str


class ChallengeCreate(ChallengeBase):
    pass


class ChallengeResponse(ChallengeBase):
    id: int
    status: str
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True  