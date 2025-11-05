from dbsession import DBSession
from migrations import PopulateMockedFullDbMigration

def populate_db():
    # Criando a sessão do banco
    dbsession = DBSession()
    
    # Criando a instância da migração
    migration = PopulateMockedFullDbMigration(dbsession=dbsession)
    
    # Executando a migração de populações
    print("Iniciando a migração de populações do banco...")
    migration.upgrade_populated_db()
    print("Migração de populações concluída com sucesso!")

if __name__ == "__main__":
    populate_db()
