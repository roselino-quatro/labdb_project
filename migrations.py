"""
Módulo de migrações - gerencia apenas upgrade e downgrade do schema.
"""
from dataclasses import dataclass
from pathlib import Path
from dbsession import DBSession


@dataclass
class SchemaMigration:
    """Gerencia migrações do schema do banco (estrutura, não dados)."""
    dbsession: DBSession

    def upgrade_schema(self):
        """Aplica o schema do banco de dados."""
        schema_file = Path('./sql/upgrade_schema.sql')
        self.dbsession.run_sql_file(str(schema_file))

    def downgrade_schema(self):
        """Remove o schema do banco de dados."""
        schema_file = Path('./sql/downgrade_schema.sql')
        self.dbsession.run_sql_file(str(schema_file))
