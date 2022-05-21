from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.app.cliente import cliente_por_id, novo_cliente
from app.core.schemas.cliente import ClienteBase, ClienteCreate
from passlib.context import CryptContext

from v1.dependences import get_db, usuario_atual

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/cliente",
    tags=["cliente"],
    responses={404: {"description": "Not found"}},
)

@router.get('/{cliente_id}', response_model=ClienteBase)
async def cliente(cliente_id:int, db:Session = Depends(get_db)):
    return await cliente_por_id(db, cliente_id)


@router.post('/novo-cliente', response_model=ClienteBase)
async def criar_cliente(cliente:ClienteCreate, db:Session = Depends(get_db)):
    cliente.hashSenha = pwd_context.hash(cliente.hashSenha)
    return await novo_cliente(db, cliente)
