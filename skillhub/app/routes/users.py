from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserResponse
from app.core.security import get_current_user, get_admin_user

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return db.query(User).all()