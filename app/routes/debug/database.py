from pathlib import Path

from flask import jsonify

from app.routes.debug import debug_blueprint
from app.database import DBSession
from app.services.migrations import SchemaMigration
from data_generators.populate import populate_db
from app.services.database.downgrade import downgrade_database


@debug_blueprint.post("/populate-db")
def populate_database():
    """Popula o banco de dados com dados sintéticos usando o sistema unificado."""
    try:
        # Usa o método unificado que cria schema e popula dados
        populate_db()

        return jsonify({
            "success": True,
            "message": "Banco de dados populado com sucesso!"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao popular banco: {str(e)}"
        }), 500


@debug_blueprint.post("/clear-db")
def clear_database():
    """Apaga todos os dados do banco de dados e recria o schema vazio."""
    try:
        # Resetar flag do bootstrap para forçar recriação
        import app.services.bootstrap as bootstrap_module
        bootstrap_module._schema_ready = False

        dbsession = DBSession()
        schema_migration = SchemaMigration(dbsession)

        # Limpar todos os dados e schema
        downgrade_database(dbsession)
        schema_migration.downgrade_schema()

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
        project_root = Path(__file__).parent.parent.parent.parent
        functions_file = project_root / "sql" / "funcionalidades" / "upgrade_functions.sql"
        triggers_file = project_root / "sql" / "funcionalidades" / "upgrade_triggers.sql"

        # Aplicar funções com tratamento de erro melhorado
        if functions_file.exists():
            try:
                with open(functions_file, 'r') as f:
                    query = f.read()
                with dbsession.connection.cursor() as cursor:
                    cursor.execute(query)
                dbsession.connection.commit()
            except Exception as e:
                dbsession.connection.rollback()
                # Não é crítico - o bootstrap tentará novamente na próxima requisição
                print(f"Aviso: Erro ao aplicar funções (será tentado novamente pelo bootstrap): {e}")

        # Aplicar triggers com tratamento de erro melhorado
        if triggers_file.exists():
            try:
                with open(triggers_file, 'r') as f:
                    query = f.read()
                with dbsession.connection.cursor() as cursor:
                    cursor.execute(query)
                dbsession.connection.commit()
            except Exception as e:
                dbsession.connection.rollback()
                # Não é crítico - o bootstrap tentará novamente na próxima requisição
                print(f"Aviso: Erro ao aplicar triggers (será tentado novamente pelo bootstrap): {e}")

        dbsession.close()

        return jsonify({
            "success": True,
            "message": "Banco de dados limpo e schema recriado com sucesso! Use o botão 'Popular DB' para adicionar dados."
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao limpar banco: {str(e)}"
        }), 500
