from datetime import datetime
from pytz import timezone
from app import db


class Agenda(db.Model):
    __tablename__ = 'agenda'

    id = db.Column(db.Integer, primary_key=True)
    
    color1 = db.Column(db.string(7))
    color2 = db.Column(db.string(7))
    color3 = db.Column(db.string(7))
    maximoTarefas = db.Column(db.Integer)
    
    dataHoraCriacao = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
