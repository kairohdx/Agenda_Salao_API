from datetime import datetime
from pytz import timezone
from app import db


class Tarefa(db.Model):
    __tablename__ = 'tarefa'

    id = db.Column(db.Integer, primary_key=True)
    agendadoPara = db.Column(db.DateTime, nullable=False)
    terminoPrevistoPara = db.Column(db.DateTime, nullable=False)

    dataHoraCriacao = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
