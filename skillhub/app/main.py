from fastapi import FastAPI
from app.database import engine, Base
from app.routes import auth, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "SkillHub API Running Successfully"}
app.include_router(auth.router)
app.include_router(users.router)