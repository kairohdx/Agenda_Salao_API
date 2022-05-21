from collections import UserList
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pytz import timezone

from ..database.database import Base


class Tarefa(Base):
    __tablename__ = 'tarefa'

    id = Column(Integer, primary_key=True)
    agendadoPara = Column(DateTime, nullable=False)
    terminoPrevistoPara = Column(DateTime, nullable=False)
    concluido = Column(Boolean, default=False)

    agenda_id = Column(Integer, ForeignKey('agenda.id'), nullable=False)
    agenda = relationship('Agenda', backref='tarefas')

    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    cliente = relationship('Cliente',  backref='tarefas', uselist=False)

    servico_id = Column(Integer, ForeignKey('servico.id'), nullable=False)
    servico = relationship('Servico',  backref='tarefas')

    dataHoraCriacao = Column(DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
