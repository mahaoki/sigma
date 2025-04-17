from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.config.settings import settings

# Engine para banco RAW (staging)
engine_staging = create_engine(settings.RAW_DATABASE_URL, pool_pre_ping=True)
SessionRaw = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_staging
))

# Engine para banco DW de produção
engine_production_dw = create_engine(settings.DW_DATABASE_URL, pool_pre_ping=True)
SessionDw = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_production_dw
))

# Dependências de sessões (para uso com FastAPI, por exemplo)
def get_raw_db():
    db_raw = SessionRaw()
    try:
        yield db_raw
    finally:
        db_raw.close()

def get_dw_db():
    db_dw = SessionDw()
    try:
        yield db_dw
    finally:
        db_dw.close()
