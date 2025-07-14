from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from app.utils import SECRET_KEY, ALGORITHM
from app.models import SessionLocal, RoutePermission
import time
import logging

logger = logging.getLogger("uvicorn")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = round(time.time() - start_time, 4)
        logger.info(f"{request.method} {request.url.path} completed in {duration}s")
        return response

class RoleBasedAccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db = SessionLocal()
        try:
            path = request.url.path
            permission = db.query(RoutePermission).filter_by(path=path).first()
            if permission:
                token = request.cookies.get("access_token")
                if not token:
                    raise HTTPException(status_code=401, detail="Unauthorized")
                try:
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    user_role = payload.get("group")
                    if user_role != permission.required_role:
                        raise HTTPException(status_code=403, detail="Forbidden")
                except JWTError:
                    raise HTTPException(status_code=401, detail="Invalid token")
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )
        finally:
            db.close()

        return await call_next(request)