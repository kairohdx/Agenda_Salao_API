from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, BLOB, Time
from sqlalchemy.orm import relationship
from datetime import datetime, time
from pytz import timezone

from ..database.database import Base


class Empresa(Base):
    __tablename__ = 'empresa'

    id = Column(Integer, primary_key=True)
    nome = Column(String(256), nullable=False)
    descricao = Column(Text)
    docNum = Column(String(20), nullable=False, unique=True)
    empresaAtiva = Column(Boolean, default=True)
    empresaHorarioAbertura = Column(Time, default=time(hour=6, minute=00))
    empresaHorarioFechamento = Column(Time, default=time(hour=18, minute=00))
    
    dataHoraCriacao = Column(DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))



class EmpresaLogo(Base):
    __tablename__ = 'empresaLogo'

    id = Column(Integer, primary_key=True)
    data = Column(BLOB)

    dataHoraCriacao = Column(DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
