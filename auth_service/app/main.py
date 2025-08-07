from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
import datetime

app = FastAPI()

# In-memory user store
users = {}

SECRET_KEY = "mysecret"


class UserCredentials(BaseModel):
    username: str
    password: str


@app.post("/register")
async def register(creds: UserCredentials):
    if creds.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[creds.username] = creds.password
    return {"message": "User registered successfully"}


@app.post("/login")
async def login(creds: UserCredentials):
    if users.get(creds.username) != creds.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {
        "sub": creds.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"token": token}
