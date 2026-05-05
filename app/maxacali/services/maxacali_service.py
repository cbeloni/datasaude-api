from typing import Optional

from sqlalchemy import desc, func, select

from api.maxacali.v1.request.maxacali import MaxacaliBase, MaxacaliFiltroParams
from app.maxacali.models.maxacali_caracteristica_model import MaxacaliCaracteristica
from app.maxacali.models.maxacali_model import Maxacali
from core.db.session import session


def _apply_range(query, column, min_value=None, max_value=None):
    if min_value is not None:
        query = query.where(column >= min_value)
    if max_value is not None:
        query = query.where(column <= max_value)
    return query


async def maxacali_list(
    limit: int = None,
    prev: Optional[int] = None,
    start: int = 0,
    filtro: MaxacaliFiltroParams = None,
) -> (any, int):
    query = (
        select(Maxacali, MaxacaliCaracteristica)
        .join(MaxacaliCaracteristica, Maxacali.cd_setor == MaxacaliCaracteristica.cd_setor)
    )

    if prev:
        query = query.where(Maxacali.id < prev)

    if filtro is not None:
        if filtro.cd_setor:
            query = query.where(Maxacali.cd_setor == filtro.cd_setor)
        if filtro.situacao:
            query = query.where(Maxacali.situacao.ilike(f"%{filtro.situacao}%"))
        if filtro.nm_uf:
            query = query.where(Maxacali.nm_uf.ilike(f"%{filtro.nm_uf}%"))
        if filtro.nm_mun:
            query = query.where(Maxacali.nm_mun.ilike(f"%{filtro.nm_mun}%"))
        if filtro.nm_bairro:
            query = query.where(Maxacali.nm_bairro.ilike(f"%{filtro.nm_bairro}%"))

        if filtro.cd_uf is not None:
            query = query.where(Maxacali.cd_uf == filtro.cd_uf)
        if filtro.cd_mun is not None:
            query = query.where(Maxacali.cd_mun == filtro.cd_mun)
        if filtro.cd_sit is not None:
            query = query.where(Maxacali.cd_sit == filtro.cd_sit)
        if filtro.cd_tipo is not None:
            query = query.where(Maxacali.cd_tipo == filtro.cd_tipo)
        if filtro.cd_regiao is not None:
            query = query.where(Maxacali.cd_regiao == filtro.cd_regiao)

        query = _apply_range(query, Maxacali.area_km2, filtro.area_km2_min, filtro.area_km2_max)
        query = _apply_range(query, Maxacali.v0001, filtro.v0001_min, filtro.v0001_max)
        query = _apply_range(query, Maxacali.v0002, filtro.v0002_min, filtro.v0002_max)
        query = _apply_range(query, Maxacali.v0003, filtro.v0003_min, filtro.v0003_max)
        query = _apply_range(query, Maxacali.v0004, filtro.v0004_min, filtro.v0004_max)
        query = _apply_range(query, Maxacali.v0005, filtro.v0005_min, filtro.v0005_max)
        query = _apply_range(query, Maxacali.v0006, filtro.v0006_min, filtro.v0006_max)
        query = _apply_range(query, Maxacali.v0007, filtro.v0007_min, filtro.v0007_max)

    if limit is None:
        limit = 10
    if limit > 1000:
        limit = 1000

    count_subquery = query.with_only_columns(Maxacali.id).order_by(None).distinct().subquery()
    count_query = select(func.count()).select_from(count_subquery)
    quantidade = (await session.execute(count_query)).scalar()

    query = query.offset(start).limit(limit).order_by(desc(Maxacali.id))
    rows = (await session.execute(query)).all()
    registros = []
    for maxacali, caracteristica in rows:
        payload = dict(maxacali.__dict__)
        payload.pop("_sa_instance_state", None)
        if caracteristica is not None:
            caracteristica_dict = dict(caracteristica.__dict__)
            caracteristica_dict.pop("_sa_instance_state", None)
            for key, value in caracteristica_dict.items():
                if key in {"id", "cd_setor", "created_at", "updated_at"}:
                    continue
                payload[key] = value

        registros.append(MaxacaliBase(**payload))

    return registros, quantidade
