from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models.challenge import Challenge
from ..models.user import User
from ..models.submission import Submission
from ..schemas.challenge import ChallengeCreate, ChallengeResponse, ChallengeUpdate
from ..core.security import get_current_user, get_admin_user

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

    challenges = db.query(Challenge).all()

    result = []

    for challenge in challenges:

        solved_count = db.query(Submission).filter(
            Submission.challenge_id == challenge.id,
            Submission.is_correct == True
        ).count()

        challenge_data = challenge.__dict__.copy()
        challenge_data["solved_count"] = solved_count

        result.append(challenge_data)

    return result


@router.get("/{challenge_id}", response_model=ChallengeResponse)
def get_challenge(challenge_id: int, db: Session = Depends(get_db)):

    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id
    ).first()

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    solved_count = db.query(Submission).filter(
        Submission.challenge_id == challenge.id,
        Submission.is_correct == True
    ).count()

    challenge_data = challenge.__dict__.copy()
    challenge_data["solved_count"] = solved_count

    return challenge_data


@router.put("/{challenge_id}")
def update_challenge(
    challenge_id: int,
    challenge: ChallengeUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):

    db_challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id
    ).first()

    if not db_challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    for key, value in challenge.dict(exclude_unset=True).items():
        setattr(db_challenge, key, value)

    db.commit()
    db.refresh(db_challenge)

    return db_challenge


@router.delete("/{challenge_id}")
def delete_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):

    db_challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id
    ).first()

    if not db_challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    db.delete(db_challenge)
    db.commit()

    return {"message": "Challenge deleted"}