from dbsession import DBSession
from migrations import PopulateMockedFullDbMigration
from pathlib import Path
from app.services.csv_cleanup import delete_csv_files

def populate_db():
    # Criando a sessão do banco
    dbsession = DBSession()

    # Criando a instância da migração
    migration = PopulateMockedFullDbMigration(dbsession=dbsession)

    # Executando a migração de populações
    print("Iniciando a migração de populações do banco...")
    migration.upgrade_populated_db()
    print("Migração de populações concluída com sucesso!")

    # Remover arquivos CSV após popular o banco
    project_root = Path(__file__).parent
    dados_ficticios_path = project_root / "dados_ficticios"
    if dados_ficticios_path.exists():
        print("=== Removendo arquivos CSV gerados ===")
        delete_csv_files(dados_ficticios_path)

if __name__ == "__main__":
    populate_db()
