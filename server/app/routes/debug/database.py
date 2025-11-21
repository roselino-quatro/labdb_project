from pathlib import Path

from flask import jsonify

from app.routes.debug import debug_blueprint
from app.database import DBSession
from app.services.migrations import SchemaMigration
from data_generators.populate import populate_db
from app.services.database.downgrade import downgrade_database
from data_generators.check_populated import is_db_populated


@debug_blueprint.get("/check-db-status")
def check_database_status():
    """Verifica se o banco de dados está populado ou vazio."""
    try:
        populated = is_db_populated()
        return jsonify({
            "populated": populated
        })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Erro ao verificar estado do banco: {error_details}")
        return jsonify({
            "populated": False,
            "error": str(e)
        }), 500


@debug_blueprint.post("/populate-db")
def populate_database():
    """Popula o banco de dados com dados sintéticos usando o sistema unificado."""
    dbsession = None
    try:
        # Criar sessão própria (não usar g.db_session para evitar conflitos)
        dbsession = DBSession()

        # Garantir que schema e funções existem antes de popular
        schema_migration = SchemaMigration(dbsession)

        # Verificar se schema existe
        with dbsession.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'pessoa'
            """)
            result = cursor.fetchone()
            if not result or result[0] == 0:
                # Criar schema se não existir
                schema_migration.upgrade_schema()

        # Aplicar funções e triggers (inclui hash_password)
        from app.services.database.bootstrap import apply_plpgsql_assets
        apply_plpgsql_assets(dbsession)

        # Usa o método unificado que popula dados
        from data_generators.data_generator import populate_database as gen_populate
        gen_populate(dbsession)

        return jsonify({
            "success": True,
            "message": "Banco de dados populado com sucesso!"
        })

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Erro ao popular banco: {error_details}")
        return jsonify({
            "success": False,
            "message": f"Erro ao popular banco: {str(e)}"
        }), 500
    finally:
        if dbsession:
            dbsession.close()


@debug_blueprint.post("/clear-db")
def clear_database():
    """Apaga todos os dados do banco de dados e recria o schema vazio."""
    dbsession = None
    try:
        # Resetar flag do bootstrap para forçar recriação
        import app.services.database.bootstrap as bootstrap_module
        bootstrap_module._schema_ready = False

        # Criar sessão própria (não usar g.db_session para evitar conflitos)
        dbsession = DBSession()
        schema_migration = SchemaMigration(dbsession)

        # Limpar todos os dados primeiro
        try:
            downgrade_database(dbsession)
            dbsession.connection.commit()
        except Exception as e:
            dbsession.connection.rollback()
            print(f"Aviso ao limpar dados: {e}")

        # Limpar schema
        try:
            schema_migration.downgrade_schema()
        except Exception as e:
            print(f"Aviso ao fazer downgrade do schema: {e}")

        # Recriar o schema vazio (sem dados, mas com estrutura)
        schema_migration.upgrade_schema()

        # Verificar se o schema foi criado corretamente
        with dbsession.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'pessoa'
            """)
            result = cursor.fetchone()
            if not result or result[0] == 0:
                raise Exception("Schema não foi criado corretamente")

        # Aplicar funções e triggers (que dependem do schema)
        from app.services.database.bootstrap import apply_plpgsql_assets
        apply_plpgsql_assets(dbsession)

        return jsonify({
            "success": True,
            "message": "Banco de dados limpo e schema recriado com sucesso! Use o botão 'Popular DB' para adicionar dados."
        })

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Erro ao limpar banco: {error_details}")
        return jsonify({
            "success": False,
            "message": f"Erro ao limpar banco: {str(e)}"
        }), 500
    finally:
        if dbsession:
            dbsession.close()
