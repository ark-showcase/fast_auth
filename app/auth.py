from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models import SessionLocal, Users
from app.utils import create_access_token, verify_password
from sqlalchemy.orm import Session

auth_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginRequest(BaseModel):
    username: str
    password: str

@auth_router.post("/login")
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Users).filter_by(username=login_req.username).first()
    if not user or not verify_password(login_req.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username, "group": user.group})
    response = JSONResponse(content={"msg": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=1800,
    )
    return response

@auth_router.post("/logout")
def logout():
    response = JSONResponse(content={"msg": "Logged out"})
    response.delete_cookie("access_token")
    return response
