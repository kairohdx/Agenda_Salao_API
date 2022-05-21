from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel

from app.core.schemas.agenda import Agenda


class FuncionarioParaCliente(BaseModel):
    nome: str | None
    id : int

    class Config:
        orm_mode = True


class FuncionarioBase(BaseModel):
    nome: str | None
    email: str
    administrador: bool = False

    class Config:
        orm_mode = True


class FuncionarioCreate(FuncionarioBase):
    hashSenha: str


class Funcionario(FuncionarioBase):
    id: int
    agenda: Agenda | None
    loginSocial: bool | None
    empresa_id: int
    

    class Config:
        orm_mode = True
