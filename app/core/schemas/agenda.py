from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel
from app.core.schemas.tarefa import Tarefa


class AgendaBase(BaseModel):
    tarefas: list[Tarefa] = []
    
    class Config:
        orm_mode = True


class AgendaCreate(AgendaBase):
    maximoTarefas: int


class Agenda(AgendaBase):
    id: int
    maximoTarefas: int    
    funcionario_id: int

    class Config:
        orm_mode = True
