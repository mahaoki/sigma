from backend.core.logging import setup_logging
from backend.helpers.logger import get_logger
from backend.config.settings import settings

import os
import sys

from sqlalchemy import create_engine, inspect, text
from sqlalchemy_utils import database_exists, create_database, drop_database

from backend.db.raw.models.base import RawBase

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")


# Inicializa logging
setup_logging()
logger = get_logger("create_tables")

def create_tables():
    database_url = settings.RAW_DATABASE_URL
    engine = create_engine(database_url)

    if database_exists(database_url):
        logger.info(f"🔍 Banco de dados já existe: {database_url}")

        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        if existing_tables:
            logger.info(f"📋 Tabelas existentes: {', '.join(existing_tables)}")
            response = input("🔴 Deseja excluir o banco de dados e criar novamente? (s/N): ").strip().lower()

            if response == 's':
                try:
                    engine.dispose()
                    logger.info("🗑️ Excluindo banco de dados...")
                    drop_database(database_url)
                    logger.info("✅ Banco de dados excluído com sucesso.")
                    logger.info("🆕 Criando novo banco de dados...")
                    create_database(database_url)
                    logger.info("✅ Banco de dados criado com sucesso.")
                    engine = create_engine(database_url)
                except Exception as e:
                    logger.error(f"❌ Erro ao excluir/recriar banco de dados: {str(e)}")
                    sys.exit(1)
            else:
                logger.info("🛑 Operação cancelada.")
                update_response = input("🔄 Deseja atualizar a estrutura das tabelas existentes? (s/N): ").strip().lower()
                if update_response != 's':
                    logger.info("🛑 Nenhuma alteração realizada.")
                    return
    else:
        logger.info(f"🆕 Criando banco de dados: {database_url}")
        create_database(database_url)

    try:
        with engine.connect() as conn:
            conn.execute(text("SET TIME ZONE 'UTC';"))
            logger.info("⏱️ Timezone UTC configurado.")

            logger.info("🔄 Criando/atualizando tabelas no banco de dados...")
            RawBase.metadata.create_all(engine)
            logger.info("✅ Tabelas criadas/atualizadas com sucesso!")

    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    create_tables()
