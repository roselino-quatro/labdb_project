import csv
import random

# Função para gerar um número de conselho aleatório
def gerar_numero_conselho():
    return f"CREF {random.randint(100000, 999999)}-{random.choice(['G', 'M', 'X', 'P', 'T', 'Q', 'R', 'S', 'U', 'V'])}"

# Função para gerar os dados de educador físico para 10% dos funcionários
def gerar_educadores_fisicos(nome_arquivo_csv_funcionario, nome_arquivo_sql_educador, nome_arquivo_csv_educador):
    with open(nome_arquivo_csv_funcionario, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Pega o cabeçalho
        funcionarios = list(reader)

    # Calcular 10% dos funcionários
    total_funcionarios = len(funcionarios)
    percentual_10 = int(total_funcionarios * 0.1)

    # Selecionar aleatoriamente 10% dos funcionários
    funcionarios_10 = random.sample(funcionarios, percentual_10)

    # Montar os dados para o educador físico
    educadores = []
    for row in funcionarios_10:
        cpf_funcionario = row[0]
        numero_conselho = gerar_numero_conselho()
        educadores.append([cpf_funcionario, numero_conselho])

    # Salvar arquivo CSV com os dados dos educadores físicos
    with open(nome_arquivo_csv_educador, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CPF_FUNCIONARIO', 'NUMERO_CONSELHO'])  # Cabeçalho
        writer.writerows(educadores)

    # Salvar arquivo SQL com comandos INSERT
    with open(nome_arquivo_sql_educador, mode='w', encoding='utf-8') as sql_file:
        for cpf_funcionario, numero_conselho in educadores:
            insert_sql = f"INSERT INTO EDUCADOR_FISICO (CPF_FUNCIONARIO, NUMERO_CONSELHO) VALUES ('{cpf_funcionario}', '{numero_conselho}');\n"
            sql_file.write(insert_sql)

    print(f"Arquivo SQL de educadores físicos gerado: {nome_arquivo_sql_educador}")
    print(f"Arquivo CSV de educadores físicos gerado: {nome_arquivo_csv_educador}")

# Executa o gerador
gerar_educadores_fisicos('funcionarios.csv', 'upgrade_educador_fisico.sql', 'educador_fisico.csv')
