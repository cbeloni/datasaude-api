from typing import Optional

from sqlalchemy import desc, func, select
from decimal import Decimal, ROUND_HALF_UP

from api.ibge.v1.request.ibge import IbgeBase, IbgeFiltroParams
from app.ibge.models.ibge_caracteristica_model import IbgeCaracteristica
from app.ibge.models.ibge_model import Ibge
from app.ibge.models.ibge_pessoas_model import IbgePessoas
from app.ibge.models.ibge_pessoas_b_model import IbgePessoasB
from app.ibge.models.ibge_pessoas_c_model import IbgePessoasC
from app.ibge.services.ibge_formula_service import aplicar_formulas_customizadas
from core.db.session import session


def _apply_range(query, column, min_value=None, max_value=None):
    if min_value is not None:
        query = query.where(column >= min_value)
    if max_value is not None:
        query = query.where(column <= max_value)
    return query


def _to_decimal_if_numeric(value):
    if value is None:
        return None
    if isinstance(value, (int, float, Decimal)):
        try:
            return Decimal(str(value))
        except Exception:
            return None
    if isinstance(value, str):
        clean = value.strip()
        if clean.isdigit():
            return Decimal(clean)
    return None


async def ibge_list(
    limit: int = None,
    prev: Optional[int] = None,
    start: int = 0,
    filtro: IbgeFiltroParams = None,
) -> (any, int):
    query = (
        select(Ibge, IbgeCaracteristica, IbgePessoas, IbgePessoasB, IbgePessoasC)
        .outerjoin(IbgeCaracteristica, Ibge.cd_setor == IbgeCaracteristica.cd_setor)
        .outerjoin(IbgePessoas, Ibge.cd_setor == IbgePessoas.cd_setor)
        .outerjoin(IbgePessoasB, Ibge.cd_setor == IbgePessoasB.cd_setor)
        .outerjoin(IbgePessoasC, Ibge.cd_setor == IbgePessoasC.cd_setor)
    )

    if prev:
        query = query.where(Ibge.id < prev)

    if filtro is not None:
        if filtro.cd_setor:
            query = query.where(Ibge.cd_setor.in_(filtro.cd_setor))
        if filtro.situacao:
            query = query.where(Ibge.situacao.ilike(f"%{filtro.situacao}%"))
        if filtro.nm_uf:
            query = query.where(Ibge.nm_uf.ilike(f"%{filtro.nm_uf}%"))
        if filtro.nm_mun:
            query = query.where(Ibge.nm_mun.ilike(f"%{filtro.nm_mun}%"))
        if filtro.nm_bairro:
            query = query.where(Ibge.nm_bairro.ilike(f"%{filtro.nm_bairro}%"))

        if filtro.cd_uf is not None:
            query = query.where(Ibge.cd_uf == filtro.cd_uf)
        if filtro.cd_mun is not None:
            query = query.where(Ibge.cd_mun == filtro.cd_mun)
        if filtro.cd_sit is not None:
            query = query.where(Ibge.cd_sit == filtro.cd_sit)
        if filtro.cd_tipo is not None:
            query = query.where(Ibge.cd_tipo == filtro.cd_tipo)
        if filtro.cd_regiao is not None:
            query = query.where(Ibge.cd_regiao == filtro.cd_regiao)

        query = _apply_range(query, Ibge.area_km2, filtro.area_km2_min, filtro.area_km2_max)

    if limit is None:
        limit = 10
    if limit > 1000:
        limit = 1000

    count_subquery = query.with_only_columns(Ibge.id).order_by(None).distinct().subquery()
    count_query = select(func.count()).select_from(count_subquery)
    quantidade = (await session.execute(count_query)).scalar()

    query = query.offset(start).limit(limit).order_by(desc(Ibge.id))
    rows = (await session.execute(query)).all()
    registros = []
    for ibge, caracteristica, pessoas, pessoas_b, pessoas_c in rows:
        payload = dict(ibge.__dict__)
        payload.pop("_sa_instance_state", None)
        if caracteristica is not None:
            caracteristica_dict = dict(caracteristica.__dict__)
            caracteristica_dict.pop("_sa_instance_state", None)
            for key, value in caracteristica_dict.items():
                if key in {"id", "cd_setor", "created_at", "updated_at"}:
                    continue
                payload[key] = value
        if pessoas is not None:
            pessoas_dict = dict(pessoas.__dict__)
            pessoas_dict.pop("_sa_instance_state", None)
            for key, value in pessoas_dict.items():
                if key in {"id", "cd_setor", "created_at", "updated_at"}:
                    continue
                payload[f"pes_{key}"] = value
        if pessoas_b is not None:
            pessoas_b_dict = dict(pessoas_b.__dict__)
            pessoas_b_dict.pop("_sa_instance_state", None)
            for key, value in pessoas_b_dict.items():
                if key in {"id", "cd_setor", "created_at", "updated_at"}:
                    continue
                payload[f"pes_b_{key}"] = value
        if pessoas_c is not None:
            pessoas_c_dict = dict(pessoas_c.__dict__)
            pessoas_c_dict.pop("_sa_instance_state", None)
            for key, value in pessoas_c_dict.items():
                if key in {"id", "cd_setor", "created_at", "updated_at"}:
                    continue
                payload[f"pes_c_{key}"] = value

        try:
            v00047 = Decimal(payload["v00047"]) if payload.get("v00047") is not None else None
            v0003 = Decimal(payload["v0003"]) if payload.get("v0003") is not None else None
            if v00047 is not None and v0003 is not None and v0003 != 0:
                payload["percentual_domicios_ocupados"] = (v00047 / v0003 * 100).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            else:
                payload["percentual_domicios_ocupados"] = None
        except Exception:
            payload["percentual_domicios_ocupados"] = None

        v01696 = _to_decimal_if_numeric(payload.get("pes_v01696"))
        v0001 = _to_decimal_if_numeric(payload.get("v0001"))
        if v01696 is None or v0001 is None or v0001 == 0:
            payload["percentual_pessoas"] = Decimal("0")
        else:
            payload["percentual_pessoas"] = (v01696 / v0001 * 100).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

        payload = await aplicar_formulas_customizadas(payload)

        registros.append(IbgeBase(**payload))

    return registros, quantidade
