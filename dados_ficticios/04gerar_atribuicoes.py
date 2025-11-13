import csv
import random

# Função para gerar uma atribuição aleatória para o contexto de Educação Física, Esportes e Recreação
def gerar_atribuicao():
    atribuicoes = [
        'Professor de Educação Física',
        'Coordenador de Atividades Esportivas',
        'Treinador de Atletismo',
        'Professor de Natação',
        'Preparador Físico',
        'Instrutor de Musculação',
        'Técnico de Futebol',
        'Técnico de Vôlei',
        'Assistente de Reabilitação Física',
        'Supervisor de Recreação',
        'Nutricionista Esportivo',
        'Psicólogo Esportivo',
        'Fisioterapeuta',
        'Analista de Performance',
        'Gerente de Eventos Esportivos',
        'Administrador de Ginásio',
        'Monitores de Atividades Recreativas',
        'Gestor de Programas Esportivos',
        'Professor de Yoga ou Pilates',
        'Especialista em Medicina Esportiva'
    ]
    return random.choice(atribuicoes)

def gerar_atribuicoes_funcionario(nome_arquivo_csv_funcionario, nome_arquivo_sql_atribuicao, nome_arquivo_csv_atribuicao):
    with open(nome_arquivo_csv_funcionario, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Pega o cabeçalho
        funcionarios = list(reader)

    # Montar os dados para atribuição
    atribuicoes = []
    for row in funcionarios:
        cpf_funcionario = row[0]
        atribuicao = gerar_atribuicao()
        atribuicoes.append([cpf_funcionario, atribuicao])

    # Salvar arquivo CSV com as atribuições
    with open(nome_arquivo_csv_atribuicao, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CPF_FUNCIONARIO', 'ATRIBUICAO'])  # cabeçalho
        writer.writerows(atribuicoes)

    # Salvar arquivo SQL com comandos INSERT
    with open(nome_arquivo_sql_atribuicao, mode='w', encoding='utf-8') as sql_file:
        for cpf_funcionario, atribuicao in atribuicoes:
            insert_sql = f"INSERT INTO FUNCIONARIO_ATRIBUICAO (CPF_FUNCIONARIO, ATRIBUICAO) VALUES ('{cpf_funcionario}', '{atribuicao}');\n"
            sql_file.write(insert_sql)

    print(f"Arquivo SQL de atribuições gerado: {nome_arquivo_sql_atribuicao}")
    print(f"Arquivo CSV de atribuições gerado: {nome_arquivo_csv_atribuicao}")

# Executa o gerador
gerar_atribuicoes_funcionario('funcionarios.csv', 'upgrade_funcionario_atribuicao.sql', 'funcionario_atribuicao.csv')
