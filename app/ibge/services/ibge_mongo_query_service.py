import asyncio
import ast
import time
from math import ceil
from typing import Dict, List

from pymongo.cursor import Cursor

from api.ibge.v2.request.ibge import IbgeMongoQueryRequest, IbgeMongoQueryResponse
from app.ibge.services.ibge_mongo_cache_service import (
    get_cached_collection_count,
    get_cached_query_response,
    set_cached_collection_count,
    set_cached_query_response,
)
from app.ibge.services.ibge_mongo_formula_service import (
    aplicar_formulas_customizadas,
    listar_formulas_customizadas,
)
from core.exceptions import BadRequestException
from core.mongo import get_mongo_client, get_mongo_database, get_mongo_query_timeout
from core.utils.logger import LoggerUtils

log = LoggerUtils(__name__)


def _normalize_columns(columns: List[str]) -> List[str]:
    normalized_columns = []
    for column in columns:
        if column is None:
            continue
        normalized_column = column.strip()
        if normalized_column and normalized_column not in normalized_columns:
            normalized_columns.append(normalized_column)
    return normalized_columns


def _build_projection(columns: List[str], extra_columns: List[str] = None) -> Dict[str, int]:
    projection_columns = list(columns)
    for extra in extra_columns or []:
        if extra not in projection_columns:
            projection_columns.append(extra)
    projection = {column: 1 for column in projection_columns}
    projection["_id"] = 0
    return projection


def _extract_formula_dependencies(formulas: List[Dict]) -> List[str]:
    dependencies = []
    for formula in formulas:
        try:
            tree = ast.parse(formula["formula"], mode="eval")
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id not in dependencies:
                dependencies.append(node.id)
    return dependencies


def _executar_consulta_mongo(
    collection,
    query: Dict,
    projection: Dict,
    skip: int,
    limit: int,
) -> List[Dict]:
    """Executa a consulta MongoDB de forma síncrona (para ser chamada via to_thread)."""
    cursor: Cursor = (
        collection.find(query, projection)
        .sort("_id", 1)
        .skip(skip)
        .limit(limit)
    )
    return list(cursor)


def _contar_documentos_mongo(collection, query: Dict) -> int:
    return collection.count_documents(query)


def _build_count_signature(collection_name: str, query: Dict) -> Dict[str, str]:
    return {
        "collection_name": collection_name,
        "cd_setor": query.get("cd_setor") or "",
    }


def _build_query_signature(
    collection_name: str,
    columns: List[str],
    page: int,
    limit: int,
    query: Dict,
) -> Dict:
    return {
        "collection_name": collection_name,
        "columns": columns,
        "page": page,
        "limit": limit,
        "cd_setor": query.get("cd_setor") or "",
    }


async def consultar_colecao_mongo(payload: IbgeMongoQueryRequest):
    request_start = time.time()
    collection_name = payload.collection_name.strip()
    if not collection_name:
        raise BadRequestException("collection_name é obrigatório")

    columns = _normalize_columns(payload.columns)
    if not columns:
        raise BadRequestException("columns deve conter ao menos uma coluna")

    page = payload.page
    limit = payload.limit
    skip = (page - 1) * limit
    cd_setor_list = None

    log.info(
        f"[IBGE V2] Iniciando consulta | collection={collection_name} | "
        f"page={page} | limit={limit} | has_cd_setor={bool(payload.cd_setor)} | "
        f"columns={len(columns)}"
    )

    try:
        client = get_mongo_client()
    except ValueError as exc:
        raise BadRequestException(str(exc)) from exc

    try:
        database = get_mongo_database(client)
        if database is None:
            raise BadRequestException("Database MongoDB não configurado")

        query = {}
        if payload.cd_setor and len(payload.cd_setor) > 0:
            cd_setor_list = [s.strip() for s in payload.cd_setor if s.strip()]
            if len(cd_setor_list) == 1:
                query["cd_setor"] = cd_setor_list[0]
            else:
                query["cd_setor"] = {"$in": cd_setor_list}

        t0 = time.time()
        query_signature = _build_query_signature(
            collection_name=collection_name,
            columns=columns,
            page=page,
            limit=limit,
            query=query,
        )
        cached_response = await get_cached_query_response(query_signature)
        t1 = time.time()
        if cached_response is not None:
            if isinstance(cached_response.get("cd_setor"), str):
                cached_response["cd_setor"] = (
                    [cached_response["cd_setor"]] if cached_response["cd_setor"] else None
                )
            cached_payload = cached_response.get("payload", [])
            cached_total = cached_response.get("total_records", 0)
            if not (cached_total > 0 and len(cached_payload) == 0):
                log.info(
                    f"[IBGE V2] Cache HIT | collection={collection_name} | "
                    f"page={page} | cache_time={t1-t0:.3f}s"
                )
                return cached_response

        log.info(
            f"[IBGE V2] Cache MISS | collection={collection_name} | "
            f"page={page} | cache_check_time={t1-t0:.3f}s"
        )

        t2 = time.time()
        formulas = await asyncio.wait_for(
            listar_formulas_customizadas(),
            timeout=get_mongo_query_timeout(),
        )
        t3 = time.time()
        log.info(
            f"[IBGE V2] Formulas carregadas | collection={collection_name} | "
            f"qtd={len(formulas)} | time={t3-t2:.3f}s"
        )

        formula_dependencies = _extract_formula_dependencies(formulas)

        projection = _build_projection(
            columns,
            extra_columns=["cd_setor", *formula_dependencies],
        )
        collection = database[collection_name]

        t4 = time.time()
        documentos = await asyncio.wait_for(
            asyncio.to_thread(
                _executar_consulta_mongo,
                collection,
                query,
                projection,
                skip,
                limit,
            ),
            timeout=get_mongo_query_timeout(),
        )
        t5 = time.time()
        log.info(
            f"[IBGE V2] Query MongoDB | collection={collection_name} | "
            f"page={page} | skip={skip} | docs_retornados={len(documentos)} | "
            f"time={t5-t4:.3f}s"
        )

        t6 = time.time()
        payload_rows = []
        for documento in documentos:
            documento.pop("_id", None)
            documento["cd_setor"] = documento.get("cd_setor")
            payload_rows.append(
                await aplicar_formulas_customizadas(
                    documento, formulas=formulas, collection_name=collection_name
                )
            )
        t7 = time.time()
        log.info(
            f"[IBGE V2] Aplicar formulas | collection={collection_name} | "
            f"docs_qtd={len(payload_rows)} | time={t7-t6:.3f}s"
        )

        response = {
            "collection_name": collection_name,
            "columns": columns,
            "cd_setor": cd_setor_list,
            "page": page,
            "limit": limit,
            "payload": payload_rows,
        }

        t10 = time.time()
        try:
            validated = IbgeMongoQueryResponse(**response)
            if validated.total_records == 0 or len(validated.payload) > 0:
                await set_cached_query_response(query_signature, response)
        except Exception:
            pass
        t11 = time.time()
        log.info(
            f"[IBGE V2] Cache write | collection={collection_name} | "
            f"page={page} | time={t11-t10:.3f}s"
        )

        total_time = time.time() - request_start
        log.info(
            f"[IBGE V2] Consulta finalizada | collection={collection_name} | "
            f"page={page} | docs={len(payload_rows)} | total_time={total_time:.3f}s"
        )

        return response
    finally:
        client.close()
