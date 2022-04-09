from datetime import datetime
from pytz import timezone
from app import db


class Pagamento(db.Model):
    __tablename__ = 'pagamento'

    id = db.Column(db.Integer, primary_key=True)
    formaPagamento = db.Column(db.String(256))
    pagamentoRealizado = db.Column(db.Boolean, default=False)

    dataHoraCriacao = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))