
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.app.empresa import buscar_empresas, empresa_por_id, novo_empresa
from app.core.schemas.empresa import Empresa, EmpresaBase, EmpresaCreate


from v1.dependences import get_db, usuario_atual


router = APIRouter(
    prefix="/empresa",
    tags=["empresa"],
    responses={404: {"description": "Not found"}},
)


@router.get("/buscar", response_model=list[EmpresaBase])
async def teste(palavras:str = "", pagina:int=1, max:int=10, db:Session = Depends(get_db)):
    empresas = await buscar_empresas(db, palavras, pagina, max)
    print(len(empresas))
    return empresas


@router.get('/{empresa_id}', response_model=EmpresaBase)
async def empresa(empresa_id:int, db:Session = Depends(get_db)):
    return await empresa_por_id(db, empresa_id)


@router.post('/nova-empresa', response_model=EmpresaBase)
async def criar_empresa(empresa: EmpresaCreate, db:Session = Depends(get_db)):
    return await novo_empresa(db, empresa)


if __debug__:
    @router.post('/novas-empresas', response_model=list[EmpresaBase])
    async def add_empresas(empresas:list[EmpresaCreate], db:Session = Depends(get_db)):
        return [await criar_empresa(empresa, db) for empresa in empresas]
