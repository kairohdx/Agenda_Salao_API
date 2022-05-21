from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
SQLALCHEMY_DATABASE_URL = r'sqlite:///D:\GIT\SALAO_SIS\db\my_db.db'

#engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True) # postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, connect_args={"check_same_thread": False}) # sqlite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
