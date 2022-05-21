from datetime import datetime, timedelta
from sqlalchemy import func, not_
from sqlalchemy.orm import Session
from sqlalchemy.dialects import sqlite

from app.core.app.agenda import novo_agenda
from app.core.models.agenda import Agenda
from app.core.models.servico import Servico
from app.core.models.tarefa import Tarefa
from app.core.schemas.agenda import AgendaCreate

from ..models.funcionario import Funcionario
from ..schemas.funcionario import FuncionarioCreate

async def funcionario_por_id(db: Session, funcionario_id: int):
   return db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()

async def funcionario_por_email(db: Session, email: int):
    return db.query(Funcionario).filter(Funcionario.email == email).first()


async def funcionarios_disponiveis_servico(db: Session, agendar_para: datetime, servico_id: int):
    tarefas_subquery = db.query(Tarefa.agenda_id).filter(Tarefa.agenda_id == Agenda.id)
    tarefas_subquery = tarefas_subquery.filter(func.datetime(agendar_para).between(func.datetime(Tarefa.agendadoPara), func.datetime(Tarefa.terminoPrevistoPara)))
    tarefas_subquery = tarefas_subquery.subquery()
    funcionarios = db.query(Funcionario).join(Agenda).join(Servico, Funcionario.servicos).filter(Servico.id == servico_id)
    funcionarios = funcionarios.join(Tarefa, Agenda.tarefas).filter(not_(Tarefa.agenda_id.in_(tarefas_subquery)))
    #_sql = f'''{funcionarios.statement.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True})}'''.replace('\n', '')
    
    return funcionarios.all()

async def novo_funcionario(db: Session, funcionario: FuncionarioCreate, empresa_id):
    db_obj = Funcionario(**funcionario.dict(), empresa_id=empresa_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj