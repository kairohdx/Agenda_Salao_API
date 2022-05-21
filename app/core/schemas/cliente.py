from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel

from app.core.schemas.tarefa import Tarefa


class ClienteBase(BaseModel):
    email: str

    class Config:
        orm_mode = True


class ClienteCreate(ClienteBase):
    hashSenha: str | None = None


class Cliente(ClienteBase):
    id: int
    nome: str | None
    loginSocial: bool = False
    tarefas: list[Tarefa] =  []

    class Config:
        orm_mode = True