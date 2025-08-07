from fastapi import FastAPI
import os

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

@app.get("/")
def read_root():
    return {"message": "Prediction API"}
