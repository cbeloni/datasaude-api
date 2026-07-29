from abc import ABC, abstractmethod
from typing import List, Type

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

from app.user.services import UserService
from core.exceptions import (
    CustomException,
    ForbiddenException,
    UnauthorizedException,
)


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class IsAdmin(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        return await UserService().is_admin(user_id=user_id)


def HasPermission(permission_code: str):
    class Permission(BasePermission):
        exception = UnauthorizedException

        async def has_permission(self, request: Request) -> bool:
            user_id = request.user.id
            if not user_id:
                raise UnauthorizedException
            if not await UserService().has_permission(user_id, permission_code):
                raise ForbiddenException
            return True

    Permission.__name__ = f"HasPermission_{permission_code.replace('.', '_')}"
    return Permission


class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[Type[BasePermission]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission() if isinstance(permission, type) else permission
            if not await cls.has_permission(request=request):
                raise cls.exception
