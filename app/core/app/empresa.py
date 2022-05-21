from typing import Any
from sqlalchemy import or_
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Session

from app.core.models.servico import Servico


from app.core.models.empresa import Empresa
from app.core.schemas.empresa import EmpresaCreate
from app.httpExeptions import exeption_401

async def empresa_por_id(db: Session, empresa_id: int):
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()

async def buscar_empresas(db: Session, palavras_chave:str, pagina, max):
    query = db.query(Empresa).join(Servico)
    filter_list = []
    for palavra in palavras_chave.split(" "):
        filter_list.append(Empresa.nome.like(f"%{palavra}%"))
        #filter_list.append(Servico.nome.like(f"%{palavra}%"))
    
    _sql = f'''{query.statement.compile(dialect=sqlite.dialect())}'''

    empresas = query.filter(or_(*filter_list)).all()
    return empresas[(pagina-1)*max: pagina*max]

async def novo_empresa(db: Session, empresa: EmpresaCreate):
    em = db.query(Empresa).filter_by(docNum = empresa.docNum).first()
    if em:
        raise exeption_401("CNPJ já castrado!")
    db_obj = Empresa(**empresa.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    
async def todas_empresas(db: Session):
    return db.query(Empresa).all()

