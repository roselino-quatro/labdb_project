import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

# Gerar CONDUZ_ATIVIDADE a partir do banco
def gerar_conduz_atividade(dbsession):
    # Buscar educadores físicos do banco
    educadores_result = dbsession.fetch_all("SELECT CPF_FUNCIONARIO FROM EDUCADOR_FISICO ORDER BY CPF_FUNCIONARIO")
    educadores = [row['cpf_funcionario'] for row in educadores_result]

    # Buscar atividades com IDs do banco
    atividades_result = dbsession.fetch_all("SELECT ID_ATIVIDADE FROM ATIVIDADE ORDER BY ID_ATIVIDADE")
    atividades = [row['id_atividade'] for row in atividades_result]

    conduzir_data = []

    for educador in educadores:
        num_atividades = random.randint(1, min(5, len(atividades)))
        atividades_selecionadas = random.sample(atividades, num_atividades)
        for atividade_id in atividades_selecionadas:
            conduzir_data.append((educador, atividade_id))

    # Inserir diretamente no banco
    query = """
        INSERT INTO CONDUZ_ATIVIDADE (CPF_EDUCADOR_FISICO, ID_ATIVIDADE)
        VALUES (%s, %s)
    """

    print(f"Inserindo {len(conduzir_data)} registros de CONDUZ_ATIVIDADE no banco...")
    dbsession.executemany(query, conduzir_data)
    print(f"✅ {len(conduzir_data)} registros inseridos com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_conduz_atividade(dbsession)
    finally:
        dbsession.close()
