# test_schema.py
import pytest
from app.services.migrations import SchemaMigration

TABLES = [
    "PESSOA",
    "INTERNO_USP",
    "FUNCIONARIO",
    "FUNCIONARIO_ATRIBUICAO",
    "FUNCIONARIO_RESTRICAO",
    "EDUCADOR_FISICO",
    "INSTALACAO",
    "EQUIPAMENTO",
    "DOACAO",
    "RESERVA",
    "ATIVIDADE",
    "OCORRENCIA_SEMANAL",
    "CONDUZ_ATIVIDADE",
    "PARTICIPACAO_ATIVIDADE",
    "EVENTO",
    "SUPERVISAO_EVENTO",
    "GRUPO_EXTENSAO",
    "ATIVIDADE_GRUPO_EXTENSAO",
]

def test_schema_migration(dbsession):
    migration = SchemaMigration(dbsession=dbsession)
    migration.upgrade_schema()
    with dbsession.connection.cursor() as cursor:
        for table in TABLES:
            cursor.execute(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'tests' AND lower(table_name) = lower(%s);",
                (table,)
            )
            count = cursor.fetchone()[0]
            assert count == 1, f"Table {table} was not created in schema 'tests'"

    migration.downgrade_schema()

    with dbsession.connection.cursor() as cursor:
        for table in TABLES:
            cursor.execute(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'tests' AND lower(table_name) = lower(%s);",
                (table,)
            )
            count = cursor.fetchone()[0]
            assert count == 0, f"Table {table} still exists in schema 'tests'"
