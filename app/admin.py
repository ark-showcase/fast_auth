from fastapi import APIRouter, HTTPException, Depends, Body, Query, Path
from sqlalchemy.orm import Session
from app.models import SessionLocal, RoutePermission
from app.roles import get_user_from_cookie
from app.schemas import PermissionCreateRequest

admin_router = APIRouter(prefix="/admin", tags=["admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@admin_router.get("/permissions")
def list_permissions(db: Session = Depends(get_db)):
    return db.query(RoutePermission).all()

@admin_router.post("/permissions")
def create_permission(
    permission: PermissionCreateRequest = Body(..., description='Route path param'),
    db: Session = Depends(get_db)
):

    existing = db.query(RoutePermission).filter_by(path=permission.path).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")

    new_perm = RoutePermission(
        path=permission.path,
        required_role=permission.required_role
    )
    db.add(new_perm)
    db.commit()
    db.refresh(new_perm)
    return new_perm

@admin_router.delete("/permissions")
def delete_permission(
        path: str = Query(description='Route path param'),
        db: Session = Depends(get_db)
):
    perm = db.query(RoutePermission).filter_by(path=path).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(perm)
    db.commit()
    return {"detail": "Permission deleted"}