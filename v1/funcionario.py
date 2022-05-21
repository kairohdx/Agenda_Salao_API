from datetime import datetime
from random import randint, sample
import random
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.app.agenda import novo_agenda
from app.core.app.empresa import buscar_empresas, todas_empresas
from app.core.app.funcionario import funcionario_por_id, funcionarios_disponiveis_servico, novo_funcionario
from app.core.models.empresa import Empresa
from app.core.schemas.agenda import AgendaCreate
from app.core.schemas.funcionario import FuncionarioBase, FuncionarioCreate, FuncionarioParaCliente
from passlib.context import CryptContext

from v1.dependences import get_db, usuario_atual
from v1.empresa import teste

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/funcionario",
    tags=["funcionario"],
    responses={404: {"description": "Not found"}},
)

if __debug__:
    @router.get('/gen_dois_func_empresa')
    async def gerar_dois_funcionarios_para_cada_empresa(db:Session = Depends(get_db)):
        empresas:list[Empresa] = await todas_empresas(db)

        nomes = ["Maria", "Ana", "Gabriela", "Julia", "Leticia", "Marina", "Suelen", "Adriana", "Andressa", "Bruna", "Patricia", "Laura", "Beatriz", "Alice", "Larissa", "Mariana"]
        sobreNome = ["Alves", "dos Santos", "da Silva", "de Carvalho", "Camargo", "Pereira", "Gomes", "Andrade", "Carvalho", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Lima", "Gomes", "Ribeiro", "Martins"]
        func_rand_email = random.sample(range(123, 56421), (78*4))
        for empresa in empresas:
            for i in range(4):
                f = await novo_funcionario(funcionario=FuncionarioCreate(
                    administrador=0,
                    email= f"email_{func_rand_email.pop()}@funcionario.com",
                    nome= f"{nomes[randint(0, len(nomes) - 1)]} {sobreNome[randint(0, len(sobreNome) - 1)]}",
                    hashSenha="As12345"
                ), empresa_id=empresa.id, db=db)
                await novo_agenda(db, AgendaCreate(maximoTarefas=10),f.id)
        return True


@router.get('/funcionarios-disponiveis', response_model=list[FuncionarioParaCliente])
async def funcionarios_disponiveis(agendar_para: datetime, servico_id:int, db:Session = Depends(get_db)):
    print(f'Servico_ID: {servico_id}, agendar_para: {agendar_para}')
    funcionarios = await funcionarios_disponiveis_servico(db, agendar_para, servico_id)
    print(funcionarios)
    return funcionarios

@router.get('/{funcionario_id}')
async def funcionario(funcionairo_id:int, db:Session = Depends(get_db)):
    return await funcionario_por_id(db, funcionairo_id)


@router.post('/novo-funcionairo', response_model=FuncionarioBase)
async def criar_funcionario(funcionario: FuncionarioCreate, empresa_id:int, db:Session = Depends(get_db)):
    funcionario.hashSenha = pwd_context.hash(funcionario.hashSenha)
    funcionario = await novo_funcionario(db, funcionario, empresa_id)
    await novo_agenda(db=db, funcionario_id=funcionario.id, agenda=AgendaCreate(maximoTarefas=12))
    return funcionario

