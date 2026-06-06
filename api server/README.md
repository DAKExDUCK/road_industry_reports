# API Server (FastAPI)

Minimal FastAPI backend for the Road Industry Reports project.

Overview
- FastAPI + SQLAlchemy + PostgreSQL
- JWT-based authentication (OAuth2 password grant)
- Role / Permission model (root_admin, admin, user)

Prerequisites
- Python 3.11+ (local development)
- Docker & Docker Compose (recommended)

Quick start (Docker Compose)

```bash
# from repository root
cp "api server/.env.example" "api server/.env"  # edit values if needed
docker-compose up --build
```

Local development

```bash
cd "api server"
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Environment variables (set in `api server/.env`)
- `DATABASE_URL` — SQLAlchemy database URL (default: `postgresql://postgres:postgres@db:5432/reports`)
- `SECRET_KEY` — JWT secret key (replace with a secure random value)
- `ACCESS_TOKEN_EXPIRE_MINUTES` — token expiry in minutes (default: 60)
- `ROOT_ADMIN_EMAIL` — optional: email to seed a root admin on startup
- `ROOT_ADMIN_PASSWORD` — optional: password to seed a root admin on startup

Authentication endpoints
- `POST /auth/token` — obtain JWT token (OAuth2 password form; use `username` for email)
- `POST /auth/register` — register a new user (email + password). Only callable by users with the root-admin role.
- `GET /auth/me` — returns the current user (requires `Authorization: Bearer <token>`)

Example: obtain a token

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=root@example.com&password=secret"
```

Roles & permissions
- Roles: `root_admin` (is_root=True), `admin` (is_admin=True), `user` (default)
- Permissions are separate entities and can be assigned to roles.
- New permissions are automatically assigned to roles with `is_admin=True`.

Admin API (prefix `/admin`)
- `POST /admin/roles` — create a role (root-only)
- `POST /admin/permissions` — create a permission (requires `perm.create` permission)
- `POST /admin/roles/{role_id}/assign/{user_id}` — assign a role to a user (root-only)
- `POST /admin/roles/{role_id}/permissions/{perm_id}` — assign permission to a role (requires `perm.assign`)

Startup behavior
- On startup the app will create database tables (SQLAlchemy `Base.metadata.create_all`).
- If `ROOT_ADMIN_EMAIL` and `ROOT_ADMIN_PASSWORD` are set, a root admin user is seeded and assigned the `root_admin` role.

Development helpers
- `format.sh` sources `format_configs/config.sh` and runs formatting and linting tools (`black`, `isort`, `pylint`, `mypy`).

Notes / next steps
- Use Alembic for production-grade DB migrations instead of `create_all`.
- Tighten CORS and secrets for production.

Files of interest
- `app/main.py` — application entrypoint, router registration, startup seeding
- `app/core` — configuration and security helpers
- `app/db.py` — SQLAlchemy engine / session / Base
- `app/models.py` — database models (`User`, `Role`, `Permission`)
- `app/schemas.py` — Pydantic schemas
- `app/crud.py` — CRUD helpers for users, roles, permissions
- `app/api` — API routers (auth, admin)
