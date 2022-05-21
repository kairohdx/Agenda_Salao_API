from sqlalchemy.orm import Session
from logging.handlers import RotatingFileHandler
from fastapi import APIRouter, Depends
from app.core.app.agenda import agenda_fake_cliente, agenda_por_funcionario, novo_agenda
from app.core.schemas.agenda import AgendaBase, AgendaCreate
from app.core.schemas.funcionario import Funcionario, FuncionarioBase
from app.core.schemas.cliente import Cliente
from app.httpExeptions import exeption_404

from v1.dependences import get_db, usuario_atual


router = APIRouter(
    prefix="/agenda",
    tags=["agenda"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=AgendaBase)
async def minha_agenda(db:Session = Depends(get_db), usuario:Funcionario | Cliente = Depends(usuario_atual)):
    if type(usuario) == Funcionario:
        agenda = await agenda_por_funcionario(db, usuario.id)
        return agenda
    return await agenda_fake_cliente(db, usuario.id)


@router.post('/novo-agenda', response_model=AgendaBase)
async def criar_agenda(agenda: AgendaCreate, funcionario_id, db:Session = Depends(get_db), usuario:Funcionario | Cliente = Depends(usuario_atual)):
    if type(usuario) == Funcionario:
        return await novo_agenda(db, agenda, funcionario_id)
    raise exeption_404("Funcionario não encontrado!")

