from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.auth import auth_router
from app.roles import get_user_from_cookie, require_group
from app.users import users_router
from app.middleware import LoggingMiddleware, RoleBasedAccessMiddleware
from app.models import Base, engine, SessionLocal, RoutePermission
from app.admin import admin_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Initial route permissions seed
def seed_permissions():
    db = SessionLocal()
    try:
        existing = db.query(RoutePermission).all()
        if not existing:
            default_permissions = [
                RoutePermission(path="/admin-only", required_role="admin"),
                RoutePermission(path="/profile", required_role="user"),
                RoutePermission(path="/admin/permissions", required_role="admin"),
            ]
            db.add_all(default_permissions)
            db.commit()
    finally:
        db.close()

seed_permissions()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)

# Add middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(RoleBasedAccessMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/profile")
def profile(user=Depends(get_user_from_cookie)):
    return {"message": f"Hello, {user['sub']}!"}

@app.get("/admin-only")
def admin_panel(user=Depends(get_user_from_cookie)):
    return {"message": "Welcome to the admin panel"}