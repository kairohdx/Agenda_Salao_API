from datetime import datetime
from pytz import timezone
from app import db, app
import uuid


class Grupo(db.Model):
    __tablename__ = 'grupo'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(256), nullable=False)

    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
    empresa = db.relationship('Empresa', backref=db.backref('grupos', lazy=True))

    dataHoraCriacao = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(256), nullable=False)
    nomeUsuario = db.Column(db.String(24), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    hashSenha = db.Column(db.Text)
    loginSocial = db.Column(db.Boolean, default=False)
    administrador = db.Column(db.Boolean, default=False)

    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
    empresa = db.relationship('Empresa', backref=db.backref('usuarios', lazy=True))

    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'), nullable=False)
    grupo = db.relationship('Grupo', backref=db.backref('usuarios', lazy=True))

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