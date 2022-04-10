from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app.models.agenda import Agenda
from app.models.cliente import Cliente
from app.models.empresa import Empresa, EmpresaLogo
from app.models.pagamento import Pagamento
from app.models.servico import Servico
from app.models.tarefa import Tarefa
from app.models.usuario import Usuario, Grupo
