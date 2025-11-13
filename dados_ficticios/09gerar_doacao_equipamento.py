import csv
import random
from datetime import datetime, timedelta

# Função para gerar uma data de doação aleatória
def gerar_data_doacao():
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).date()

def gerar_doacoes(nome_arquivo_pessoas_restantes, nome_arquivo_equipamentos,
                  nome_arquivo_sql_doacao, nome_arquivo_csv_doacao):
    # Ler pessoas restantes
    with open(nome_arquivo_pessoas_restantes, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Pula cabeçalho
        pessoas = list(reader)

    # Ler equipamentos existentes
    with open(nome_arquivo_equipamentos, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        equipamentos = list(reader)

    if not equipamentos:
        raise ValueError("Não há equipamentos disponíveis para doação!")

    # Criar conjunto de equipamentos disponíveis (evita duplicatas)
    equipamentos_disponiveis = set(equipamento[0] for equipamento in equipamentos)

    # Selecionar 15% das pessoas aleatoriamente
    total_pessoas = len(pessoas)
    percentual_15 = max(1, int(total_pessoas * 0.15))
    pessoas_selecionadas = random.sample(pessoas, percentual_15)

    # Garantir que não geraremos mais doações do que equipamentos disponíveis
    num_doacoes = min(len(pessoas_selecionadas), len(equipamentos_disponiveis))
    pessoas_selecionadas = pessoas_selecionadas[:num_doacoes]

    doacoes = []

    for pessoa in pessoas_selecionadas:
        cpf_doador = pessoa[0]
        # Escolher equipamento aleatório sem repetição
        id_equipamento = random.choice(list(equipamentos_disponiveis))
        equipamentos_disponiveis.remove(id_equipamento)

        data_doacao = gerar_data_doacao()
        doacoes.append([id_equipamento, cpf_doador, data_doacao])

    # Gerar arquivo SQL
    with open(nome_arquivo_sql_doacao, 'w', encoding='utf-8') as sql_file:
        for doacao in doacoes:
            insert_sql = (
                f"INSERT INTO DOACAO (ID_EQUIPAMENTO, CPF_DOADOR, DATA_DOACAO) "
                f"VALUES ('{doacao[0]}', '{doacao[1]}', '{doacao[2]}');\n"
            )
            sql_file.write(insert_sql)

    # Gerar arquivo CSV
    with open(nome_arquivo_csv_doacao, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_EQUIPAMENTO', 'CPF_DOADOR', 'DATA_DOACAO'])
        writer.writerows(doacoes)

    print(f"Arquivo SQL de doações gerado: {nome_arquivo_sql_doacao}")
    print(f"Arquivo CSV de doações gerado: {nome_arquivo_csv_doacao}")
    print(f"Total de doações geradas: {len(doacoes)} (sobre {total_pessoas} pessoas)")

# Executa o gerador
gerar_doacoes('pessoas_restantes.csv', 'equipamentos.csv', 'upgrade_doacao.sql', 'doacoes.csv')
