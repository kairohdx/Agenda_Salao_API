from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class TarefaBase(BaseModel):
    agendadoPara: datetime
    terminoPrevistoPara: datetime | None = None
    concluido: bool | None = False

    class Config:
        orm_mode = True


class TarefaCreate(TarefaBase):
    pass


class Tarefa(TarefaBase):
    id: int
    agenda_id: int
    cliente_id: int
    servico_id: int


    class Config:
        orm_mode = True
