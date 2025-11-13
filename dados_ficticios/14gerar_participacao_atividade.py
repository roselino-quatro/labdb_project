import csv
import random
from datetime import datetime, timedelta

# Função para gerar uma data de inscrição aleatória
def gerar_data_inscricao():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).date()

# Função principal para gerar os dados de PARTICIPACAO_ATIVIDADE
def gerar_participacao_atividade(nome_arquivo_sql, nome_arquivo_csv, 
                                 nome_arquivo_csv_participantes, 
                                 nome_arquivo_csv_internos, 
                                 nome_arquivo_csv_atividades):
    # Carregar CPFs das pessoas restantes (participantes)
    with open(nome_arquivo_csv_participantes, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Ignora cabeçalho
        participantes = [row[0] for row in reader]  # CPF é a primeira coluna

    # Carregar CPFs dos internos (podem ser convidantes)
    with open(nome_arquivo_csv_internos, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        internos = [row[0] for row in reader]

    # Carregar IDs das atividades
    with open(nome_arquivo_csv_atividades, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        atividades = list(range(1, len(list(reader)) + 1))  # IDs de 1 até o total de linhas

    participacoes = []

    # Cada participante pode participar de 1 a 3 atividades
    for participante in participantes:
        num_atividades = random.randint(1, 3)
        atividades_escolhidas = random.sample(atividades, num_atividades)

        for id_atividade in atividades_escolhidas:
            # 50% de chance de ter um convidante interno
            cpf_convidante = random.choice(internos) if random.random() < 0.5 else None
            data_inscricao = gerar_data_inscricao()

            participacoes.append([participante, id_atividade, cpf_convidante, data_inscricao])

    # Gerar arquivo SQL
    with open(nome_arquivo_sql, mode='w', encoding='utf-8') as sql_file:
        for cpf_participante, id_atividade, cpf_convidante, data_inscricao in participacoes:
            if cpf_convidante:
                insert_sql = (
                    f"INSERT INTO PARTICIPACAO_ATIVIDADE (CPF_PARTICIPANTE, ID_ATIVIDADE, CPF_CONVIDANTE_INTERNO, DATA_INSCRICAO) "
                    f"VALUES ('{cpf_participante}', {id_atividade}, '{cpf_convidante}', '{data_inscricao}');\n"
                )
            else:
                insert_sql = (
                    f"INSERT INTO PARTICIPACAO_ATIVIDADE (CPF_PARTICIPANTE, ID_ATIVIDADE, DATA_INSCRICAO) "
                    f"VALUES ('{cpf_participante}', {id_atividade}, '{data_inscricao}');\n"
                )
            sql_file.write(insert_sql)

    # Gerar arquivo CSV
    with open(nome_arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CPF_PARTICIPANTE', 'ID_ATIVIDADE', 'CPF_CONVIDANTE_INTERNO', 'DATA_INSCRICAO'])
        writer.writerows(participacoes)

    print(f"Arquivo SQL gerado: {nome_arquivo_sql}")
    print(f"Arquivo CSV gerado: {nome_arquivo_csv}")

# Executa o gerador
gerar_participacao_atividade(
    nome_arquivo_sql='upgrade_participacao_atividade.sql',
    nome_arquivo_csv='participacao_atividade.csv',
    nome_arquivo_csv_participantes='pessoas_restantes.csv',
    nome_arquivo_csv_internos='pessoas_internas.csv',
    nome_arquivo_csv_atividades='atividades.csv'
)
