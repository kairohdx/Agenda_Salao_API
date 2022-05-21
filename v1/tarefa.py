from datetime import date, datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.core.app.tarefa import horarios_alocados_do_servico, novo_tarefa, tarefa_por_id
from app.core.schemas.cliente import Cliente
from app.core.schemas.funcionario import Funcionario
from app.core.schemas.tarefa import TarefaBase, TarefaCreate
from app.httpExeptions import exeption_403

from v1.dependences import get_db, usuario_atual


router = APIRouter(
    prefix="/tarefa",
    tags=["tarefa"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=TarefaBase)
async def tarefa(tarefa_id:int, db:Session = Depends(get_db), usuario:Funcionario | Cliente = Depends(usuario_atual)):
    if type(usuario) == Funcionario:
        return await tarefa_por_id(db, tarefa_id)
    raise exeption_403("Permição não concedida")


@router.get('/agenda-servico', response_model=list[TarefaBase])
async def agenda_do_servico(servico_id, model:str = 'semana', hoje:datetime | None =None, db:Session = Depends(get_db)):
    return await horarios_alocados_do_servico(db, servico_id, model, hoje)
    


@router.post('/novo-tarefa', response_model=TarefaBase)
async def tarefa(agendar_para:datetime, funcionario_id:int, cliente_email:str, servico_id:int, db:Session = Depends(get_db)):
    return await novo_tarefa(db, TarefaCreate(agendadoPara=agendar_para), funcionario_id, cliente_email, servico_id)
