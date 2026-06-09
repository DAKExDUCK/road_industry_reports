"""Application factory and startup helpers for the API server."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud
from .api import auth as auth_router
from .api import roles as roles_router
from .core.config import settings
from .db import engine
from .models import Base

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Root endpoint returning a simple health/message payload."""
    return {"message": "Road Industry Reports API"}


# Register routers
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(roles_router.router, prefix="/admin", tags=["admin"])


@app.on_event("startup")
def on_startup():
    """Create database tables and seed default roles/root admin if configured."""
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # Seed default roles and root admin if configured
    db = Session(bind=engine)
    try:
        # Read root admin credentials from settings; support multiple key styles
        root_email = getattr(settings, "ROOT_ADMIN_EMAIL", None) or getattr(settings, "root_admin_email", None)
        root_password = getattr(settings, "ROOT_ADMIN_PASSWORD", None) or getattr(settings, "root_admin_password", None)

        # create roles if missing
        root_role = crud.get_role_by_name(db, "root_admin")
        if not root_role:
            root_role = crud.create_role(
                db,
                type("R", (), {"name": "root_admin", "is_admin": True, "is_root": True}),
            )
        admin_role = crud.get_role_by_name(db, "admin")
        if not admin_role:
            admin_role = crud.create_role(db, type("R", (), {"name": "admin", "is_admin": True, "is_root": False}))
        user_role = crud.get_role_by_name(db, "user")
        if not user_role:
            user_role = crud.create_role(db, type("R", (), {"name": "user", "is_admin": False, "is_root": False}))

        # create root user if env provided and not exists
        if root_email and root_password:
            existing = crud.get_user_by_email(db, root_email)
            if not existing:
                u_in = type("U", (), {"email": root_email, "password": root_password})
                created = crud.create_user(db, u_in)
                crud.assign_role_to_user(db, created, root_role)
    finally:
        db.close()
