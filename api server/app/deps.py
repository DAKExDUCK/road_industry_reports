from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .core.config import settings
from .db import SessionLocal
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
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
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def require_root_user(current_user: models.User = Depends(get_current_user)):
    # Ensure current_user has a role with is_root=True
    for r in getattr(current_user, "roles", []):
        if getattr(r, "is_root", False):
            return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Requires root admin privileges")


def require_permission(permission_name: str):
    def _checker(current_user: models.User = Depends(get_current_user)):
        # collect permissions from user roles
        perms = set()
        for r in getattr(current_user, "roles", []):
            # roles with is_admin True implicitly have all perms via assignment on creation
            for p in getattr(r, "permissions", []) :
                perms.add(p.name)
        if permission_name in perms:
            return current_user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return _checker
