# FastAPI Role-Based Auth

## Features
- Role-based authentication using cookies and JWT
- Middleware-driven route protection
- Admin panel for managing route permissions
- Uses SQLAlchemy and MySQL

## Setup
1. Create a MySQL DB and update the URL in `models.py`
2. Install requirements: `pip install -r requirements.txt`
3. Run: `uvicorn app.main:app --reload`
4. Use `/signup`, `/login`, and `/admin/permissions` to interact

## Default Roles
- `admin`
- `user`