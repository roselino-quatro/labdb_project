import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('pt_BR')

# Lista de nomes mais descritivos e organizados
NOMES_ATIVIDADES = [
    'Treinamento Funcional', 'Iniciação à Corrida', 'Condicionamento Físico',
    'Ginástica Localizada', 'Fortalecimento Muscular', 'Natação Adulto Iniciante',
    'Natação Adulto Avançado', 'Hidroginástica', 'Yoga e Alongamento', 'Ritmos Dançantes',
    'Vôlei Recreativo', 'Futebol Society Amistoso', 
    'Karatê (Extensão)', 'Kung Fu (Extensão)', 'Tai Chi Chuan (Extensão)', 'Capoeira (Extensão)'
]

def gerar_atividades(nome_arquivo_sql, nome_arquivo_csv, quantidade):
    """
    Gera dados fictícios e consistentes para a tabela ATIVIDADE.
    - As datas são geradas de forma coerente.
    - Nomes são únicos e controlados pela lista NOMES_ATIVIDADES.
    - Gera também o SQL de inserção e o CSV.
    """

    print(f"Gerando {quantidade} registros de atividades...")

    atividades = []
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

        atividades.append([
            id_atividade,
            nome,
            vagas_limite,
            data_inicio.isoformat(),
            data_fim.isoformat()
        ])

    #Gerar arquivo SQL
    with open(nome_arquivo_sql, 'w', encoding='utf-8') as sql_file:
        for atividade in atividades:
            nome_sql = atividade[1].replace("'", "''")
            insert_sql = (
                "INSERT INTO ATIVIDADE (NOME, VAGAS_LIMITE, DATA_INICIO_PERIODO, DATA_FIM_PERIODO) "
                f"VALUES ('{nome_sql}', {atividade[2]}, '{atividade[3]}', '{atividade[4]}');\n"
            )
            sql_file.write(insert_sql)

    #Gerar arquivo CSV
    with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID_ATIVIDADE', 'NOME', 'VAGAS_LIMITE', 'DATA_INICIO_PERIODO', 'DATA_FIM_PERIODO'])
        writer.writerows(atividades)

    print(f"Arquivo SQL gerado: {nome_arquivo_sql}")
    print(f"Arquivo CSV gerado: {nome_arquivo_csv}")
    print(f"Total de atividades geradas: {len(atividades)}")


# Executa o gerador
gerar_atividades(
    nome_arquivo_sql='upgrade_atividade.sql',
    nome_arquivo_csv='atividades.csv',
    quantidade = 16
)
