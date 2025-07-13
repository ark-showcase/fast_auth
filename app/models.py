from typing import Dict
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:123456@localhost:3306/getauth"
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RoutePermission(Base):
    __tablename__ = "route_permissions"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(255), unique=True, index=True)
    required_role = Column(String(50))


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    group = Column(String(50))


class UserGroups(Base):
    __tablename__ = "user_groups"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True)

# For dev/demo purposes (still in memory)
fake_users_db: Dict[str, dict] = {
    "admin_user": {
        "username": "admin_user",
        "password": "$2b$12$kbO3/4NHPPogyvgYvoCdcOlPITKhN/tWA3WOAAfTmkFQA2LeJkjuu",  # "adminpass"
        "group": "admin"
    },
    "normal_user": {
        "username": "normal_user",
        "password": "$2b$12$AFUZ1oj5zDwGxyixOdOt4enKTGivIQThYOwOM2cF1rDzEEZ7goYyO",  # "userpass"
        "group": "user"
    }
}
fake_groups_db: Dict[str, list] = {
    "admin": [],
    "user": []
}