from dotenv import load_dotenv
load_dotenv()

import os
import sys

from backend.config import settings
from backend.db.dw.models.base import DwBase
from backend.helpers.logger import log_info, log_error
from sqlalchemy import create_engine, inspect, text
from sqlalchemy_utils import database_exists, create_database, drop_database

def create_tables():
    database_url = settings.DW_DATABASE_URL
    engine = create_engine(database_url)

    if database_exists(database_url):
        log_info(f"🔍 Banco de dados já existe: {database_url}")

        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        if existing_tables:
            log_info(f"📋 Tabelas existentes: {', '.join(existing_tables)}")
            response = input("🔴 Deseja excluir o banco de dados e criar novamente? (s/N): ").strip().lower()

            if response == 's':
                try:
                    engine.dispose()
                    log_info("🗑️ Excluindo banco de dados...")
                    drop_database(database_url)
                    log_info("✅ Banco de dados excluído com sucesso.")
                    log_info("🆕 Criando novo banco de dados...")
                    create_database(database_url)
                    log_info("✅ Banco de dados criado com sucesso.")
                    engine = create_engine(database_url)
                except Exception as e:
                    log_error(f"❌ Erro ao excluir/recriar banco de dados: {str(e)}")
                    sys.exit(1)
            else:
                log_info("🛑 Operação cancelada.")
                update_response = input("🔄 Deseja atualizar a estrutura das tabelas existentes? (s/N): ").strip().lower()
                if update_response != 's':
                    log_info("🛑 Nenhuma alteração realizada.")
                    return
    else:
        log_info(f"🆕 Criando banco de dados: {database_url}")
        create_database(database_url)

    try:
        # Criar tabelas primeiro
        log_info("🔄 Criando/atualizando tabelas no banco de dados...")
        DwBase.metadata.create_all(engine)
        log_info("✅ Tabelas criadas/atualizadas com sucesso!")

        # Ativar extensão pg_trgm e criar índice separado
        with engine.connect() as connection:
            try:
                connection.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
                log_info("✅ Extensão pg_trgm ativada com sucesso.")
            except Exception as ext_err:
                log_error(f"⚠️ Falha ao ativar extensão pg_trgm: {ext_err}")
                raise

            try:
                connection.execute(text("""
                    CREATE INDEX IF NOT EXISTS ix_f_item_contratacao_descricao_item
                    ON f_item_contratacao
                    USING gin (descricao_item gin_trgm_ops);
                """))
                log_info("✅ Índice GIN criado com sucesso em f_item_contratacao.descricao_item.")
            except Exception as index_err:
                log_error(f"❌ Erro ao criar índice GIN: {index_err}")
                raise

    except Exception as e:
        log_error(f"❌ Erro ao criar tabelas: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    create_tables()
