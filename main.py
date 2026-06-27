from fastapi import FastAPI
from routers import auth

app = FastAPI()

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "AI Notes API is running"}