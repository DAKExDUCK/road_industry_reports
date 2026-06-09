"""SQLAlchemy models for users, roles, and permissions."""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .db import Base

# Association tables
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE")),
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE")),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE")),
)


class User(Base):
    """User account model.

    Attributes:
        id: Primary key.
        email: Unique user email.
        hashed_password: Password hash.
        is_active: Whether the account is active.
        roles: Relationship to `Role`.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    roles = relationship("Role", secondary=user_roles, back_populates="users")

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"


class Role(Base):
    """Role model representing a group with permissions.

    Attributes:
        name: Role name.
        is_admin: Whether this role should receive admin-like permissions.
        is_root: Whether this role is a root/admin role.
    """

    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)  # admin-like roles that should receive new perms
    is_root = Column(Boolean, default=False)  # root admin role (one or more users)
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

    def __repr__(self):
        return f"<Role id={self.id} name={self.name} admin={self.is_admin} root={self.is_root}>"


class Permission(Base):
    """Permission model representing a named permission."""

    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

    def __repr__(self):
        return f"<Permission id={self.id} name={self.name}>"
