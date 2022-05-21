from sqlalchemy.orm import Session

from ..models.passe import Passe
from ..schemas.passe import PasseCreate

def get_passe(db: Session, passe_id: int):
    passe =  db.query(Passe).filter(Passe.id == passe_id).first()
    return passe.funcionario_id if passe.funcionario_id else passe.funcionario_cliente

def create_passe(db: Session, passe: PasseCreate):
    db_obj = Passe(**passe.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj