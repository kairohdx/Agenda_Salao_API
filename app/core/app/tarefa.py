from datetime import datetime, timedelta, date
from time import time
from xmlrpc.client import DateTime
from certifi import where
from pytz import UTC, timezone
from sqlalchemy import Time, between, cast, distinct, extract, func
from sqlalchemy.orm import Session
from sqlalchemy.dialects import sqlite
from app.core.app.agenda import agenda_por_funcionario
from app.core.app.cliente import novo_cliente

from app.core.app.servico import servico_por_id
from app.core.models.agenda import Agenda
from app.core.models.cliente import Cliente
from app.core.models.empresa import Empresa
from app.core.models.funcionario import Funcionario
from app.core.models.servico import Servico
from app.core.schemas.cliente import ClienteCreate
from app.httpExeptions import exeption_401, exeption_403

from ..models.tarefa import Tarefa
from ..schemas.tarefa import TarefaCreate

async def tarefa_por_id(db: Session, tarefa_id: int):
    return db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

async def tarefas_futuras_por_servico(db:Session, servico_id:int, intervalo:timedelta):
    return db.query(Tarefa).filter(Tarefa.terminoPrevistoPara + intervalo  > datetime.now(), Tarefa.servico_id == servico_id).all()

async def horarios_alocados_do_servico(db: Session, servico_id:int, model:str = 'semana', hoje:date | None =None):
    hoje = hoje if hoje else date.today()

    query_tarefas = db.query(Tarefa).join(Agenda).join(Funcionario).join(Servico, Funcionario.servicos).join(Empresa, Servico.empresa_id == Empresa.id)
    query_tarefas = query_tarefas.filter(func.time(Tarefa.agendadoPara).between(func.time(Empresa.empresaHorarioAbertura), func.time(Empresa.empresaHorarioFechamento)))
    query_tarefas = query_tarefas.filter(Tarefa.terminoPrevistoPara > datetime.now())
    query_tarefas = query_tarefas.filter(Servico.id == servico_id)

    if model.lower() == "semana":
        query_tarefas = query_tarefas.filter(Tarefa.agendadoPara.between(hoje, hoje + timedelta(days=7)))
    elif model.lower() == "mes":
        query_tarefas = query_tarefas.filter(Tarefa.agendadoPara.between(hoje, hoje + timedelta(days=15)))
    elif model.lower() == "dia":
        query_tarefas = query_tarefas.filter(extract('day', Tarefa.agendadoPara) == hoje.day)
    tarefas_agendadas = query_tarefas.all()


    empresa:Empresa = db.query(Empresa).join(Servico).filter(Servico.id == servico_id).first()
    servico:Servico = db.query(Servico).filter_by(id=servico_id).first()

    tarefas:list[Tarefa] = []

    for tarefa in tarefas_agendadas:
        if tarefa.agendadoPara not in [t.agendadoPara for t in tarefas] and \
            sum(tarefa.agendadoPara == t.agendadoPara for t in tarefas_agendadas) == len(servico.funcionarios):
                tarefas.append(tarefa)

    _sql = f'''{query_tarefas.statement.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True})}'''.replace('\n', '')

    return sorted(tarefas, key= lambda x: x.agendadoPara, reverse=False)

async def novo_tarefa(db: Session, tarefa: TarefaCreate, funcionario_id: int, cliente_email: int, servico_id: int): 
    
    cliente:Cliente = db.query(Cliente).filter_by(email=cliente_email).first()
    if not cliente:
        cliente = await novo_cliente(cliente=ClienteCreate(email=cliente_email), db=db)
    tarefas_cliente = db.query(Tarefa).join(Cliente).filter(func.date(Tarefa.agendadoPara) == tarefa.agendadoPara.date()).filter(Cliente.id == cliente.id).all()
    servico: Servico = await servico_por_id(db, servico_id)
    agenda:Agenda = await agenda_por_funcionario(db, funcionario_id)
    tarefa.terminoPrevistoPara = tarefa.agendadoPara + timedelta(seconds=servico.tempoAtendimento)

    utc= UTC

    if tarefas_cliente:
        datas_colidem = any(
            utc.localize(tarefa_cliente.agendadoPara) <= utc.localize(tarefa.terminoPrevistoPara) 
            and utc.localize(tarefa_cliente.terminoPrevistoPara) >= utc.localize(tarefa.agendadoPara)
            for tarefa_cliente in tarefas_cliente
        )
        if datas_colidem:
            raise exeption_403("Colisão de horarios com cliente")

    if agenda:
        datas_colidem = any(
            utc.localize(tarefa_funcionario.agendadoPara) <= utc.localize(tarefa.terminoPrevistoPara) 
            and utc.localize(tarefa_funcionario.terminoPrevistoPara) >= utc.localize(tarefa.agendadoPara)
            for tarefa_funcionario in agenda.tarefas
        )
        if datas_colidem:
            raise exeption_403("Colisão de horarios com proficional")
    

    db_obj = Tarefa(**tarefa.dict(), agenda_id=agenda.id, cliente_id=cliente.id, servico_id=servico_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
