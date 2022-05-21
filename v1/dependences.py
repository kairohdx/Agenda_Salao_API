from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from app.core.config import Settings

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.database.database import SessionLocal
from app.core.models.cliente import Cliente
from app.core.models.funcionario import Funcionario
from app.core.schemas.funcionario import Funcionario as SFuncionario
from app.core.schemas.cliente import Cliente as SCliente

from app.core.app.cliente import cliente_por_email, cliente_por_id
from app.core.app.funcionario import funcionario_por_email, funcionario_por_id
from app.core.schemas.passe import Passe
from app.httpExeptions import exeption_401


SECRET_KEY = Settings.get_random_secret_key()
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="entrar")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verificar_senha(senha, senha_hashed):
    return pwd_context.verify(senha, senha_hashed)


async def autenticar_funcionario(email: str, senha: str, db:Session):
    funcionario:Funcionario = await funcionario_por_email(db, email)
    if not funcionario:
        return False
    if not verificar_senha(senha, funcionario.hashSenha):
        return False
    return funcionario


async def autenticar_cliente(email: str, senha: str, db:Session):
    cliente:Cliente = await cliente_por_email(db, email)
    if not cliente:
        return False
    if not verificar_senha(senha, cliente.hashSenha):
        return False
    return cliente


async def novo_passe_acesso(data: dict, expira_delta: timedelta = None):
    _encode = data.copy()
    if expira_delta:
        expira = datetime.utcnow() + expira_delta
    else:
        expira = datetime.utcnow() + timedelta(minutes=15)
    _encode.update({"exp": expira})
    encoded_jwt = jwt.encode(_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def monta_funcionario(usuario:Funcionario):
    return SFuncionario(id=usuario.id, email=usuario.email, administrador=usuario.administrador, empresa_id=usuario.empresa_id)


def monta_cliente(usuairo:Cliente):
    return SCliente (id=usuairo.id, email=usuairo.email, nome=usuairo.nome, loginSocial=usuairo.loginSocial, tarefas=usuairo.tarefas)


async def processa_passe(passe: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    try:
        passe_data = jwt.decode(passe, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_email: str = passe_data.get("sub")

        if usuario_email is None:
            raise exeption_401("Não foi possivel validar suas credenciais")
    except JWTError:
        raise exeption_401("Não foi possivel validar suas credenciais")
    
    tipo: str = passe_data.get("tipo")
    #db:Session = get_db()
    usuario = await funcionario_por_email(db, usuario_email) if tipo.lower() == 'funcionario' else await cliente_por_email(db, usuario_email)
    
    if  usuario is None:
        raise exeption_401("Não foi possivel validar suas credenciais")
    return monta_funcionario(usuario) if tipo.lower() == 'funcionario' else monta_cliente(usuario)


async def usuario_atual(usuario_atual: SFuncionario | SCliente = Depends(processa_passe)):
    return usuario_atual


@router.post('/entrar')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    email = form_data.username
    senha = form_data.password
    tipo = 'funcionario'

    usuario = await autenticar_funcionario(email, senha, db) if tipo == 'funcionario' else await autenticar_cliente(email, senha, db)
    if not usuario:
        raise exeption_401("E-mail ou senha incorreto!")
    passe_expiracao = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    passe_acesso = await novo_passe_acesso(
        data={"sub": usuario.email, "tipo":tipo}, expira_delta=passe_expiracao
    )

    return {"access_token": passe_acesso, "token_type": "bearer"}
