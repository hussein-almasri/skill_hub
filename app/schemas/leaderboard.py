from pydantic import BaseModel


class LeaderboardEntry(BaseModel):

    username: str
    points: int