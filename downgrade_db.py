from dbsession import DBSession
from migrations import PopulateMockedFullDbMigration

def downgrade_db():
    # Criando a sessão do banco
    dbsession = DBSession()  
    
    # Criando a instância da migração
    migration = PopulateMockedFullDbMigration(dbsession=dbsession)
    
    # Executando a migração de downgrade
    print("Iniciando o downgrade do banco...")
    migration.downgrade_populated_db()
    print("Downgrade concluído com sucesso!")

if __name__ == "__main__":
    downgrade_db()
