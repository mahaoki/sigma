from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  # ← ignora variáveis desconhecidas

    # Bancos
    RAW_DATABASE_URL: str
    RAW_TEST_DATABASE_URL: str
    DW_DATABASE_URL: str
    # DATABASE_URL agora opcional
    DATABASE_URL: str | None = None

    # API PNCP
    API_CONSULTA: str = "https://pncp.gov.br/api/consulta"
    API_PNCP: str = "https://pncp.gov.br/api/pncp"
    API_TIMEOUT: int = 10
    API_RETRY_ATTEMPTS: int = 5
    API_RETRY_WAIT_MIN: int = 4
    API_RETRY_WAIT_MAX: int = 60

    # Celery / Redis
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP: bool = True  # ← campo adicionado

    # Outros
    SECRET_KEY: str
    DEBUG: bool = False
    ENV: str = "production"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
