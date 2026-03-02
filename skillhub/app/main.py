from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, users, challenges, submissions

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(challenges.router)
app.include_router(submissions.router)

@app.get("/")
def root():
    return {"message": "SkillHub API Running Successfully "}


