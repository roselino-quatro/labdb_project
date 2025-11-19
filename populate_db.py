"""
Ponto de entrada único para popular o banco de dados.

Este script cria o schema e popula o banco com dados sintéticos completos.
"""
from pathlib import Path
from dbsession import DBSession
from data_generators.data_generator import populate_database


def _schema_exists(dbsession):
    """Verifica se o schema já existe checando se a tabela pessoa existe."""
    try:
        with dbsession.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'pessoa'
            """)
            result = cursor.fetchone()
            return result and result[0] > 0
    except Exception:
        return False


def _database_has_data(dbsession):
    """Verifica se o banco já tem dados populados."""
    try:
        result = dbsession.fetch_one('SELECT COUNT(*) as count FROM pessoa;')
        return result and result['count'] > 0
    except Exception:
        return False


def populate_db():
    """Cria o schema e popula o banco de dados com dados completos."""
    dbsession = DBSession()

    try:
        # Verificar se schema já existe
        if not _schema_exists(dbsession):
            print("=" * 60)
            print("Criando schema do banco de dados...")
            print("=" * 60)
            schema_file = Path('./sql/upgrade_schema.sql')
            dbsession.run_sql_file(str(schema_file))
            print("✅ Schema criado com sucesso!\n")
        else:
            print("=" * 60)
            print("Schema já existe. Pulando criação do schema.")
            print("=" * 60)

        # Verificar se dados já existem
        if _database_has_data(dbsession):
            print("\n" + "=" * 60)
            print("Banco de dados já contém dados. Pulando população.")
            print("=" * 60)
            return

        # Popular banco com dados
        print("\n" + "=" * 60)
        print("Iniciando população do banco de dados...")
        print("=" * 60)
        populate_database(dbsession)

    finally:
        dbsession.close()


if __name__ == "__main__":
    populate_db()
