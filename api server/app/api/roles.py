"""Admin routes for managing roles and permissions."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..deps import get_db, require_permission, require_root_user

router = APIRouter()


@router.get("/permissions", response_model=list[schemas.PermissionOut])
def list_permissions(db: Session = Depends(get_db), _user=Depends(require_permission("perm.view"))):
    """List all permissions."""
    perms = db.query(models.Permission).all()
    return perms


@router.post("/permissions", response_model=schemas.PermissionOut)
def create_permission(
    perm_in: schemas.PermissionBase,
    db: Session = Depends(get_db),
    _user=Depends(require_permission("perm.create")),
):
    """Create a permission. Permission is automatically assigned to admin-like roles."""
    existing = db.query(models.Permission).filter(models.Permission.name == perm_in.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Permission already exists")
    perm = crud.create_permission(db, perm_in)
    return perm


@router.get("/roles", response_model=list[schemas.RoleOut])
def list_roles(db: Session = Depends(get_db), _user=Depends(require_permission("role.view"))):
    """List all roles."""
    roles = db.query(models.Role).all()
    return roles


@router.post("/roles", response_model=schemas.RoleOut)
def create_role(
    role_in: schemas.RoleCreate,
    db: Session = Depends(get_db),
    _user=Depends(require_root_user),
):
    """Create a role. Only root-admin users are allowed to create roles."""
    existing = crud.get_role_by_name(db, role_in.name)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role exists")
    role = crud.create_role(db, role_in)
    return role


@router.post("/roles/{role_id}/assign/{user_id}")
def assign_role_to_user(
    role_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    _user=Depends(require_permission("role.assign")),
):
    """Assign a role to a user. Requires `role.assign` permission."""
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not role or not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role or user not found")
    updated = crud.assign_role_to_user(db, user, role)
    return {"status": "ok", "user_id": updated.id}


@router.post("/roles/{role_id}/permissions/{perm_id}")
def assign_perm_to_role(
    role_id: int,
    perm_id: int,
    db: Session = Depends(get_db),
    _user=Depends(require_permission("perm.assign")),
):
    """Assign a permission to a role. Requires `perm.assign` permission."""
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    perm = db.query(models.Permission).filter(models.Permission.id == perm_id).first()
    if not role or not perm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role or permission not found")
    updated = crud.assign_permission_to_role(db, role, perm)
    return {"status": "ok", "role_id": updated.id}
