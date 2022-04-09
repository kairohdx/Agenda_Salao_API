from datetime import datetime
from pytz import timezone
from app import db

class Servico(db.Model):
    __tablename__ = 'servico'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    tempoAtendimento = db.Column(db.Integer, nullable=False)
    intervaloAtendimento = db.Column(db.Integer, nullable=False)

    dataHoraCriacao = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))

    