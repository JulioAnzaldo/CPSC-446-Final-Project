from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

# File to define schemas


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role: str
    plan_id: Optional[int] = None

    class Config:
        orm_mode = True


class UserUpdatePlan(BaseModel):
    plan_id: int


class PermissionBase(BaseModel):
    name: str
    service_name: str


class PermissionCreate(PermissionBase):
    pass


class Permission(PermissionBase):
    id: int

    class Config:
        orm_mode = True


class PlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    max_calls_per_minute: Optional[int] = 60


class PlanCreate(PlanBase):
    permission_ids: List[int] = []


class Plan(PlanBase):
    id: int
    permissions: List[Permission] = []

    class Config:
        orm_mode = True


class CloudServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    max_calls_per_minute: Optional[int] = 60


class CloudServiceCreate(CloudServiceBase):
    pass


class CloudService(CloudServiceBase):
    id: int

    class Config:
        orm_mode = True


class AccessControlBase(BaseModel):
    permission: str


class AccessControlCreate(AccessControlBase):
    user_id: int
    service_id: int


class AccessControl(AccessControlBase):
    id: int
    user_id: int
    service_id: int

    class Config:
        orm_mode = True


class UsageRecordBase(BaseModel):
    user_id: int
    service_id: int


class UsageRecordCreate(UsageRecordBase):
    pass


class UsageRecord(UsageRecordBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class AuditLogBase(BaseModel):
    user_id: int
    action: str
    detail: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLog(AuditLogBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
