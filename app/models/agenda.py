from datetime import datetime
from pytz import timezone
from app import db


class Agenda(db.Model):
    __tablename__ = 'agenda'

    id = db.Column(db.Integer, primary_key=True)
    
    color1 = db.Column(db.String(7))
    color2 = db.Column(db.String(7))
    color3 = db.Column(db.String(7))
    maximoTarefas = db.Column(db.Integer)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'),
        nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('agenda', lazy=True, uselist=False), uselist=False)
    
    dataHoraCriacao = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
