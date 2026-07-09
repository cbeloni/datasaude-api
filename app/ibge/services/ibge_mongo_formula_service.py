import asyncio
import ast
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional

from bson import ObjectId

from api.ibge.v2.request.ibge import IbgeFormulaCustomizadaCreate
from core.exceptions import BadRequestException, NotFoundException
from core.mongo import get_mongo_client, get_mongo_database, get_mongo_query_timeout


FORMULA_COLLECTION_NAME = "ibge_formulas"
_ALLOWED_BIN_OPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod)
_ALLOWED_UNARY_OPS = (ast.UAdd, ast.USub)


def _sanitize_formula_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def _safe_eval_formula(expression: str, values: dict):
    normalized_values = {str(key).lower(): value for key, value in values.items()}

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Num):
            return Decimal(str(node.n))
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return Decimal(str(node.value))
        if isinstance(node, ast.BinOp) and isinstance(node.op, _ALLOWED_BIN_OPS):
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                return left / right
            if isinstance(node.op, ast.Pow):
                return left ** right
            if isinstance(node.op, ast.Mod):
                return left % right
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, _ALLOWED_UNARY_OPS):
            value = _eval(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.Name):
            raw_value = values.get(node.id)
            if raw_value is None:
                raw_value = normalized_values.get(node.id.lower())
            if raw_value is None:
                return Decimal("0")
            return Decimal(str(raw_value))
        raise ValueError("expressão inválida")

    tree = ast.parse(expression, mode="eval")
    return _eval(tree)


def _serialize_formula(document: Dict) -> Dict:
    return {
        "id": str(document.get("_id")),
        "nome": document.get("nome"),
        "formula": document.get("formula"),
        "ativa": document.get("ativa", True),
        "created_at": document.get("created_at"),
        "updated_at": document.get("updated_at"),
    }


def _get_formula_collection(database):
    return database[FORMULA_COLLECTION_NAME]


def _listar_formulas_sync() -> List[Dict]:
    """Versão síncrona para ser executada via asyncio.to_thread."""
    try:
        client = get_mongo_client()
    except ValueError as exc:
        raise BadRequestException(str(exc)) from exc

    try:
        database = get_mongo_database(client)
        if database is None:
            raise BadRequestException("Database MongoDB não configurado")

        query = {"ativa": True}
        rows = list(
            _get_formula_collection(database)
            .find(query)
            .sort("nome", 1)
        )
        return [_serialize_formula(row) for row in rows]
    finally:
        client.close()


def _criar_formula_sync(payload: IbgeFormulaCustomizadaCreate) -> Dict:
    """Versão síncrona para ser executada via asyncio.to_thread."""
    try:
        client = get_mongo_client()
    except ValueError as exc:
        raise BadRequestException(str(exc)) from exc

    try:
        database = get_mongo_database(client)
        if database is None:
            raise BadRequestException("Database MongoDB não configurado")

        collection = _get_formula_collection(database)
        formula_nome = payload.nome.strip()
        formula_expressao = payload.formula.strip()

        existing = collection.find_one({"nome": formula_nome, "ativa": True})
        if existing is not None:
            raise BadRequestException("Fórmula customizada já cadastrada")

        now = datetime.utcnow()
        document = {
            "nome": formula_nome,
            "formula": formula_expressao,
            "ativa": True,
            "created_at": now,
            "updated_at": now,
        }
        result = collection.insert_one(document)
        document["_id"] = result.inserted_id
        return _serialize_formula(document)
    finally:
        client.close()


def _remover_formula_sync(formula_id: str):
    """Versão síncrona para ser executada via asyncio.to_thread."""
    try:
        client = get_mongo_client()
    except ValueError as exc:
        raise BadRequestException(str(exc)) from exc

    try:
        database = get_mongo_database(client)
        if database is None:
            raise BadRequestException("Database MongoDB não configurado")

        collection = _get_formula_collection(database)
        try:
            object_id = ObjectId(formula_id)
        except Exception as exc:
            raise BadRequestException("ID da fórmula inválido") from exc

        result = collection.delete_one({"_id": object_id})
        if result.deleted_count == 0:
            raise NotFoundException("Fórmula não encontrada")
    finally:
        client.close()


async def listar_formulas_customizadas() -> List[Dict]:
    return await asyncio.wait_for(
        asyncio.to_thread(_listar_formulas_sync),
        timeout=get_mongo_query_timeout(),
    )


async def criar_formula_customizada(payload: IbgeFormulaCustomizadaCreate):
    return await asyncio.wait_for(
        asyncio.to_thread(_criar_formula_sync, payload),
        timeout=get_mongo_query_timeout(),
    )


async def remover_formula_customizada(formula_id: str):
    await asyncio.wait_for(
        asyncio.to_thread(_remover_formula_sync, formula_id),
        timeout=get_mongo_query_timeout(),
    )


async def aplicar_formulas_customizadas(payload: dict, formulas: Optional[List[Dict]] = None):
    active_formulas = formulas if formulas is not None else await listar_formulas_customizadas()
    for formula in active_formulas:
        field_name = _sanitize_formula_name(formula["nome"])
        try:
            result = _safe_eval_formula(formula["formula"], payload)
            payload[field_name] = result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except Exception:
            payload[field_name] = None

    return payload
