from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class PasseBase(BaseModel):
    passe: str

    class Config:
        orm_mode = True


class PasseCreate(PasseBase):
    pass


class Passe(PasseBase):
    id: int
    tipo_funcionario: str

    funcionario_id: int | None
    cliente_id: int | None
    

    class Config:
        orm_mode = True