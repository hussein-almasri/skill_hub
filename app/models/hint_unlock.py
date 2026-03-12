from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class HintUnlock(Base):

    __tablename__ = "hint_unlocks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hint_id = Column(Integer, ForeignKey("hints.id"))