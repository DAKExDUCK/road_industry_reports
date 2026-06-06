from sqlalchemy.orm import Session
from . import models, schemas
from .core.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Roles & Permissions CRUD
def get_role_by_name(db: Session, name: str):
    return db.query(models.Role).filter(models.Role.name == name).first()


def create_role(db: Session, role_in: schemas.RoleCreate):
    role = models.Role(name=role_in.name, is_admin=role_in.is_admin or False, is_root=role_in.is_root or False)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def create_permission(db: Session, perm_in: schemas.PermissionBase):
    perm = models.Permission(name=perm_in.name, description=perm_in.description)
    db.add(perm)
    db.commit()
    db.refresh(perm)
    # automatically assign this permission to all admin-like roles
    admin_roles = db.query(models.Role).filter(models.Role.is_admin == True).all()
    for r in admin_roles:
        r.permissions.append(perm)
    db.commit()
    return perm


def assign_role_to_user(db: Session, user: models.User, role: models.Role):
    if role not in user.roles:
        user.roles.append(role)
        db.commit()
        db.refresh(user)
    return user


def assign_permission_to_role(db: Session, role: models.Role, perm: models.Permission):
    if perm not in role.permissions:
        role.permissions.append(perm)
        db.commit()
        db.refresh(role)
    return role

