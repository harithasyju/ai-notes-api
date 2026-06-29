from fastapi import FastAPI
from app.routers import auth
from app.routers import auth, notes

app = FastAPI()

app.include_router(auth.router)
app.include_router(notes.router)


@app.get("/")
def root():
    return {"message": "AI Notes API is running"}