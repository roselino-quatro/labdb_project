"""
Script para verificar se o banco de dados já foi populado.
Retorna 0 se já foi populado, 1 se não foi populado.
"""
import sys
from dbsession import DBSession

def is_db_populated():
    """Verifica se o banco já foi populado checando se a tabela PESSOA existe e tem dados."""
    try:
        dbsession = DBSession()

        # Verifica se a tabela PESSOA existe (PostgreSQL armazena em lowercase no information_schema)
        check_table_query = """
            SELECT COUNT(*) as count
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND LOWER(table_name) = 'pessoa';
        """

        result = dbsession.fetch_one(check_table_query)

        if result and result['count'] > 0:
            # Verifica se a tabela tem dados (PostgreSQL armazena em lowercase)
            count_query = 'SELECT COUNT(*) as count FROM pessoa;'
            count_result = dbsession.fetch_one(count_query)

            if count_result and count_result['count'] > 0:
                print(f"Banco de dados já populado ({count_result['count']} pessoas encontradas).")
                dbsession.close()
                return True

        print("Banco de dados não populado ainda.")
        dbsession.close()
        return False

    except Exception as e:
        # Se houver erro (tabela não existe, conexão falhou, etc), assume que não está populado
        print(f"Erro ao verificar banco: {e}")
        print("Assumindo que banco não está populado.")
        return False

if __name__ == "__main__":
    if is_db_populated():
        sys.exit(0)  # Já populado
    else:
        sys.exit(1)  # Não populado
