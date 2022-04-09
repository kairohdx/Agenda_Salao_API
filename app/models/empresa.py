from datetime import datetime
from pytz import timezone
from app import db


class Empresa(db.Model):
    __tablename__ = 'empresa'

    id = db.Column(db.Integer, primary_key=True)
    
    
    dataHoraCriacao = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
