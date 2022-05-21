from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database.database import Base, engine

from v1 import dependences, empresa, servico, funcionario, agenda, cliente, grupo, tarefa


Base.metadata.create_all(engine)

async def captura_de_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as ex:
        body = await request.body()
        print({"errors": ex.errors(), "body": body.decode(), "url":request.url})
        return Response("Internal server error", status_code=500)


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    #_app.middleware('http')(captura_de_exceptions)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(empresa.router)
    _app.include_router(dependences.router)
    _app.include_router(servico.router)
    _app.include_router(funcionario.router)
    _app.include_router(agenda.router)
    _app.include_router(cliente.router)
    _app.include_router(grupo.router)
    _app.include_router(tarefa.router)

    return _app


app = get_application()
