"""Dependency helpers for retrieving the current user and enforcing permissions.

This module exposes `get_db` for acquiring a DB session, `get_current_user`
which decodes a JWT and returns the corresponding user, and helper
dependencies for requiring root users or specific permissions.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models
from .core.config import settings
from .db import session_local

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    """Yield a database session and ensure it is closed afterwards."""
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Decode the JWT `token` and return the corresponding `User`.

    Raises HTTP 401 if the token is invalid or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def require_root_user(current_user: models.User = Depends(get_current_user)):
    """Dependency that ensures `current_user` has a role with `is_root=True`.

    Raises HTTP 403 if the user is not a root admin.
    """
    for r in getattr(current_user, "roles", []):
        if getattr(r, "is_root", False):
            return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requires root admin privileges")


def require_permission(permission_name: str):
    """Factory that returns a dependency which checks for `permission_name`.

    The returned dependency will raise HTTP 403 if the current user lacks the
    named permission.
    """

    def _checker(current_user: models.User = Depends(get_current_user)):
        # collect permissions from user roles
        perms = set()
        for r in getattr(current_user, "roles", []):
            # roles with is_admin True implicitly have all perms via assignment on creation
            for p in getattr(r, "permissions", []):
                perms.add(p.name)
        if permission_name in perms:
            return current_user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

    return _checker
