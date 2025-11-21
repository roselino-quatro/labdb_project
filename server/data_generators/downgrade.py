"""
Script para fazer downgrade do banco de dados.

Remove todos os dados e o schema.
"""
from app.database import DBSession
from app.services.database.downgrade import downgrade_database_and_schema


def downgrade_db():
    """Remove todos os dados e o schema do banco."""
    dbsession = DBSession()

    try:
        print("=" * 60)
        print("Iniciando o downgrade do banco...")
        print("=" * 60)
        downgrade_database_and_schema(dbsession)
        print("✅ Downgrade concluído com sucesso!")
    finally:
        dbsession.close()


if __name__ == "__main__":
    downgrade_db()
