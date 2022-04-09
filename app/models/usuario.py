from datetime import datetime
from pytz import timezone
from app import db, app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import uuid

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(256), nullable=False)
    nomeUsuario = db.Column(db.String(24), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    hashSenha = db.Column(db.Text)
    loginSocial = db.Column(db.Boolean, default=False)

    dataHoraCriacao = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))

    def generate_token(self, token_key, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'token': self.id, })

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None, True # token valido, porem expirado
        except BadSignature:
            return None, False # token invalido'''
        user = Usuario.query.get(data['token'])
        return user, True