from fastapi import APIRouter, HTTPException, Depends
from app.schemas import UserCreate
from app.utils import get_password_hash
from app.models import SessionLocal, Users, UserGroups
from sqlalchemy.orm import Session

users_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)

    existing_user_by_requested_username = db.query(Users).filter_by(username=user.username).first()
    if existing_user_by_requested_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    requested_user_group = db.query(UserGroups).filter_by(title=user.group).all()
    if not requested_user_group:
        raise HTTPException(status_code=400, detail="Invalid group")

    new_user = Users(username=user.username, password=hashed_password, group=user.group)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User created successfully"}