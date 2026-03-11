from fastapi import FastAPI
from .database import Base, engine
from .routes import auth, users, challenges, submissions, hints, leaderboard

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(leaderboard.router)
app.include_router(users.router)
app.include_router(challenges.router)
app.include_router(submissions.router)
app.include_router(hints.router)

@app.get("/")
def root():
    return {"message": "SkillHub API Running Successfully"}