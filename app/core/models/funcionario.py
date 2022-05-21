from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pytz import timezone

from ..database.database import Base


class Funcionario(Base):
    __tablename__ = 'funcionario'
    id = Column(Integer, primary_key=True)
    nome = Column(String(256))
    email = Column(String(256), nullable=False, unique=True)
    hashSenha = Column(Text)
    loginSocial = Column(Boolean, default=False)
    administrador = Column(Boolean, default=False)

    empresa_id = Column(Integer, ForeignKey('empresa.id'), nullable=False)
    empresa = relationship('Empresa', backref='funcionarios')

    dataHoraCriacao = Column(DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
