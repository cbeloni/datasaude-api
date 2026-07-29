from typing import List, Optional

from sqlalchemy import func, or_, select

from app.user.models import Permission, Role, RolePermission, User
from app.user.services.password import hash_password
from core.db import Transactional, session
from core.exceptions import (
    BadRequestException,
    DuplicateEmailOrNicknameException,
    ForbiddenException,
    NotFoundException,
)


DEFAULT_PERMISSIONS = [
    ("dashboard.view", "Dashboard"),
    ("previsao.view", "Previsão"),
    ("chat_ia.view", "IA Chat"),
    ("indicadores.view", "Indicadores"),
    ("table.view", "Tabelas"),
    ("table.patients.view", "Tabelas / Pacientes"),
    ("table.pollutants.view", "Tabelas / Poluente online"),
    ("table.ibge_v1.view", "Tabelas / IBGE v1"),
    ("table.ibge_v2.view", "Tabelas / IBGE"),
    ("maps.view", "Mapas"),
    ("maps.dynamic.view", "Mapas / Mapa dinâmico"),
    ("maps.bronquiolite.view", "Mapas / Bronquiolite"),
    ("maps.static.view", "Mapas / Mapa estático"),
    ("maps.ibge.view", "Mapas / Mapa IBGE"),
    ("maps.ibge_v2.view", "Mapas / Mapa IBGE V2"),
    ("maps.bronquiolite_vsr.view", "Mapas / Bronquiolite VSR"),
    ("users.manage", "Gestão de usuários"),
    ("roles.manage", "Gestão de perfis"),
]


def _user_payload(user: User, role_name: Optional[str] = None) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "nickname": user.nickname,
        "is_active": user.is_active,
        "is_admin": bool(user.is_admin),
        "role_id": user.role_id,
        "role_name": role_name,
        "created_at": user.__dict__.get("created_at"),
        "updated_at": user.__dict__.get("updated_at"),
    }


async def _get_active_role(role_id: Optional[int]) -> Optional[Role]:
    if role_id is None:
        return None

    role = await session.get(Role, role_id)
    if not role or not role.is_active:
        raise BadRequestException("perfil inválido ou inativo")
    return role


class UserAdminService:
    async def list_users(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        role_id: Optional[int] = None,
    ) -> dict:
        limit = min(max(limit, 1), 100)
        page = max(page, 1)
        filters = []
        if search:
            term = f"%{search.strip()}%"
            filters.append(
                or_(
                    User.nickname.ilike(term),
                    User.email.ilike(term),
                    Role.name.ilike(term),
                )
            )
        if is_active is not None:
            filters.append(User.is_active == is_active)
        if role_id is not None:
            filters.append(User.role_id == role_id)

        count_query = (
            select(func.count(User.id))
            .select_from(User)
            .outerjoin(Role, User.role_id == Role.id)
            .where(*filters)
        )
        total = int((await session.execute(count_query)).scalar_one())

        query = (
            select(User, Role.name)
            .outerjoin(Role, User.role_id == Role.id)
            .where(*filters)
            .order_by(User.id.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
        rows = (await session.execute(query)).all()
        return {
            "items": [_user_payload(user, role_name) for user, role_name in rows],
            "page": page,
            "limit": limit,
            "total": total,
        }

    async def get_user(self, user_id: int) -> dict:
        query = (
            select(User, Role.name)
            .outerjoin(Role, User.role_id == Role.id)
            .where(User.id == user_id)
        )
        row = (await session.execute(query)).first()
        if not row:
            raise NotFoundException("usuário não encontrado")
        return _user_payload(row[0], row[1])

    @Transactional()
    async def create_user(
        self,
        email: str,
        nickname: str,
        password: str,
        role_id: Optional[int] = None,
        is_active: bool = True,
    ) -> dict:
        email = email.strip().lower()
        nickname = nickname.strip()
        if len(password) < 8:
            raise BadRequestException("a senha deve possuir ao menos 8 caracteres")
        duplicate = await session.execute(
            select(User).where(or_(User.email == email, User.nickname == nickname))
        )
        if duplicate.scalars().first():
            raise DuplicateEmailOrNicknameException
        await _get_active_role(role_id)
        user = User(
            email=email,
            nickname=nickname,
            password=hash_password(password),
            role_id=role_id,
            is_active=is_active,
            is_admin=False,
        )
        session.add(user)
        await session.flush()
        return _user_payload(user)

    @Transactional()
    async def update_user(self, user_id: int, **changes) -> dict:
        user = await session.get(User, user_id)
        if not user:
            raise NotFoundException("usuário não encontrado")

        email = changes.get("email")
        nickname = changes.get("nickname")
        if email is not None:
            email = email.strip().lower()
        if nickname is not None:
            nickname = nickname.strip()
        if email or nickname:
            duplicate = await session.execute(
                select(User).where(
                    User.id != user_id,
                    or_(
                        User.email == email if email else False,
                        User.nickname == nickname if nickname else False,
                    ),
                )
            )
            if duplicate.scalars().first():
                raise DuplicateEmailOrNicknameException
        if email:
            user.email = email
        if nickname:
            user.nickname = nickname
        if changes.get("password") is not None:
            if len(changes["password"]) < 8:
                raise BadRequestException("a senha deve possuir ao menos 8 caracteres")
            user.password = hash_password(changes["password"])
        if "role_id" in changes:
            await _get_active_role(changes["role_id"])
            user.role_id = changes["role_id"]
        if changes.get("is_active") is not None:
            user.is_active = changes["is_active"]
        await session.flush()
        return await self.get_user(user_id)

    @Transactional()
    async def set_active(self, user_id: int, is_active: bool) -> dict:
        user = await session.get(User, user_id)
        if not user:
            raise NotFoundException("usuário não encontrado")
        if not is_active and user.is_active and user.is_admin:
            active_admins = await session.execute(
                select(func.count(User.id)).where(
                    User.is_admin.is_(True), User.is_active.is_(True)
                )
            )
            if int(active_admins.scalar_one()) <= 1:
                raise ForbiddenException("não é possível inativar o último administrador")
        user.is_active = is_active
        await session.flush()
        return await self.get_user(user_id)

    async def list_roles(self) -> List[dict]:
        roles = (await session.execute(select(Role).order_by(Role.name))).scalars().all()
        result = []
        for role in roles:
            result.append(await self.get_role(role.id))
        return result

    async def get_role(self, role_id: int) -> dict:
        role_query = select(
            Role.id,
            Role.name,
            Role.is_active,
            Role.created_at,
            Role.updated_at,
        ).where(Role.id == role_id)
        role = (await session.execute(role_query)).first()
        if not role:
            raise NotFoundException("perfil não encontrado")
        query = (
            select(Permission.code, Permission.name)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .where(RolePermission.role_id == role_id)
            .order_by(Permission.code)
        )
        permissions = (await session.execute(query)).all()
        return {
            "id": role.id,
            "name": role.name,
            "is_active": role.is_active,
            "permissions": [
                {"code": code, "name": name} for code, name in permissions
            ],
            "created_at": role.created_at,
            "updated_at": role.updated_at,
        }

    async def _get_permission_ids(self, codes: List[str]) -> List[int]:
        if not codes:
            return []
        rows = (
            await session.execute(select(Permission).where(Permission.code.in_(codes)))
        ).scalars().all()
        found = {permission.code: permission.id for permission in rows}
        missing = [code for code in codes if code not in found]
        if missing:
            raise BadRequestException(f"permissões inválidas: {', '.join(missing)}")
        return [found[code] for code in codes]

    @Transactional()
    async def create_role(self, name: str, permission_codes: List[str]) -> dict:
        name = name.strip()
        if not name:
            raise BadRequestException("nome do perfil é obrigatório")
        existing = await session.execute(select(Role).where(Role.name == name))
        if existing.scalars().first():
            raise BadRequestException("perfil já cadastrado")
        permission_ids = await self._get_permission_ids(permission_codes)
        permission_names = {
            permission.code: permission.name
            for permission in (
                await session.execute(
                    select(Permission).where(Permission.code.in_(permission_codes))
                )
            ).scalars().all()
        }
        role = Role(name=name, is_active=True)
        session.add(role)
        await session.flush()
        for permission_id in permission_ids:
            session.add(RolePermission(role_id=role.id, permission_id=permission_id))
        await session.flush()
        return {
            "id": role.id,
            "name": role.name,
            "is_active": role.is_active,
            "permissions": [
                {"code": code, "name": permission_names[code]}
                for code in sorted(permission_names)
            ],
            "created_at": None,
            "updated_at": None,
        }

    @Transactional()
    async def update_role(
        self,
        role_id: int,
        name: Optional[str] = None,
        permission_codes: Optional[List[str]] = None,
        is_active: Optional[bool] = None,
    ) -> dict:
        role = await session.get(Role, role_id)
        if not role:
            raise NotFoundException("perfil não encontrado")
        if name:
            duplicate = await session.execute(
                select(Role).where(Role.name == name.strip(), Role.id != role_id)
            )
            if duplicate.scalars().first():
                raise BadRequestException("perfil já cadastrado")
            role.name = name.strip()
        if is_active is not None:
            role.is_active = is_active
        if permission_codes is not None:
            await session.execute(
                RolePermission.__table__.delete().where(
                    RolePermission.role_id == role_id
                )
            )
            for permission_id in await self._get_permission_ids(permission_codes):
                session.add(RolePermission(role_id=role_id, permission_id=permission_id))
        await session.flush()
        return await self.get_role(role_id)

    async def list_permissions(self) -> List[dict]:
        permissions = (
            await session.execute(select(Permission).order_by(Permission.code))
        ).scalars().all()
        return [{"code": item.code, "name": item.name} for item in permissions]

    async def get_me(self, user_id: int) -> dict:
        user = await session.get(User, user_id)
        if not user or not user.is_active:
            raise NotFoundException("usuário não encontrado")
        permissions = ["dashboard.view"]
        role = await self.get_role(user.role_id) if user.role_id else None
        if role and role["is_active"]:
            permissions.extend(item["code"] for item in role["permissions"])
        if user.is_admin:
            permissions = [code for code, _ in DEFAULT_PERMISSIONS]
        else:
            permissions = list(dict.fromkeys(permissions))
        return {
            **_user_payload(user, role["name"] if role else None),
            "permissions": permissions,
        }
