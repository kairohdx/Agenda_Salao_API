from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pytz import timezone

from ..database.database import Base

grupo_funcionario = Table('grupoFuncionario', Base.metadata,
    Column('grupo_id', ForeignKey('grupo.id')),
    Column('funcionario_id', ForeignKey('funcionario.id'))
)

grupo_servico = Table('grupoServico', Base.metadata,
    Column('grupo_id', ForeignKey('grupo.id')),
    Column('servico_id', ForeignKey('servico.id'))
)

class Grupo(Base):
    __tablename__ = 'grupo'
    id = Column(Integer, primary_key=True)
    nome = Column(String(256), nullable=False)

    empresa_id = Column(Integer, ForeignKey('empresa.id'), nullable=False)
    empresa = relationship('Empresa', backref='grupos')

    funcionarios = relationship('Funcionario', secondary=grupo_funcionario, backref='grupos')
    servicos = relationship('Servico', secondary=grupo_servico, backref='grupos')

    dataHoraCriacao = Column(DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
