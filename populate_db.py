"""
Ponto de entrada único para popular o banco de dados.

Este script cria o schema e popula o banco com dados sintéticos completos.
"""
from pathlib import Path
from dbsession import DBSession
from app.services.data_generator import populate_database


def populate_db():
    """Cria o schema e popula o banco de dados com dados completos."""
    dbsession = DBSession()

    try:
        # Criar schema primeiro
        print("=" * 60)
        print("Criando schema do banco de dados...")
        print("=" * 60)
        schema_file = Path('./sql/upgrade_schema.sql')
        dbsession.run_sql_file(str(schema_file))
        print("✅ Schema criado com sucesso!\n")

        # Popular banco com dados
        populate_database(dbsession)

    finally:
        dbsession.close()


if __name__ == "__main__":
    populate_db()
