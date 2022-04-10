from datetime import datetime
from pytz import timezone
from app import db


class Tarefa(db.Model):
    __tablename__ = 'tarefa'

    id = db.Column(db.Integer, primary_key=True)
    agendadoPara = db.Column(db.DateTime, nullable=False)
    terminoPrevistoPara = db.Column(db.DateTime, nullable=False)
    concluido = db.Column(db.Boolean, default=False)

    agenda_id = db.Column(db.Integer, db.ForeignKey('agenda.id'), nullable=False)
    agenda = db.relationship('Agenda', backref=db.backref('tarefas', lazy=True))

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cliente = db.relationship('Cliente', backref=db.backref('tarefas', lazy=True))

    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)
    servico = db.relationship('Servico', backref=db.backref('tarefas', lazy=True))

    dataHoraCriacao = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))
