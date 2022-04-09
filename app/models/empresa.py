from datetime import datetime
from pytz import timezone
from app import db


class Empresa(db.Model):
    __tablename__ = 'empresa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(256), nullable=False)
    descricao = db.Column(db.Text)
    docNum = db.Column(db.String(20), nullable=False, unique=True)
    empresaAtiva = db.Column(db.Boolean, default=True)
    
    dataHoraCriacao = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))


class EmpresaLogo(db.Model):
    __tablename__ = 'empresaLogo'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Blob)

    dataHoraCriacao = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
