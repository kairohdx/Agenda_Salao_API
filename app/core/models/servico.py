from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text, DateTime, Float
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pytz import timezone

from ..database.database import Base

servico_funcionario = Table('servicoFuncionario', Base.metadata,
    Column('servico_id', ForeignKey('servico.id')),
    Column('funcionario_id', ForeignKey('funcionario.id'))
)

class Servico(Base):
    __tablename__ = 'servico'

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    tempoAtendimento = Column(Integer, nullable=False)
    intervaloAtendimento = Column(Float)

    empresa_id = Column(Integer, ForeignKey('empresa.id'), nullable=False)
    empresa = relationship('Empresa', backref='servicos')

    funcionarios = relationship('Funcionario', secondary=servico_funcionario, backref='servicos')

    dataHoraCriacao = Column(DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))

    