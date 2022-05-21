from http import client
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from pytz import timezone

from ..database.database import Base

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True)
    nome = Column(String(256))
    email = Column(String(256), nullable=False)
    hashSenha = Column(Text)
    loginSocial = Column(Boolean, default=False)

    dataHoraCriacao = Column(DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
