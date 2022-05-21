from datetime import datetime, timedelta

from pydantic import BaseModel


class ServicoBase(BaseModel):
    id: int | None
    nome: str
    descricao: str | None = None

    class Config:
        orm_mode = True


class ServicoCreate(ServicoBase):
    tempoAtendimento: int = 1800
    intervaloAtendimento: int = 0


class Servico(ServicoBase):    
    id_empresa:int
    tempoAtendimento: timedelta
    intervaloAtendimento:timedelta = timedelta(0)

    class Config:
        orm_mode = True


class AtribuirServico(BaseModel):
    servico_id: int
    funcionario_id: int | None = None
    grupo_id: int | None = None


class HorarioDisponivel(BaseModel):
    ini: datetime
    fim: datetime | None
