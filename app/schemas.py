from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    group: str

class PermissionCreateRequest(BaseModel):
    path: str
    required_role: str