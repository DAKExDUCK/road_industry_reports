"""Pydantic schemas for API input and output models."""

from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base fields shared by user schemas."""

    email: EmailStr


class UserCreate(UserBase):
    """Schema for user creation (includes password)."""

    password: str


class UserOut(UserBase):
    """Response schema for user objects."""

    id: int
    is_active: bool

    class Config:  # pylint: disable=missing-class-docstring
        from_attributes = True


class PermissionBase(BaseModel):
    """Base schema for permissions."""

    name: str
    description: Optional[str] = None


class PermissionOut(PermissionBase):
    """Response schema for permissions."""

    id: int

    class Config:  # pylint: disable=missing-class-docstring
        from_attributes = True


class RoleBase(BaseModel):
    """Base schema for roles."""

    name: str


class RoleCreate(RoleBase):
    """Schema used when creating roles."""

    is_admin: Optional[bool] = False
    is_root: Optional[bool] = False


class RoleOut(RoleBase):
    """Response schema for roles including permissions."""

    id: int
    is_admin: bool
    is_root: bool
    permissions: list[PermissionOut] = []

    class Config:  # pylint: disable=missing-class-docstring
        from_attributes = True


class Token(BaseModel):
    """OAuth2 token response schema."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload data parsed from JWTs."""

    email: Optional[str] = None
