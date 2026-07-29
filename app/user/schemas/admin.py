from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class PermissionResponseSchema(BaseModel):
    code: str
    name: str


class RoleResponseSchema(BaseModel):
    id: int
    name: str
    is_active: bool
    permissions: List[PermissionResponseSchema] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class RoleCreateRequestSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    permission_codes: List[str] = Field(default_factory=list)


class RoleUpdateRequestSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    permission_codes: Optional[List[str]] = None
    is_active: Optional[bool] = None


class UserAdminResponseSchema(BaseModel):
    id: int
    email: str
    nickname: str
    is_active: bool
    is_admin: bool
    role_id: Optional[int] = None
    role_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserAdminCreateRequestSchema(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    nickname: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8, max_length=255)
    role_id: Optional[int] = None
    is_active: bool = True


class UserAdminUpdateRequestSchema(BaseModel):
    email: Optional[str] = Field(None, min_length=3, max_length=255)
    nickname: Optional[str] = Field(None, min_length=1, max_length=255)
    password: Optional[str] = Field(None, min_length=8, max_length=255)
    role_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserAdminListResponseSchema(BaseModel):
    items: List[UserAdminResponseSchema]
    page: int
    limit: int
    total: int


class PermissionListResponseSchema(BaseModel):
    items: List[PermissionResponseSchema]


class MeResponseSchema(UserAdminResponseSchema):
    permissions: List[str] = Field(default_factory=list)

    @validator("permissions", pre=True)
    def normalize_permissions(cls, value):
        return value or []
