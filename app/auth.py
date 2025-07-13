from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models import fake_users_db
from app.utils import create_access_token, verify_password

auth_router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@auth_router.post("/login")
def login(login_req: LoginRequest):
    user = fake_users_db.get(login_req.username)
    if not user or not verify_password(login_req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user["username"], "group": user["group"]})
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
