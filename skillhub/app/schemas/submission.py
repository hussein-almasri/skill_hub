from pydantic import BaseModel
from datetime import datetime

class SubmissionCreate(BaseModel):
    challenge_id: int
    submitted_flag: str

class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    challenge_id: int
    is_correct: bool
    submitted_at: datetime

    class Config:
        from_attributes = True