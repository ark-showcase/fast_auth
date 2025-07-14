from typing import Dict
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
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