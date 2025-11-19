import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from dbsession import DBSession

# Função para gerar uma data de doação aleatória
def gerar_data_doacao():
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).date()

def gerar_doacoes(dbsession):
    # Buscar pessoas que não são internas (pessoas restantes)
    pessoas_result = dbsession.fetch_all("""
        SELECT CPF FROM PESSOA
        WHERE CPF NOT IN (SELECT CPF_PESSOA FROM INTERNO_USP)
        ORDER BY CPF
    """)
    cpfs_pessoas = [row['cpf'] for row in pessoas_result]

    # Buscar equipamentos existentes
    equipamentos_result = dbsession.fetch_all("SELECT ID_PATRIMONIO FROM EQUIPAMENTO ORDER BY ID_PATRIMONIO")
    ids_equipamentos = [row['id_patrimonio'] for row in equipamentos_result]

    if not ids_equipamentos:
        raise ValueError("Não há equipamentos disponíveis para doação!")

    # Criar conjunto de equipamentos disponíveis (evita duplicatas)
    equipamentos_disponiveis = set(ids_equipamentos)

    # Selecionar 15% das pessoas aleatoriamente
    total_pessoas = len(cpfs_pessoas)
    percentual_15 = max(1, int(total_pessoas * 0.15))
    cpfs_selecionados = random.sample(cpfs_pessoas, percentual_15)

    # Garantir que não geraremos mais doações do que equipamentos disponíveis
    num_doacoes = min(len(cpfs_selecionados), len(equipamentos_disponiveis))
    cpfs_selecionados = cpfs_selecionados[:num_doacoes]

    doacoes_data = []

    for cpf_doador in cpfs_selecionados:
        # Escolher equipamento aleatório sem repetição
        id_equipamento = random.choice(list(equipamentos_disponiveis))
        equipamentos_disponiveis.remove(id_equipamento)

        data_doacao = gerar_data_doacao()
        doacoes_data.append((id_equipamento, cpf_doador, data_doacao))

    # Inserir diretamente no banco
    query = """
        INSERT INTO DOACAO (ID_EQUIPAMENTO, CPF_DOADOR, DATA_DOACAO)
        VALUES (%s, %s, %s)
    """

    print(f"Inserindo {len(doacoes_data)} doações no banco...")
    dbsession.executemany(query, doacoes_data)
    print(f"✅ {len(doacoes_data)} doações inseridas com sucesso!")
    print(f"Total de doações geradas: {len(doacoes_data)} (sobre {total_pessoas} pessoas)")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_doacoes(dbsession)
    finally:
        dbsession.close()
