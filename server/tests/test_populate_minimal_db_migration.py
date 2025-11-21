import pytest
from collections import OrderedDict
from app.services.migrations import SchemaMigration
from data_generators.data_generator import populate_database
from app.services.database.downgrade import downgrade_database


def count_table_records(cursor, table_name, schema='tests'):
    cursor.execute(f"SELECT COUNT(*) FROM {schema}.{table_name};")
    return cursor.fetchone()[0]

def table_exists(cursor, table_name, schema='tests'):
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = %s AND table_name = lower(%s);
        """,
        (schema, table_name)
    )
    return cursor.fetchone()[0] > 0

def assert_upgrade(cursor, EXPECTED_TABLES_RECORDS):
    for table_name, expected_count in EXPECTED_TABLES_RECORDS.items():
        actual_count = count_table_records(cursor, table_name)
        assert actual_count == expected_count, (
            f"Tabela {table_name}: esperado {expected_count}, "
            f"obtido {actual_count}"
        )

def assert_downgrade(cursor, tables):
    for table_name in tables:
        assert not table_exists(cursor, table_name), (
            f"Tabela {table_name} ainda existe após downgrade"
        )

def test_populate_minimal_db_migration(dbsession):
    EXPECTED_TABLES_RECORDS = OrderedDict([
        ('PESSOA', 20),
        ('INTERNO_USP', 10),
        ('FUNCIONARIO', 3),
        ('FUNCIONARIO_ATRIBUICAO', 6),
        ('FUNCIONARIO_RESTRICAO', 1),
        ('EDUCADOR_FISICO', 2),
        ('INSTALACAO', 8),
        ('EQUIPAMENTO', 10),
        ('DOACAO', 3),
        ('ATIVIDADE', 6),
        ('OCORRENCIA_SEMANAL', 15),
        ('RESERVA', 6),
        ('CONDUZ_ATIVIDADE', 6),
        ('PARTICIPACAO_ATIVIDADE', 10),
        ('EVENTO', 4),
        ('SUPERVISAO_EVENTO', 5),
        ('GRUPO_EXTENSAO', 4),
        ('ATIVIDADE_GRUPO_EXTENSAO', 6)
    ])

    ALL_TABLES = list(EXPECTED_TABLES_RECORDS.keys())

    # Criar schema e popular dados
    schema_migration = SchemaMigration(dbsession=dbsession)
    schema_migration.upgrade_schema()
    populate_database(dbsession)

    with dbsession.connection.cursor() as cursor:
        assert_upgrade(cursor, EXPECTED_TABLES_RECORDS)

    # Fazer downgrade de dados e schema
    downgrade_database(dbsession)
    schema_migration.downgrade_schema()

    with dbsession.connection.cursor() as cursor:
        assert_downgrade(cursor, ALL_TABLES)
