from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Hint(Base):
    __tablename__ = "hints"

    id = Column(Integer, primary_key=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    hint_text = Column(String, nullable=False)
    cost = Column(Integer, default=0)