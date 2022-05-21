from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.app.grupo import grupo_por_empresa, grupo_por_id, novo_grupo, vincular_ao_grupo
from app.core.schemas.cliente import Cliente
from app.core.schemas.funcionario import Funcionario
from app.core.schemas.grupo import AtribuirGrupo, GrupoBase, GrupoCreate
from app.httpExeptions import exeption_404

from v1.dependences import get_db, usuario_atual


router = APIRouter(
    prefix="/grupo",
    tags=["grupo"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=GrupoBase)
async def grupo(grupo_id:int, db:Session = Depends(get_db), usuario:Funcionario = Depends(usuario_atual)):
    if usuario.administrador:
        return await grupo_por_id(db, grupo_id, usuario.empresa_id)
    raise exeption_404("Usuario não encontrado!")


@router.get('/grupos', response_model=list[GrupoBase])
async def grupos(empresa_id:int, db:Session = Depends(get_db), usuario:Funcionario | Cliente = Depends(usuario_atual)):
    return await grupo_por_empresa(db, empresa_id)


@router.post('/novo-grupo', response_model=GrupoBase)
async def criar_grupo(grupo:GrupoCreate, empresa_id:int, db:Session = Depends(get_db), usuario:Funcionario | Cliente = Depends(usuario_atual)):
    return await novo_grupo(db, grupo, empresa_id)


@router.post('/atribuir-grupo')
async def atribuir_ao_grupo(attr_grupo: AtribuirGrupo, empresa_id, db:Session = Depends(get_db), usuario:Funcionario | Cliente = Depends(usuario_atual)):
    return await vincular_ao_grupo(db, attr_grupo, empresa_id)
