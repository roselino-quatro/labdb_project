"""
Módulo para fazer downgrade de dados do banco de dados.

Gerencia apenas a remoção de dados, não o schema.
Para downgrade do schema, use app.services.migrations.SchemaMigration.
"""
from pathlib import Path
from app.database import DBSession
from app.services.migrations import SchemaMigration


def _table_exists(dbsession: DBSession, table_name: str) -> bool:
    """Verifica se uma tabela existe no banco de dados."""
    try:
        with dbsession.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND LOWER(table_name) = LOWER(%s)
            """, (table_name,))
            result = cursor.fetchone()
            return result and result[0] > 0
    except Exception:
        return False


def downgrade_database(dbsession: DBSession):
    """Remove todos os dados do banco (mantém o schema)."""
    tables = [
        'solicitacao_cadastro', 'metrica_acesso_diaria', 'auditoria_login',
        'atividade_grupo_extensao', 'grupo_extensao', 'supervisao_evento', 'evento',
        'participacao_atividade', 'conduz_atividade', 'ocorrencia_semanal', 'atividade',
        'reserva_equipamento', 'reserva', 'doacao', 'equipamento', 'instalacao',
        'educador_fisico', 'funcionario_restricao', 'funcionario_atribuicao',
        'funcionario', 'usuario_senha', 'interno_usp', 'pessoa'
    ]

    for table in tables:
        # Verificar se a tabela existe antes de tentar deletar
        if not _table_exists(dbsession, table):
            continue

        downgrade_file = Path('./sql/downgrades') / f'downgrade_{table}.sql'
        if downgrade_file.exists():
            try:
                dbsession.run_sql_file(str(downgrade_file))
            except Exception as e:
                # Log do erro mas continua com as outras tabelas
                print(f"Erro ao fazer downgrade da tabela {table}: {e}")
                continue


def downgrade_database_and_schema(dbsession: DBSession):
    """Remove todos os dados e o schema do banco."""
    downgrade_database(dbsession)
    schema_migration = SchemaMigration(dbsession)
    schema_migration.downgrade_schema()
