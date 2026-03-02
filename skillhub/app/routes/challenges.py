from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.models.challenge import Challenge
from app.models.user import User
from app.schemas.challenge import ChallengeCreate, ChallengeResponse
from app.core.security import get_current_user, get_admin_user

router = APIRouter(prefix="/challenges", tags=["Challenges"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ChallengeResponse)
def create_challenge(
    challenge: ChallengeCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    new_challenge = Challenge(
        title=challenge.title,
        description=challenge.description,
        difficulty=challenge.difficulty,
        points=challenge.points,
        category=challenge.category,
        flag=challenge.flag,          
        created_by=admin.id
    )

    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)

    return new_challenge


@router.get("/", response_model=List[ChallengeResponse])
def get_challenges(db: Session = Depends(get_db)):
    return db.query(Challenge).all()


@router.get("/{challenge_id}", response_model=ChallengeResponse)
def get_challenge(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    return challenge