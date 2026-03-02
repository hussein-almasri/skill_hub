from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.submission import Submission
from app.models.challenge import Challenge
from app.models.user import User
from app.schemas.submission import SubmissionCreate, SubmissionResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.post("/", response_model=SubmissionResponse)
def submit_flag(
    data: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # نعيد جلب المستخدم من نفس الـ session
    user = db.query(User).filter(User.id == current_user.id).first()

    challenge = db.query(Challenge).filter(
        Challenge.id == data.challenge_id
    ).first()

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    existing = db.query(Submission).filter(
        Submission.user_id == user.id,
        Submission.challenge_id == data.challenge_id,
        Submission.is_correct == True
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already solved")

    is_correct = data.submitted_flag == challenge.flag

    submission = Submission(
        user_id=user.id,
        challenge_id=data.challenge_id,
        submitted_flag=data.submitted_flag,
        is_correct=is_correct
    )

    db.add(submission)

    if is_correct:
        user.points += challenge.points

    db.commit()
    db.refresh(submission)

    return submission