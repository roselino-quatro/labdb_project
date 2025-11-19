"""
Módulo para fazer downgrade de dados do banco de dados.

Gerencia apenas a remoção de dados, não o schema.
Para downgrade do schema, use migrations.SchemaMigration.
"""
from pathlib import Path
from dbsession import DBSession
from migrations import SchemaMigration


def downgrade_database(dbsession: DBSession):
    """Remove todos os dados do banco (mantém o schema)."""
    tables = [
        'atividade_grupo_extensao', 'grupo_extensao', 'supervisao_evento', 'evento',
        'participacao_atividade', 'conduz_atividade', 'ocorrencia_semanal', 'atividade',
        'reserva_equipamento', 'reserva', 'doacao', 'equipamento', 'instalacao',
        'educador_fisico', 'funcionario_restricao', 'funcionario_atribuicao',
        'funcionario', 'interno_usp', 'pessoa'
    ]

    for table in tables:
        downgrade_file = Path('./sql/downgrades') / f'downgrade_{table}.sql'
        if downgrade_file.exists():
            dbsession.run_sql_file(str(downgrade_file))


def downgrade_database_and_schema(dbsession: DBSession):
    """Remove todos os dados e o schema do banco."""
    downgrade_database(dbsession)
    schema_migration = SchemaMigration(dbsession)
    schema_migration.downgrade_schema()
