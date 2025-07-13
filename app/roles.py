from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from app.utils import SECRET_KEY, ALGORITHM

def get_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_group(group: str):
    def group_checker(user=Depends(get_user_from_cookie)):
        if user.get("group") != group:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return group_checker