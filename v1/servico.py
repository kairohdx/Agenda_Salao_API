
from random import randint, sample
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.app.empresa import buscar_empresas, todas_empresas
from app.core.app.servico import buscar_servicos, novo_servico, servico_por_empresa, servico_por_id, vincular_ao_servico
from app.core.models.empresa import Empresa
from app.core.schemas.cliente import Cliente
from app.core.schemas.empresa import EmpresaBase
from app.core.schemas.funcionario import Funcionario
from app.core.schemas.servico import AtribuirServico, ServicoBase, ServicoCreate

from v1.dependences import get_db, usuario_atual
from v1.empresa import teste


router = APIRouter(
    prefix="/servico",
    tags=["servico"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=ServicoBase)
async def servico(servico_id:int, db:Session = Depends(get_db), usuario:Funcionario | Cliente = Depends(usuario_atual)):
    return await servico_por_id(db, servico_id)


@router.get('/servicos', response_model=list[ServicoBase])
async def servicos(empresa_id:int, palavras:str = "", pagina:int=1, max:int=10, db:Session = Depends(get_db)):
    return await buscar_servicos(db, empresa_id, palavras, pagina, max)


@router.post('/novo-servico', response_model=ServicoBase)
async def criar_servico(servico:ServicoCreate, empresa_id:int, db:Session = Depends(get_db), usuario:Funcionario | Cliente = Depends(usuario_atual)):
    return await novo_servico(db, servico, empresa_id)


@router.post('/atribuir-servico')
async def atribuir_ao_servico(attr_servico: AtribuirServico, empresa_id, db:Session = Depends(get_db), usuario:Funcionario | Cliente = Depends(usuario_atual)):
    return await vincular_ao_servico(db, attr_servico, empresa_id)


if __debug__:
    @router.post('/atribuir-servicos-aleatorio')
    async def criar_atribuir_servicos_aleatorios(servicos:list[str], db:Session = Depends(get_db)):
        _servicos:list[ServicoCreate] = []
        for servico in servicos:
            s = ServicoCreate(nome=servico, descricao=f"{servico} Descrição Automatica", )
            _servicos.append(s)
        empresas:list[Empresa] = await todas_empresas(db)

        for empresa in empresas:
            idxs = sample(range(0, len(_servicos)), 4)
            _s = [await novo_servico(servico=_servicos[i], db=db, empresa_id=empresa.id) for i in idxs]
            ss = []
            ss.append(AtribuirServico(funcionario_id=empresa.funcionarios[0].id, servico_id=_s[0].id))
            ss.append(AtribuirServico(funcionario_id=empresa.funcionarios[0].id, servico_id=_s[1].id))
            ss.append(AtribuirServico(funcionario_id=empresa.funcionarios[1].id, servico_id=_s[1].id))
            ss.append(AtribuirServico(funcionario_id=empresa.funcionarios[1].id, servico_id=_s[2].id))
            ss.append(AtribuirServico(funcionario_id=empresa.funcionarios[2].id, servico_id=_s[1].id))
            ss.append(AtribuirServico(funcionario_id=empresa.funcionarios[2].id, servico_id=_s[3].id))
            ss.append(AtribuirServico(funcionario_id=empresa.funcionarios[3].id, servico_id=_s[1].id))
            ss.append(AtribuirServico(funcionario_id=empresa.funcionarios[3].id, servico_id=_s[3].id))
            [await atribuir_ao_servico(_ss, empresa.id, db) for _ss in ss]
            
        return True


