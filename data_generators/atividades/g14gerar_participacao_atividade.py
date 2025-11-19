import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from dbsession import DBSession

# Função para gerar uma data de inscrição aleatória
def gerar_data_inscricao():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).date()

# Função principal para gerar os dados de PARTICIPACAO_ATIVIDADE
def gerar_participacao_atividade(dbsession):
    # Buscar CPFs das pessoas restantes (participantes) - pessoas que não são internas
    participantes_result = dbsession.fetch_all("""
        SELECT CPF FROM PESSOA
        WHERE CPF NOT IN (SELECT CPF_PESSOA FROM INTERNO_USP)
        ORDER BY CPF
    """)
    participantes = [row['cpf'] for row in participantes_result]

    # Buscar CPFs dos internos (podem ser convidantes)
    internos_result = dbsession.fetch_all("SELECT CPF_PESSOA FROM INTERNO_USP ORDER BY CPF_PESSOA")
    internos = [row['cpf_pessoa'] for row in internos_result]

    # Buscar IDs das atividades
    atividades_result = dbsession.fetch_all("SELECT ID_ATIVIDADE FROM ATIVIDADE ORDER BY ID_ATIVIDADE")
    atividades = [row['id_atividade'] for row in atividades_result]

    participacoes_data = []

    # Cada participante pode participar de 1 a 3 atividades
    for participante in participantes:
        num_atividades = min(random.randint(1, 3), len(atividades))
        atividades_escolhidas = random.sample(atividades, num_atividades)

        for id_atividade in atividades_escolhidas:
            # 50% de chance de ter um convidante interno
            cpf_convidante = random.choice(internos) if random.random() < 0.5 and internos else None
            data_inscricao = gerar_data_inscricao()

            if cpf_convidante:
                participacoes_data.append((participante, id_atividade, cpf_convidante, data_inscricao))
            else:
                participacoes_data.append((participante, id_atividade, None, data_inscricao))

    # Inserir diretamente no banco (com tratamento para NULL)
    query_com_convidante = """
        INSERT INTO PARTICIPACAO_ATIVIDADE (CPF_PARTICIPANTE, ID_ATIVIDADE, CPF_CONVIDANTE_INTERNO, DATA_INSCRICAO)
        VALUES (%s, %s, %s, %s)
    """

    query_sem_convidante = """
        INSERT INTO PARTICIPACAO_ATIVIDADE (CPF_PARTICIPANTE, ID_ATIVIDADE, DATA_INSCRICAO)
        VALUES (%s, %s, %s)
    """

    print(f"Inserindo {len(participacoes_data)} participações no banco...")

    # Separar por tipo para executar queries apropriadas
    with_convidante = [(p, a, c, d) for p, a, c, d in participacoes_data if c is not None]
    sem_convidante = [(p, a, d) for p, a, c, d in participacoes_data if c is None]

    if with_convidante:
        dbsession.executemany(query_com_convidante, with_convidante)
    if sem_convidante:
        dbsession.executemany(query_sem_convidante, sem_convidante)

    print(f"✅ {len(participacoes_data)} participações inseridas com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_participacao_atividade(dbsession)
    finally:
        dbsession.close()
