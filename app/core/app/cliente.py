from sqlalchemy.orm import Session

from ..models.cliente import Cliente
from ..schemas.cliente import ClienteCreate

async def cliente_por_id(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

async def cliente_por_email(db: Session, email: int):
    return db.query(Cliente).filter(Cliente.email == email).first()

async def novo_cliente(db: Session, cliente: ClienteCreate):
    db_obj = Cliente(**cliente.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj