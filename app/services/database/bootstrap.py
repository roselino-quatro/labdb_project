from __future__ import annotations

from pathlib import Path

from flask import current_app

from app.services.database import executor
from data_generators.populate import populate_db

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SQL_ROOT = PROJECT_ROOT / "sql"
SCHEMA_FILE = SQL_ROOT / "upgrade_schema.sql"
FUNCTIONS_FILE = SQL_ROOT / "funcionalidades" / "upgrade_functions.sql"
TRIGGERS_FILE = SQL_ROOT / "funcionalidades" / "upgrade_triggers.sql"

_schema_ready = False


def ensure_schema_populated(db_session) -> None:
    global _schema_ready

    current_app.logger.info("ensure_schema_populated chamado")

    # Sempre verificar se o schema existe, mesmo se _schema_ready for True
    # Isso garante que se o banco foi limpo, o schema será recriado
    try:
        table_count = _count_tables(db_session)
        current_app.logger.info(f"Contagem de tabelas: {table_count}")

        # Verificar também se a tabela PESSOA existe especificamente
        pessoa_exists = False
        try:
            with db_session.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'pessoa'
                """)
                result = cursor.fetchone()
                pessoa_exists = result and result[0] > 0
        except Exception:
            pessoa_exists = False

        current_app.logger.info(f"Tabela PESSOA existe: {pessoa_exists}")

        if table_count == 0 or not pessoa_exists:
            current_app.logger.info("Nenhuma tabela encontrada ou PESSOA não existe. Criando schema...")
            _schema_ready = False  # Resetar flag antes de tentar criar
            _apply_schema(db_session)
            # Verificar se o schema foi criado corretamente
            table_count_after = _count_tables(db_session)
            if table_count_after == 0:
                current_app.logger.error("Falha ao criar schema. Tabelas não foram criadas.")
                _schema_ready = False
                raise Exception("Falha ao criar schema do banco de dados")
            _apply_plpgsql_assets(db_session)
            _apply_sample_data(db_session)
            _schema_ready = True
            current_app.logger.info("Schema criado e populado com sucesso")
        else:
            # Schema existe, apenas aplicar funções/triggers se necessário
            current_app.logger.info("Schema já existe. Aplicando funções/triggers se necessário...")
            if not _schema_ready:
                _apply_plpgsql_assets(db_session)
                _schema_ready = True
    except Exception as e:
        current_app.logger.error(f"Erro ao garantir schema populado: {e}", exc_info=True)
        _schema_ready = False
        # Re-raise para que o erro seja visível
        raise


def _count_tables(db_session) -> int:
    try:
        # Usar a conexão diretamente para evitar problemas com executor
        with db_session.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
            """)
            result = cursor.fetchone()
            if result:
                return int(result[0])
        return 0
    except Exception as e:
        current_app.logger.debug(f"Erro ao contar tabelas (assumindo 0): {e}")
        # Se a query falhar (por exemplo, se não houver tabelas ou schema), retorna 0
        return 0


def _apply_schema(db_session) -> None:
    current_app.logger.info("Applying schema from %s", SCHEMA_FILE)
    try:
        # Ler o arquivo SQL
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as file:
            query = file.read()

        # Verificar se o tipo DIA_SEMANA já existe antes de criar
        with db_session.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM pg_type
                WHERE typname = 'dia_semana'
            """)
            result = cursor.fetchone()
            dia_semana_exists = result and result[0] > 0

        # Modificar o SQL para usar CREATE TABLE IF NOT EXISTS
        # Substituir CREATE TABLE por CREATE TABLE IF NOT EXISTS
        modified_query = query.replace('CREATE TABLE ', 'CREATE TABLE IF NOT EXISTS ')

        # Para CREATE TYPE, remover a linha se o tipo já existir
        # PostgreSQL não suporta CREATE TYPE IF NOT EXISTS
        if dia_semana_exists:
            # Remover a criação do tipo DIA_SEMANA se já existir
            lines = modified_query.split('\n')
            new_lines = []
            skip_type_creation = False
            for line in lines:
                if 'CREATE TYPE DIA_SEMANA' in line.upper():
                    skip_type_creation = True
                    continue
                if skip_type_creation:
                    # Continuar pulando até encontrar o fechamento do enum
                    if line.strip() == ');':
                        skip_type_creation = False
                    continue
                new_lines.append(line)
            modified_query = '\n'.join(new_lines)

        with db_session.connection.cursor() as cursor:
            cursor.execute(modified_query)
        db_session.connection.commit()

        # Verificar se pelo menos a tabela PESSOA foi criada
        with db_session.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'pessoa'
            """)
            result = cursor.fetchone()
            if not result or result[0] == 0:
                raise Exception("Schema não foi criado corretamente. Tabela PESSOA não existe.")
        current_app.logger.info("Schema aplicado com sucesso")
    except Exception as e:
        db_session.connection.rollback()
        current_app.logger.error(f"Erro ao aplicar schema: {e}", exc_info=True)
        raise


def _apply_sample_data(db_session) -> None:
    """Popula o banco com dados usando o sistema unificado."""
    current_app.logger.info("Populando banco com dados...")
    try:
        populate_db()  # Usa a função importada de data_generators
        current_app.logger.info("Dados populados com sucesso")
    except Exception as e:
        current_app.logger.error(f"Erro ao popular dados: {e}", exc_info=True)
        # Não re-raise para não quebrar o bootstrap se a população falhar


def _apply_plpgsql_assets(db_session) -> None:
    # Verificar se o schema está completo (tipo DIA_SEMANA deve existir)
    try:
        with db_session.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM pg_type
                WHERE typname = 'dia_semana'
            """)
            result = cursor.fetchone()
            if not result or result[0] == 0:
                current_app.logger.warning("Schema não está completo (tipo DIA_SEMANA não existe). Pulando aplicação de funções/triggers.")
                return
    except Exception as e:
        current_app.logger.warning(f"Erro ao verificar schema: {e}. Pulando aplicação de funções/triggers.")
        return

    if FUNCTIONS_FILE.exists():
        current_app.logger.info("Applying functions from %s", FUNCTIONS_FILE)
        try:
            db_session.run_sql_file(str(FUNCTIONS_FILE))
        except Exception as e:
            current_app.logger.error(f"Erro ao aplicar funções: {e}")
    if TRIGGERS_FILE.exists():
        current_app.logger.info("Applying triggers from %s", TRIGGERS_FILE)
        try:
            db_session.run_sql_file(str(TRIGGERS_FILE))
        except Exception as e:
            current_app.logger.error(f"Erro ao aplicar triggers: {e}")
