import hashlib
import json
import pickle
from typing import Any, Dict, Iterable, List, Optional

from core.helpers.redis import redis

IBGE_V2_CACHE_TTL_SECONDS = 60 * 60 * 24 * 30
IBGE_V2_QUERY_CACHE_PREFIX = "ibge:v2:query"
IBGE_V2_COUNT_CACHE_PREFIX = "ibge:v2:count"
IBGE_V2_FORMULAS_CACHE_PREFIX = "ibge:v2:formulas"


def _build_cache_key(prefix: str, payload: Dict[str, Any]) -> str:
    normalized_payload = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    )
    digest = hashlib.sha256(normalized_payload.encode("utf-8")).hexdigest()
    return f"{prefix}::{digest}"


async def _get_cached_value(key: str) -> Optional[Any]:
    try:
        cached_value = await redis.get(key)
        if cached_value is None:
            return None
        return pickle.loads(cached_value)
    except Exception:
        return None


async def _set_cached_value(key: str, value: Any, ttl: int = IBGE_V2_CACHE_TTL_SECONDS) -> None:
    try:
        await redis.set(name=key, value=pickle.dumps(value), ex=ttl)
    except Exception:
        return None


async def _delete_prefix(prefix: str) -> None:
    try:
        async for key in redis.scan_iter(f"{prefix}::*"):
            await redis.delete(key)
    except Exception:
        return None


async def get_cached_query_response(signature: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    cache_key = _build_cache_key(IBGE_V2_QUERY_CACHE_PREFIX, signature)
    return await _get_cached_value(cache_key)


async def set_cached_query_response(
    signature: Dict[str, Any],
    response: Dict[str, Any],
) -> None:
    cache_key = _build_cache_key(IBGE_V2_QUERY_CACHE_PREFIX, signature)
    await _set_cached_value(cache_key, response)


async def clear_query_cache() -> None:
    await _delete_prefix(IBGE_V2_QUERY_CACHE_PREFIX)


async def get_cached_collection_count(signature: Dict[str, Any]) -> Optional[int]:
    cache_key = _build_cache_key(IBGE_V2_COUNT_CACHE_PREFIX, signature)
    cached_value = await _get_cached_value(cache_key)
    if cached_value is None:
        return None
    try:
        return int(cached_value)
    except (TypeError, ValueError):
        return None


async def set_cached_collection_count(
    signature: Dict[str, Any],
    total_records: int,
) -> None:
    cache_key = _build_cache_key(IBGE_V2_COUNT_CACHE_PREFIX, signature)
    await _set_cached_value(cache_key, int(total_records))


async def get_cached_formulas() -> Optional[List[Dict[str, Any]]]:
    cache_key = _build_cache_key(
        IBGE_V2_FORMULAS_CACHE_PREFIX,
        {"scope": "active"},
    )
    cached_value = await _get_cached_value(cache_key)
    return cached_value if isinstance(cached_value, list) else None


async def set_cached_formulas(formulas: Iterable[Dict[str, Any]]) -> None:
    cache_key = _build_cache_key(
        IBGE_V2_FORMULAS_CACHE_PREFIX,
        {"scope": "active"},
    )
    await _set_cached_value(cache_key, list(formulas))


async def clear_formulas_cache() -> None:
    await _delete_prefix(IBGE_V2_FORMULAS_CACHE_PREFIX)


async def clear_ibge_v2_query_related_cache() -> None:
    await clear_query_cache()
    await clear_formulas_cache()
