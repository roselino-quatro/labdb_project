from dataclasses import dataclass
from abc import ABC
from dbsession import DBSession
from pathlib import Path

@dataclass
class BaseMigration:
    dbsession: DBSession
    folder: str = ''

    def upgrade(self, name: str):
        folder_path = Path('./sql/') / self.folder
        self.dbsession.run_sql_file(folder_path / f'upgrade_{name}.sql')

    def downgrade(self, name: str):
        folder_path = Path('./sql/') / self.folder
        self.dbsession.run_sql_file(folder_path / f'downgrade_{name}.sql')


@dataclass
class SchemaMigration(BaseMigration):
    def upgrade_schema(self):
        self.upgrade('schema')

    def downgrade_schema(self):
        self.downgrade('schema')


@dataclass
class BasePopulateMigration(BaseMigration, ABC):
    tables = [
        'pessoa', 'interno_usp', 'funcionario', 'funcionario_atribuicao',
        'funcionario_restricao', 'educador_fisico', 'instalacao', 'equipamento',
        'doacao', 'atividade', 'ocorrencia_semanal', 'reserva', 'conduz_atividade',
        'participacao_atividade', 'evento', 'supervisao_evento', 'grupo_extensao',
        'atividade_grupo_extensao', 'usuario_senha'
    ]

    @property
    def schema_migration(self):
        return SchemaMigration(self.dbsession)

    def upgrade_populated_db(self):
        self.schema_migration.upgrade_schema()
        for table in self.tables:
            self.upgrade(table)

    def downgrade_populated_db(self):
        for table in reversed(self.tables):
            self.downgrade(table)
        self.schema_migration.downgrade_schema()

    # Sobrescrevendo downgrade para usar pasta central
    def downgrade(self, name: str):
        folder_path = Path('./sql/downgrades')  # pasta central de downgrades
        self.dbsession.run_sql_file(folder_path / f'downgrade_{name}.sql')


@dataclass
class PopulateMockedMinimalDbMigration(BasePopulateMigration):
    folder: str = 'populate_mocked_minimal_db'

@dataclass
class PopulateMockedFullDbMigration(BasePopulateMigration):
    folder: str = 'populate_mocked_full_db'
