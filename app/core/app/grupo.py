from sqlalchemy.orm import Session

from app.core.app.funcionario import funcionario_por_id
from app.httpExeptions import exeption_404

from ..models.grupo import Grupo
from ..schemas.grupo import AtribuirGrupo, GrupoCreate

async def grupo_por_id(db: Session, grupo_id: int, empresa_id):
    return db.query(Grupo).filter(Grupo.id == grupo_id and Grupo.empresa_id == empresa_id).first()

async def grupo_por_empresa(db: Session, empresa_id):
    return db.query(Grupo).filter(Grupo.empresa_id == empresa_id).all()

async def novo_grupo(db: Session, grupo: GrupoCreate, empresa_id: int):
    db_obj = Grupo(**grupo.dict(), empresa_id=empresa_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

async def vincular_ao_grupo(db: Session, attr_grupo: AtribuirGrupo, empresa_id: int):
    grupo = await grupo_por_id(db, attr_grupo.grupo_id)
    vinc = await funcionario_por_id(db, attr_grupo.funcionario_id)
    if grupo:
        grupo.funcionarios.append(vinc)
        db.commit()
        return True
    raise exeption_404("Grupo não encontrado!")
