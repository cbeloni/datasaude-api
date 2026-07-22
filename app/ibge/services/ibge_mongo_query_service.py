import asyncio
import ast
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

        query_signature = _build_query_signature(
            collection_name=collection_name,
            columns=columns,
            page=page,
            limit=limit,
            query=query,
        )
        cached_response = await get_cached_query_response(query_signature)
        if cached_response is not None:
            if isinstance(cached_response.get("cd_setor"), str):
                cached_response["cd_setor"] = (
                    [cached_response["cd_setor"]] if cached_response["cd_setor"] else None
                )
            cached_payload = cached_response.get("payload", [])
            cached_total = cached_response.get("total_records", 0)
            if not (cached_total > 0 and len(cached_payload) == 0):
                return cached_response

        formulas = await asyncio.wait_for(
            listar_formulas_customizadas(),
            timeout=get_mongo_query_timeout(),
        )
        formula_dependencies = _extract_formula_dependencies(formulas)

        projection = _build_projection(
            columns,
            extra_columns=["cd_setor", *formula_dependencies],
        )
        collection = database[collection_name]

        count_signature = _build_count_signature(collection_name, query)
        total_records = await get_cached_collection_count(count_signature)
        if total_records is None:
            total_records = await asyncio.wait_for(
                asyncio.to_thread(
                    _contar_documentos_mongo,
                    collection,
                    query,
                ),
                timeout=get_mongo_query_timeout(),
            )
            await set_cached_collection_count(count_signature, total_records)

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

        payload_rows = []
        for documento in documentos:
            documento.pop("_id", None)
            documento["cd_setor"] = documento.get("cd_setor")
            payload_rows.append(
                await aplicar_formulas_customizadas(
                    documento, formulas=formulas, collection_name=collection_name
                )
            )

        response = {
            "collection_name": collection_name,
            "columns": columns,
            "cd_setor": cd_setor_list,
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": ceil(total_records / limit) if total_records else 0,
            "payload": payload_rows,
        }

        try:
            validated = IbgeMongoQueryResponse(**response)
            if validated.total_records == 0 or len(validated.payload) > 0:
                await set_cached_query_response(query_signature, response)
        except Exception:
            pass

        return response
    finally:
        client.close()
