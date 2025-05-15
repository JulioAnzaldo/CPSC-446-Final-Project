from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
)
from sqlalchemy.orm import relationship

from .db import Base

# Association table for Plan; Permission many-to-many
plan_permissions = Table(
    "plan_permissions",
    Base.metadata,
    Column("plan_id", Integer, ForeignKey("plans.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")

    usage_records = relationship(
        "UsageRecord",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Link to individual access controls:
    access_controls = relationship(
        "AccessControl",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Link to a subscription plan:
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=True)
    plan = relationship("Plan", back_populates="users")


class CloudService(Base):
    __tablename__ = "cloud_services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    # Maximum allowed calls per minute (default is 60)
    max_calls_per_minute = Column(Integer, default=60)

    access_controls = relationship(
        "AccessControl",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    # Optional backref for usage records
    usage_records = relationship("UsageRecord", back_populates="service")


class AccessControl(Base):
    __tablename__ = "access_controls"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("cloud_services.id"), nullable=False)
    permission = Column(String, nullable=False)

    user = relationship("User", back_populates="access_controls")
    service = relationship("CloudService", back_populates="access_controls")


class UsageRecord(Base):
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("cloud_services.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="usage_records")
    service = relationship("CloudService", back_populates="usage_records")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # e.g. "read", "write"
    service_name = Column(String, index=True)  # e.g. "gaming-api"

    # Plans that include this permission
    plans = relationship(
        "Plan",
        secondary=plan_permissions,
        back_populates="permissions",
    )


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    max_calls_per_minute = Column(Integer, default=60)

    # Permissions included in this plan
    permissions = relationship(
        "Permission",
        secondary=plan_permissions,
        back_populates="plans",
    )

    # Users subscribed to this plan
    users = relationship("User", back_populates="plan")
