import random
import csv

# Gerar CONDUZ_ATIVIDADE a partir de CSV de atividades e educadores físicos
def gerar_conduz_atividade(nome_arquivo_sql, nome_arquivo_csv, nome_arquivo_csv_educador, nome_arquivo_csv_atividades):
    # Ler educadores físicos
    with open(nome_arquivo_csv_educador, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # pular cabeçalho
        educadores = [row[0] for row in reader]  # CPF

    # Ler atividades com IDs
    with open(nome_arquivo_csv_atividades, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # pular cabeçalho
        atividades = [int(row[0]) for row in reader]  # apenas IDs

    conduzir = []

    for educador in educadores:
        num_atividades = random.randint(1, 5)
        atividades_selecionadas = random.sample(atividades, num_atividades)
        for atividade_id in atividades_selecionadas:
            conduzir.append([educador, atividade_id])

    # SQL
    with open(nome_arquivo_sql, 'w', encoding='utf-8') as sql_file:
        for educador, atividade_id in conduzir:
            insert_sql = f"INSERT INTO CONDUZ_ATIVIDADE (CPF_EDUCADOR_FISICO, ID_ATIVIDADE) VALUES ('{educador}', {atividade_id});\n"
            sql_file.write(insert_sql)

    # CSV
    with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CPF_EDUCADOR_FISICO', 'ID_ATIVIDADE'])
        writer.writerows(conduzir)

    print(f"Arquivo SQL de CONDUZ_ATIVIDADE gerado: {nome_arquivo_sql}")
    print(f"Arquivo CSV de CONDUZ_ATIVIDADE gerado: {nome_arquivo_csv}")

# Executa o gerador
gerar_conduz_atividade('upgrade_conduz_atividade.sql', 'conduz_atividade.csv', 'educador_fisico.csv', 'atividades.csv')
