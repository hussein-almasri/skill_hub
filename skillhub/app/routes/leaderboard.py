from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import SessionLocal
from ..models.user import User
from ..models.challenge import Challenge
from ..models.submission import Submission
from ..schemas.leaderboard import LeaderboardEntry

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):

    users = (
        db.query(User)
        .order_by(User.points.desc())
        .all()
    )

    return users