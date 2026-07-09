import os
from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConfigurationError

from core.config import config


def get_mongo_uri() -> Optional[str]:
    return os.environ.get("MONGODB_URI") or os.environ.get("MONGO_URI") or config.MONGODB_URI


def get_mongo_query_timeout() -> float:
    """Timeout em segundos para operacoes MongoDB. Lê da env MONGODB_QUERY_TIMEOUT, default 60."""
    raw = os.environ.get("MONGODB_QUERY_TIMEOUT") or "60"
    try:
        return float(raw)
    except (ValueError, TypeError):
        return 60.0


def get_mongo_client() -> MongoClient:
    uri = get_mongo_uri()
    if not uri:
        raise ValueError("MONGODB_URI não configurada")
    return MongoClient(uri, serverSelectionTimeoutMS=5000)


def get_mongo_database(client: MongoClient) -> Optional[Database]:
    database_name = os.environ.get("MONGODB_DATABASE") or os.environ.get("MONGO_DB")
    if database_name:
        return client[database_name]

    try:
        return client.get_default_database()
    except ConfigurationError:
        return None
