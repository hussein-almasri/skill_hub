from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.challenge import Challenge
from app.models.submission import Submission
from app.models.user import User

from app.schemas.submission import SubmissionCreate
from app.core.security import get_current_user

router = APIRouter(prefix="/submissions", tags=["Submissions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def submit_flag(
    submission: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    user = db.query(User).filter(User.id == current_user.id).first()

    challenge = db.query(Challenge).filter(
        Challenge.id == submission.challenge_id
    ).first()

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")


    user_flag = submission.submitted_flag.strip().lower()
    correct_flag = challenge.flag.strip().lower()

    print("USER FLAG:", user_flag)
    print("DB FLAG:", correct_flag)

    is_correct = user_flag == correct_flag

    new_submission = Submission(
        user_id=user.id,
        challenge_id=submission.challenge_id,
        submitted_flag=submission.submitted_flag,
        is_correct=is_correct
    )

    db.add(new_submission)

    if is_correct:
        user.points += challenge.points
        challenge.solved_count += 1

    db.commit()

    return {
        "correct": is_correct,
        "points": user.points,
        "challenge_id": submission.challenge_id
    }