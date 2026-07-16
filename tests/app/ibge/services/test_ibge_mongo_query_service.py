import importlib.util
import json
import sys
import types
from pathlib import Path
from types import SimpleNamespace

import pytest


class FakeCursor:
    def __init__(self, rows):
        self.rows = rows

    def sort(self, *args, **kwargs):
        return self

    def skip(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    def __iter__(self):
        return iter(self.rows)


class FakeCollection:
    def __init__(self):
        self.count_calls = 0
        self.find_calls = 0

    def count_documents(self, query):
        self.count_calls += 1
        return 42

    def find(self, query, projection):
        self.find_calls += 1
        return FakeCursor(
            [
                {
                    "cd_setor": "123",
                    "v1": 10,
                }
            ]
        )


def _register_module(name, attributes=None):
    module = types.ModuleType(name)
    module.__path__ = []
    if attributes:
        for key, value in attributes.items():
            setattr(module, key, value)
    sys.modules[name] = module
    return module


def _load_query_service_module():
    root_dir = Path(__file__).resolve().parents[4]
    service_path = root_dir / "app/ibge/services/ibge_mongo_query_service.py"

    class BadRequestException(Exception):
        pass

    class NotFoundException(Exception):
        pass

    _register_module("app")
    _register_module("app.ibge")
    _register_module("app.ibge.services")
    _register_module(
        "app.ibge.services.ibge_mongo_cache_service",
        {
            "get_cached_collection_count": lambda *args, **kwargs: None,
            "get_cached_query_response": lambda *args, **kwargs: None,
            "set_cached_collection_count": lambda *args, **kwargs: None,
            "set_cached_query_response": lambda *args, **kwargs: None,
        },
    )
    _register_module(
        "app.ibge.services.ibge_mongo_formula_service",
        {
            "aplicar_formulas_customizadas": lambda payload, formulas=None: payload,
            "listar_formulas_customizadas": lambda: [],
        },
    )
    _register_module("api")
    _register_module("api.ibge")
    _register_module("api.ibge.v2")
    _register_module("api.ibge.v2.request")
    _register_module(
        "api.ibge.v2.request.ibge",
        {"IbgeMongoQueryRequest": object},
    )
    _register_module("core")
    _register_module(
        "core.exceptions",
        {
            "BadRequestException": BadRequestException,
            "NotFoundException": NotFoundException,
        },
    )
    _register_module(
        "core.mongo",
        {
            "get_mongo_client": lambda: SimpleNamespace(close=lambda: None),
            "get_mongo_database": lambda client: None,
            "get_mongo_query_timeout": lambda: 5.0,
        },
    )
    _register_module("pymongo")
    _register_module("pymongo.cursor", {"Cursor": object})

    spec = importlib.util.spec_from_file_location(
        "app.ibge.services.ibge_mongo_query_service",
        service_path,
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


service = _load_query_service_module()


@pytest.fixture
def cached_query_setup(monkeypatch):
    cache = {}
    collection = FakeCollection()
    database = {"setores_alfabetizacao_br": collection}

    async def fake_get_cached_query_response(signature):
        return cache.get(("query", json.dumps(signature, sort_keys=True, default=str)))

    async def fake_set_cached_query_response(signature, response):
        cache[("query", json.dumps(signature, sort_keys=True, default=str))] = response

    async def fake_get_cached_collection_count(signature):
        return cache.get(("count", json.dumps(signature, sort_keys=True, default=str)))

    async def fake_set_cached_collection_count(signature, total_records):
        cache[("count", json.dumps(signature, sort_keys=True, default=str))] = total_records

    async def fake_listar_formulas_customizadas():
        return []

    async def fake_aplicar_formulas_customizadas(payload, formulas=None):
        return payload

    monkeypatch.setattr(service, "get_cached_query_response", fake_get_cached_query_response)
    monkeypatch.setattr(service, "set_cached_query_response", fake_set_cached_query_response)
    monkeypatch.setattr(service, "get_cached_collection_count", fake_get_cached_collection_count)
    monkeypatch.setattr(service, "set_cached_collection_count", fake_set_cached_collection_count)
    monkeypatch.setattr(service, "listar_formulas_customizadas", fake_listar_formulas_customizadas)
    monkeypatch.setattr(service, "aplicar_formulas_customizadas", fake_aplicar_formulas_customizadas)
    monkeypatch.setattr(
        service,
        "get_mongo_client",
        lambda: SimpleNamespace(close=lambda: None),
    )
    monkeypatch.setattr(service, "get_mongo_database", lambda client: database)
    monkeypatch.setattr(service, "get_mongo_query_timeout", lambda: 5.0)

    return collection


@pytest.mark.asyncio
async def test_consultar_colecao_mongo_cacheia_resposta_repetida(cached_query_setup):
    payload = SimpleNamespace(
        collection_name="setores_alfabetizacao_br",
        columns=["cd_setor", "v1"],
        cd_setor=None,
        page=1,
        limit=10,
    )

    first_response = await service.consultar_colecao_mongo(payload)
    second_response = await service.consultar_colecao_mongo(payload)

    assert first_response == second_response
    assert cached_query_setup.count_calls == 1
    assert cached_query_setup.find_calls == 1


@pytest.mark.asyncio
async def test_consultar_colecao_mongo_reusa_cache_de_count_entre_paginas(
    cached_query_setup,
):
    first_payload = SimpleNamespace(
        collection_name="setores_alfabetizacao_br",
        columns=["cd_setor", "v1"],
        cd_setor=None,
        page=1,
        limit=10,
    )
    second_payload = SimpleNamespace(
        collection_name="setores_alfabetizacao_br",
        columns=["cd_setor", "v1"],
        cd_setor=None,
        page=2,
        limit=10,
    )

    await service.consultar_colecao_mongo(first_payload)
    await service.consultar_colecao_mongo(second_payload)

    assert cached_query_setup.count_calls == 1
    assert cached_query_setup.find_calls == 2
