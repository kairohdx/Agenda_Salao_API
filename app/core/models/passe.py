from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pytz import timezone

from ..database.database import Base

class Passe(Base):
    __tablename__ = 'passe'

    id = Column(Integer, primary_key=True)
    passe = Column(String(256), nullable=False)
    tipo_funcionario = Column(String())

    funcionario_id = Column(Integer)
    funcionario = relationship('Funcionario', backref=backref('tarefas', lazy=True))

    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    
    funcionario = relationship('Cliente', backref=backref('passe', lazy=True))

    dataHoraCriacao = Column(DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))

    