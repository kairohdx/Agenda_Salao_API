from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel

from app.core.schemas.funcionario import FuncionarioBase
from app.core.schemas.grupo import GrupoBase
from app.core.schemas.servico import ServicoBase


class EmpresaLogoBase(BaseModel):
    blob: Any


class EmpresaLogoCreate(EmpresaLogoBase):
    pass


class EmpresaLogo(EmpresaLogoBase):
    id: int

    class Config:
        orm_mode = True


class EmpresaBase(BaseModel):
    id: int | None
    nome: str
    descricao: str | None = None

    class Config:
        orm_mode = True


class EmpresaCreate(EmpresaBase):
    docNum: str


class Empresa(EmpresaBase):
    empresaAtiva: bool
    empresaLogo: EmpresaLogo | None
    docNum: str
    funncionarios: List[FuncionarioBase] = []
    servicos: List[ServicoBase] = []
    grupos: List[GrupoBase] = []

    class Config:
        orm_mode = True