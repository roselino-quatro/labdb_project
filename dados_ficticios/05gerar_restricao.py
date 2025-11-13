import csv
import random

# Função para gerar uma restrição física aleatória
def gerar_restricao_fisica():
    restricoes = [
        'Lesão no joelho',
        'Problemas de coluna',
        'Deslocamento no ombro',
        'Restrição para atividades de impacto',
        'Hipertensão',
        'Problemas cardíacos',
        'Lesão no tornozelo',
        'Artrite',
        'Asma',
        'Deficiência auditiva'
    ]
    return random.choice(restricoes)

# Função para gerar os dados de restrição física para 10% dos funcionários
def gerar_restricoes_funcionario(nome_arquivo_csv_funcionario, nome_arquivo_sql_restricao, nome_arquivo_csv_restricao):
    with open(nome_arquivo_csv_funcionario, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Pega o cabeçalho
        funcionarios = list(reader)

    # Calcular 10% dos funcionários
    total_funcionarios = len(funcionarios)
    percentual_10 = int(total_funcionarios * 0.1)

    # Selecionar aleatoriamente 10% dos funcionários
    funcionarios_10 = random.sample(funcionarios, percentual_10)

    # Montar os dados para a restrição física
    restricoes = []
    for row in funcionarios_10:
        cpf_funcionario = row[0]
        restricao_fisica = gerar_restricao_fisica()
        restricoes.append([cpf_funcionario, restricao_fisica])

    # Salvar arquivo CSV com as restrições físicas
    with open(nome_arquivo_csv_restricao, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CPF_FUNCIONARIO', 'RESTRICAO_FISICA'])  # cabeçalho
        writer.writerows(restricoes)

    # Salvar arquivo SQL com comandos INSERT
    with open(nome_arquivo_sql_restricao, mode='w', encoding='utf-8') as sql_file:
        for cpf_funcionario, restricao_fisica in restricoes:
            insert_sql = f"INSERT INTO FUNCIONARIO_RESTRICAO (CPF_FUNCIONARIO, RESTRICAO_FISICA) VALUES ('{cpf_funcionario}', '{restricao_fisica}');\n"
            sql_file.write(insert_sql)

    print(f"Arquivo SQL de restrições gerado: {nome_arquivo_sql_restricao}")
    print(f"Arquivo CSV de restrições gerado: {nome_arquivo_csv_restricao}")

# Executa o gerador
gerar_restricoes_funcionario('funcionarios.csv', 'upgrade_funcionario_restricao.sql', 'funcionario_restricao.csv')
