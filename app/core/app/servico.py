from datetime import datetime
from random import randint
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.dialects import sqlite
from app.core.models.empresa import Empresa
from app.core.models.tarefa import Tarefa

from app.core.app.funcionario import funcionario_por_id
from app.core.app.grupo import grupo_por_id

from ..models.servico import Servico
from ..schemas.servico import AtribuirServico, HorarioDisponivel, ServicoCreate

async def buscar_servicos(db: Session, empresa_id: int, palavras_chave:str, pagina:int, max:int):
    query = db.query(Servico).join(Empresa)
    query = query.filter(Empresa.id == empresa_id)
    filter_list = []
    for palavra in palavras_chave.split(" "):
        filter_list.append(Servico.nome.like(f"%{palavra}%"))
        #filter_list.append(Servico.nome.like(f"%{palavra}%"))
    
    _sql = f'''{query.statement.compile(dialect=sqlite.dialect())}'''

    empresas = query.filter(or_(*filter_list)).all()
    return empresas[(pagina-1)*max: pagina*max]

async def servico_por_id(db: Session, servico_id: int):
    return db.query(Servico).filter(Servico.id == servico_id).first()

async def servico_por_empresa(db: Session, empresa_id: int):
    return db.query(Servico).filter(Servico.empresa_id == empresa_id).all()

async def novo_servico(db: Session, servico: ServicoCreate, empresa_id: int):
    db_obj = Servico(**servico.dict(), empresa_id=empresa_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

async def vincular_ao_servico(db: Session, attr_servico:AtribuirServico, empresa_id):
    servico = await servico_por_id(db, attr_servico.servico_id)
    vinc = await funcionario_por_id(db, attr_servico.funcionario_id) if attr_servico.funcionario_id else await grupo_por_id(db, attr_servico.grupo_id)
    servico.funcionarios.append(vinc) if attr_servico.funcionario_id else servico.grupos.append(vinc)
    db.commit()

