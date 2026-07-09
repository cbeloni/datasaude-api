from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class IbgeMongoQueryRequest(BaseModel):
    collection_name: str = Field(..., description="Nome da collection MongoDB")
    columns: List[str] = Field(..., description="Colunas que devem ser retornadas")
    cd_setor: Optional[str] = Field(
        None,
        description="Filtro opcional por cd_setor",
    )
    page: int = Field(
        1,
        ge=1,
        description="Página desejada",
    )
    limit: int = Field(
        10,
        ge=1,
        le=1000,
        description="Quantidade de registros por página",
    )


class IbgeMongoQueryResponse(BaseModel):
    collection_name: str = Field(..., description="Nome da collection MongoDB")
    columns: List[str] = Field(..., description="Colunas retornadas na consulta")
    cd_setor: Optional[str] = Field(
        None,
        description="Filtro aplicado por cd_setor",
    )
    page: int = Field(..., description="Página atual")
    limit: int = Field(..., description="Quantidade de registros por página")
    total_records: int = Field(..., description="Quantidade total de documentos")
    total_pages: int = Field(..., description="Total de páginas")
    payload: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Documentos retornados com projeção dinâmica",
    )


class IbgeFormulaCustomizadaBase(BaseModel):
    id: Optional[str] = None
    nome: str
    formula: str
    ativa: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class IbgeFormulaCustomizadaCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=120)
    formula: str = Field(..., min_length=1, max_length=500)


class IbgeFormulaCustomizadaListResponse(BaseModel):
    payload: List[IbgeFormulaCustomizadaBase] = Field(
        default_factory=list,
        description="Lista de fórmulas customizadas",
    )
