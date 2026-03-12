from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models.hint import Hint
from ..models.user import User
from ..models.hint_unlock import HintUnlock

from ..schemas.hint import HintCreate, HintResponse
from ..core.security import get_admin_user, get_current_user

router = APIRouter(prefix="/hints", tags=["Hints"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/unlock/{hint_id}")
def unlock_hint(
    hint_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    user = db.query(User).filter(User.id == current_user.id).first()

    hint = db.query(Hint).filter(Hint.id == hint_id).first()

    if not hint:
        raise HTTPException(status_code=404, detail="Hint not found")

    already = db.query(HintUnlock).filter(
        HintUnlock.user_id == user.id,
        HintUnlock.hint_id == hint_id
    ).first()

    if already:
        return {
            "hint_text": hint.hint_text,
            "message": "Already unlocked"
        }

    if user.points < hint.cost:
        raise HTTPException(status_code=400, detail="Not enough points")

    user.points -= hint.cost

    unlock = HintUnlock(
        user_id=user.id,
        hint_id=hint_id
    )

    db.add(unlock)

    db.commit()

    return {
        "hint_text": hint.hint_text
    }


@router.get("/{challenge_id}")
def get_hints(
    challenge_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    hints = db.query(Hint).filter(
        Hint.challenge_id == challenge_id
    ).all()

    result = []

    for hint in hints:

        unlocked = db.query(HintUnlock).filter(
            HintUnlock.user_id == user.id,
            HintUnlock.hint_id == hint.id
        ).first()

        result.append({
            "id": hint.id,
            "hint_text": hint.hint_text if unlocked else None,
            "cost": hint.cost,
            "unlocked": unlocked is not None
        })

    return result


@router.post("/{challenge_id}")
def create_hint(
    challenge_id: int,
    hint: HintCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):

    new_hint = Hint(
        challenge_id=challenge_id,
        hint_text=hint.hint_text,
        cost=hint.cost
    )

    db.add(new_hint)
    db.commit()

    return {"message": "Hint created"}