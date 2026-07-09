import asyncio
import ast
from math import ceil
from typing import Dict, List

from pymongo.cursor import Cursor

from api.ibge.v2.request.ibge import IbgeMongoQueryRequest
from app.ibge.services.ibge_mongo_formula_service import (
    aplicar_formulas_customizadas,
    listar_formulas_customizadas,
)
from core.exceptions import BadRequestException
from core.mongo import get_mongo_client, get_mongo_database


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
) -> tuple:
    """Executa a consulta MongoDB de forma síncrona (para ser chamada via to_thread)."""
    total_records = collection.count_documents(query)
    cursor: Cursor = (
        collection.find(query, projection)
        .sort("_id", 1)
        .skip(skip)
        .limit(limit)
    )
    documentos = list(cursor)
    return total_records, documentos


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

    try:
        client = get_mongo_client()
    except ValueError as exc:
        raise BadRequestException(str(exc)) from exc

    try:
        database = get_mongo_database(client)
        if database is None:
            raise BadRequestException("Database MongoDB não configurado")

        formulas = await asyncio.wait_for(
            listar_formulas_customizadas(),
            timeout=30.0,
        )
        formula_dependencies = _extract_formula_dependencies(formulas)

        query = {}
        if payload.cd_setor:
            query["cd_setor"] = payload.cd_setor.strip()

        projection = _build_projection(
            columns,
            extra_columns=["cd_setor", *formula_dependencies],
        )
        collection = database[collection_name]

        total_records, documentos = await asyncio.wait_for(
            asyncio.to_thread(
                _executar_consulta_mongo,
                collection,
                query,
                projection,
                skip,
                limit,
            ),
            timeout=30.0,
        )

        payload_rows = []
        for documento in documentos:
            documento.pop("_id", None)
            documento["cd_setor"] = documento.get("cd_setor")
            payload_rows.append(
                await aplicar_formulas_customizadas(documento, formulas=formulas)
            )

        return {
            "collection_name": collection_name,
            "columns": columns,
            "cd_setor": query.get("cd_setor"),
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": ceil(total_records / limit) if total_records else 0,
            "payload": payload_rows,
        }
    finally:
        client.close()
