from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pytz import timezone

from ..database.database import Base


class Agenda(Base):
    __tablename__ = 'agenda'

    id = Column(Integer, primary_key=True)

    maximoTarefas = Column(Integer)

    funcionario_id = Column(Integer, ForeignKey('funcionario.id'), nullable=False)
    funcionario = relationship('Funcionario', backref="agenda", uselist=False)


    dataHoraCriacao = Column(DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
