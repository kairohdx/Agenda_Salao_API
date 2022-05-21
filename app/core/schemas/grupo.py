from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel
from app.core.schemas.servico import Servico
from app.core.schemas.funcionario import Funcionario


class GrupoBase(BaseModel):
    nome: str

    class Config:
        orm_mode = True


class GrupoCreate(GrupoBase):
    pass


class Grupo(GrupoBase):
    id: int
    empresa_id: int
    funcionarios:list[Funcionario]
    servicos:list[Servico]
    

    class Config:
        orm_mode = True

class AtribuirGrupo(BaseModel):
    grupo_id: int
    funcionario_id: int | None = None
