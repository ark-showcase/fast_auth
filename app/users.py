from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate
from app.utils import get_password_hash
from app.models import fake_users_db, fake_groups_db

users_router = APIRouter()

@users_router.post("/signup")
def signup(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    if user.group not in fake_groups_db:
        raise HTTPException(status_code=400, detail="Invalid group")

    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {
        "username": user.username,
        "password": hashed_password,
        "group": user.group
    }
    fake_groups_db[user.group].append(user.username)
    return {"msg": "User created successfully"}