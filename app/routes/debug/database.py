import subprocess
import sys
from pathlib import Path

from flask import jsonify

from app.routes.debug import debug_blueprint
from dbsession import DBSession
from migrations import PopulateMockedFullDbMigration, SchemaMigration
from populate_db import populate_db


@debug_blueprint.post("/populate-db")
def populate_database():
    """Popula o banco de dados com dados sintéticos."""
    try:
        # Obter o diretório raiz do projeto (assumindo que estamos em app/routes/debug/)
        project_root = Path(__file__).parent.parent.parent.parent
        dados_ficticios_path = project_root / "dados_ficticios"
        gerar_dados_script = dados_ficticios_path / "gerar_dados.py"

        if not gerar_dados_script.exists():
            return jsonify({
                "success": False,
                "message": f"Script de geração de dados não encontrado em: {gerar_dados_script}"
            }), 500

        # Executar script de geração de dados
        result = subprocess.run(
            [sys.executable, str(gerar_dados_script)],
            cwd=str(dados_ficticios_path),
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos de timeout
        )

        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Erro desconhecido"
            return jsonify({
                "success": False,
                "message": f"Erro ao gerar dados: {error_msg}"
            }), 500

        # Popular banco de dados (a função populate_db já remove os CSVs automaticamente)
        populate_db()

        return jsonify({
            "success": True,
            "message": "Banco de dados populado com sucesso! Arquivos CSV foram removidos automaticamente."
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "message": "Timeout ao gerar dados sintéticos. O processo demorou mais de 5 minutos."
        }), 500
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
        migration = PopulateMockedFullDbMigration(dbsession=dbsession)

        # Limpar todos os dados e schema
        migration.downgrade_populated_db()

        # Recriar o schema vazio (sem dados, mas com estrutura)
        schema_migration = SchemaMigration(dbsession=dbsession)
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
