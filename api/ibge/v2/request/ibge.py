from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class IbgeMongoQueryRequest(BaseModel):
    collection_name: str = Field(..., description="Nome da collection MongoDB")
    columns: List[str] = Field(..., description="Colunas que devem ser retornadas")
    cd_setor: Optional[List[str]] = Field(
        None,
        description="Filtro opcional por lista de cd_setor",
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
    cd_setor: Optional[List[str]] = Field(
        None,
        description="Filtro aplicado por lista de cd_setor",
    )
    page: int = Field(..., description="Página atual")
    limit: int = Field(..., description="Quantidade de registros por página")
    payload: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Documentos retornados com projeção dinâmica",
    )

    @validator("cd_setor", pre=True)
    def normalize_cd_setor(cls, value):
        """Handle cached responses where cd_setor may still be a string."""
        if isinstance(value, str):
            return [value] if value else None
        return value


class IbgeFormulaCustomizadaBase(BaseModel):
    id: Optional[str] = None
    nome: str
    formula: str
    collection_name: Optional[str] = None
    ativa: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class IbgeFormulaCustomizadaCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=120)
    formula: str = Field(..., min_length=1, max_length=500)
    collection_name: Optional[str] = Field(None, max_length=120)


class IbgeFormulaCustomizadaListResponse(BaseModel):
    payload: List[IbgeFormulaCustomizadaBase] = Field(
        default_factory=list,
        description="Lista de fórmulas customizadas",
    )