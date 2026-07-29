from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Request

from app.user.schemas import (
    ExceptionResponseSchema,
    PermissionListResponseSchema,
    RoleCreateRequestSchema,
    RoleResponseSchema,
    RoleUpdateRequestSchema,
    UserAdminCreateRequestSchema,
    UserAdminListResponseSchema,
    UserAdminResponseSchema,
    UserAdminUpdateRequestSchema,
)
from app.user.services.admin import UserAdminService
from core.fastapi.dependencies import PermissionDependency
from core.fastapi.dependencies.permission import HasPermission


admin_user_router = APIRouter()


@admin_user_router.get(
    "/users",
    response_model=UserAdminListResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([HasPermission("users.manage")]))],
)
async def list_admin_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    role_id: Optional[int] = Query(None),
):
    return await UserAdminService().list_users(
        page=page,
        limit=limit,
        search=search,
        is_active=is_active,
        role_id=role_id,
    )


@admin_user_router.get(
    "/users/{user_id}",
    response_model=UserAdminResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([HasPermission("users.manage")]))],
)
async def get_admin_user(user_id: int):
    return await UserAdminService().get_user(user_id)


@admin_user_router.post(
    "/users",
    response_model=UserAdminResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([HasPermission("users.manage")]))],
)
async def create_admin_user(payload: UserAdminCreateRequestSchema):
    return await UserAdminService().create_user(**payload.dict())


@admin_user_router.patch(
    "/users/{user_id}",
    response_model=UserAdminResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([HasPermission("users.manage")]))],
)
async def update_admin_user(
    user_id: int, payload: UserAdminUpdateRequestSchema
):
    return await UserAdminService().update_user(
        user_id, **payload.dict(exclude_unset=True)
    )


@admin_user_router.post(
    "/users/{user_id}/activate",
    response_model=UserAdminResponseSchema,
    dependencies=[Depends(PermissionDependency([HasPermission("users.manage")]))],
)
async def activate_admin_user(user_id: int):
    return await UserAdminService().set_active(user_id, True)


@admin_user_router.post(
    "/users/{user_id}/deactivate",
    response_model=UserAdminResponseSchema,
    dependencies=[Depends(PermissionDependency([HasPermission("users.manage")]))],
)
async def deactivate_admin_user(user_id: int):
    return await UserAdminService().set_active(user_id, False)


@admin_user_router.get(
    "/roles",
    response_model=List[RoleResponseSchema],
    dependencies=[Depends(PermissionDependency([HasPermission("roles.manage")]))],
)
async def list_admin_roles():
    return await UserAdminService().list_roles()


@admin_user_router.get(
    "/permissions",
    response_model=PermissionListResponseSchema,
    dependencies=[Depends(PermissionDependency([HasPermission("roles.manage")]))],
)
async def list_admin_permissions():
    return {"items": await UserAdminService().list_permissions()}


@admin_user_router.post(
    "/roles",
    response_model=RoleResponseSchema,
    dependencies=[Depends(PermissionDependency([HasPermission("roles.manage")]))],
)
async def create_admin_role(payload: RoleCreateRequestSchema):
    return await UserAdminService().create_role(**payload.dict())


@admin_user_router.patch(
    "/roles/{role_id}",
    response_model=RoleResponseSchema,
    dependencies=[Depends(PermissionDependency([HasPermission("roles.manage")]))],
)
async def update_admin_role(role_id: int, payload: RoleUpdateRequestSchema):
    return await UserAdminService().update_role(
        role_id, **payload.dict(exclude_unset=True)
    )


@admin_user_router.post(
    "/roles/{role_id}/deactivate",
    response_model=RoleResponseSchema,
    dependencies=[Depends(PermissionDependency([HasPermission("roles.manage")]))],
)
async def deactivate_admin_role(role_id: int):
    return await UserAdminService().update_role(role_id, is_active=False)
