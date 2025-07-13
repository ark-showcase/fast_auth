from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import SessionLocal, RoutePermission
from app.roles import get_user_from_cookie

admin_router = APIRouter(prefix="/admin", tags=["admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@admin_router.get("/permissions")
def list_permissions(user=Depends(get_user_from_cookie), db: Session = Depends(get_db)):
    if user["group"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return db.query(RoutePermission).all()

@admin_router.post("/permissions")
def create_permission(path: str, required_role: str, user=Depends(get_user_from_cookie), db: Session = Depends(get_db)):
    if user["group"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    existing = db.query(RoutePermission).filter_by(path=path).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")
    new_perm = RoutePermission(path=path, required_role=required_role)
    db.add(new_perm)
    db.commit()
    db.refresh(new_perm)
    return new_perm

@admin_router.delete("/permissions")
def delete_permission(path: str, user=Depends(get_user_from_cookie), db: Session = Depends(get_db)):
    if user["group"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    perm = db.query(RoutePermission).filter_by(path=path).first()
    if not perm:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(perm)
    db.commit()
    return {"detail": "Permission deleted"}