from sqlalchemy.orm import Session
from app.core.app.cliente import cliente_por_id
from app.core.models.funcionario import Funcionario

from app.core.schemas.cliente import Cliente

from app.core.models.agenda import Agenda
from app.core.schemas.agenda import AgendaBase, AgendaCreate

async def agenda_por_id(db: Session, agenda_id: int):
    return db.query(Agenda).filter(Agenda.id == agenda_id).first()

async def agenda_por_funcionario(db: Session, funcionario_id: int):
    return db.query(Agenda).filter(Agenda.funcionario_id == funcionario_id).first()
    

async def agenda_fake_cliente(db: Session, cliente_id: int):
    agenda:AgendaBase
    cliente:Cliente = await cliente_por_id(cliente_id)
    if cliente:
        agenda.tarefas = cliente.tarefas
    return agenda

async def novo_agenda(db: Session, agenda: AgendaCreate, funcionario_id):
    db_obj = Agenda(**agenda.dict(), funcionario_id=funcionario_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
