import random
import sys
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from dbsession import DBSession

fake = Faker('pt_BR')

# Lista de nomes mais descritivos e organizados
NOMES_ATIVIDADES = [
    'Treinamento Funcional', 'Iniciação à Corrida', 'Condicionamento Físico',
    'Ginástica Localizada', 'Fortalecimento Muscular', 'Natação Adulto Iniciante',
    'Natação Adulto Avançado', 'Hidroginástica', 'Yoga e Alongamento', 'Ritmos Dançantes',
    'Vôlei Recreativo', 'Futebol Society Amistoso',
    'Karatê (Extensão)', 'Kung Fu (Extensão)', 'Tai Chi Chuan (Extensão)', 'Capoeira (Extensão)'
]

def gerar_atividades(dbsession, quantidade):
    """
    Gera dados fictícios e consistentes para a tabela ATIVIDADE.
    - As datas são geradas de forma coerente.
    - Nomes são únicos e controlados pela lista NOMES_ATIVIDADES.
    - Insere diretamente no banco.
    """

    print(f"Gerando {quantidade} registros de atividades...")

    atividades_data = []
    atividades_set = set()

    # Limita a quantidade ao número de nomes únicos disponíveis
    if quantidade > len(NOMES_ATIVIDADES):
        print(f"Aviso: Reduzindo número de atividades para {len(NOMES_ATIVIDADES)} (máximo de nomes únicos).")
        quantidade = len(NOMES_ATIVIDADES)

    nomes_selecionados = random.sample(NOMES_ATIVIDADES, quantidade)

    for id_atividade, nome in enumerate(nomes_selecionados, start=1):
        # Gera data de início aleatória em 2023
        data_inicio = fake.date_between(start_date='-1y', end_date='today')

        # Garante que o mesmo nome não terá a mesma data
        key = (nome, data_inicio)
        if key in atividades_set:
            continue
        atividades_set.add(key)

        # Gera data de fim coerente (30 a 180 dias depois)
        data_fim = data_inicio + timedelta(days=random.randint(30, 180))

        vagas_limite = random.randint(5, 30)

        atividades_data.append((nome, vagas_limite, data_inicio, data_fim))

    # Inserir diretamente no banco
    query = """
        INSERT INTO ATIVIDADE (NOME, VAGAS_LIMITE, DATA_INICIO_PERIODO, DATA_FIM_PERIODO)
        VALUES (%s, %s, %s, %s)
    """

    print(f"Inserindo {len(atividades_data)} atividades no banco...")
    dbsession.executemany(query, atividades_data)
    print(f"✅ {len(atividades_data)} atividades inseridas com sucesso!")
    print(f"Total de atividades geradas: {len(atividades_data)}")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_atividades(dbsession, 16)
    finally:
        dbsession.close()
