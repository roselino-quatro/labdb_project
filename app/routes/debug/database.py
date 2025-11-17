import subprocess
import sys
from pathlib import Path

from flask import jsonify

from app.routes.debug import debug_blueprint
from dbsession import DBSession
from migrations import PopulateMockedFullDbMigration, SchemaMigration


def cleanup_csv_files(dados_ficticios_path: Path) -> tuple[int, str]:
    """
    Remove apenas arquivos CSV da pasta dados_ficticios.

    Args:
        dados_ficticios_path: Caminho para a pasta dados_ficticios

    Returns:
        Tupla com (quantidade_removida, mensagem)
    """
    try:
        if not dados_ficticios_path.exists():
            return (0, f"Pasta {dados_ficticios_path} não encontrada")

        csv_files = list(dados_ficticios_path.glob("*.csv"))
        count = 0

        for csv_file in csv_files:
            try:
                csv_file.unlink()
                count += 1
            except Exception as e:
                # Log erro individual mas continua tentando os outros
                print(f"Aviso: Erro ao remover {csv_file.name}: {e}")

        return (count, f"{count} arquivo(s) CSV removido(s) com sucesso")

    except Exception as e:
        return (0, f"Erro ao limpar CSVs: {str(e)}")


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

        # Popular banco de dados
        dbsession = DBSession()
        migration = PopulateMockedFullDbMigration(dbsession=dbsession)
        migration.upgrade_populated_db()
        dbsession.close()

        # Limpar arquivos CSV após população bem-sucedida
        # (os CSVs são apenas intermediários e não são mais necessários)
        count, cleanup_msg = cleanup_csv_files(dados_ficticios_path)
        print(f"Limpeza de CSVs: {cleanup_msg}")

        return jsonify({
            "success": True,
            "message": "Banco de dados populado com sucesso!"
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
