from backend.core.logging import setup_logging
from backend.helpers.logger import get_logger
from backend.config.settings import settings

from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database, drop_database

from backend.db.raw.models.base import RawBase

def reset_database(database_url, label="raw_db"):
    logger = get_logger(f"reset_{label}")
    engine = create_engine(database_url)

    try:
        logger.info(f"Verificando existência do banco {label}...")
        if database_exists(engine.url):
            logger.info(f"🗑️ Banco {label} existente encontrado. Excluindo...")
            drop_database(engine.url)
            logger.info(f"✅ Banco {label} excluído com sucesso.")
        else:
            logger.info(f"📭 Banco {label} não existe. Será criado.")

        logger.info(f"🆕 Criando banco {label}...")
        create_database(engine.url)
        logger.info(f"✅ Banco {label} criado com sucesso.")

        engine = create_engine(database_url)
        with engine.connect() as conn:
            conn.execute(text("SET TIME ZONE 'UTC';"))
            logger.info("⏱️ Timezone UTC configurado.")
            logger.info("🧱 Criando tabelas...")
            RawBase.metadata.create_all(engine)
            logger.info("✅ Tabelas criadas com sucesso.")

    except Exception as e:
        logger.exception(f"❌ Erro ao resetar banco {label}: {str(e)}")

def main():
    setup_logging()
    reset_database(settings.RAW_DATABASE_URL, label="raw_db")
    reset_database(settings.RAW_TEST_DATABASE_URL, label="raw_db_test")

if __name__ == "__main__":
    main()
