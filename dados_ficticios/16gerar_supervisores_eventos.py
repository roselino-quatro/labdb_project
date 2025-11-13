import csv
import random

def gerar_supervisao_evento(
    nome_arquivo_funcionarios,
    nome_arquivo_eventos,
    nome_arquivo_sql,
    nome_arquivo_csv
):
    # Ler os funcionários (CPF_FUNCIONARIO)
    with open(nome_arquivo_funcionarios, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Ignora cabeçalho
        funcionarios = [row[0] for row in reader]  # Pega o CPF (coluna 0)

    # Ler os eventos
    with open(nome_arquivo_eventos, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Ignora cabeçalho
        eventos = list(reader)
    
    total_eventos = len(eventos)
    ids_eventos = list(range(1, total_eventos + 1))

    # Selecionar 80% dos eventos para serem supervisionados
    eventos_supervisionados = random.sample(ids_eventos, int(total_eventos * 0.8))

    supervisoes = []

    for id_evento in eventos_supervisionados:
        # Cada evento tem entre 1 e 3 supervisores
        qtd_supervisores = random.randint(1, 3)
        supervisores = random.sample(funcionarios, min(qtd_supervisores, len(funcionarios)))

        for cpf_funcionario in supervisores:
            supervisoes.append([cpf_funcionario, id_evento])

    # Gerar o arquivo SQL
    with open(nome_arquivo_sql, 'w', encoding='utf-8') as sql_file:
        for cpf_funcionario, id_evento in supervisoes:
            insert_sql = (
                f"INSERT INTO SUPERVISAO_EVENTO (CPF_FUNCIONARIO, ID_EVENTO) "
                f"VALUES ('{cpf_funcionario}', {id_evento});\n"
            )
            sql_file.write(insert_sql)

    # Gerar o arquivo CSV
    with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CPF_FUNCIONARIO', 'ID_EVENTO'])
        writer.writerows(supervisoes)

    print(f"Arquivo SQL gerado: {nome_arquivo_sql}")
    print(f"Arquivo CSV gerado: {nome_arquivo_csv}")
    print(f"Total de eventos: {total_eventos}")
    print(f"Total de eventos supervisionados: {len(eventos_supervisionados)} ({len(eventos_supervisionados)/total_eventos:.0%})")
    print(f"Total de linhas geradas (supervisões): {len(supervisoes)}")

# Executa o gerador
gerar_supervisao_evento(
    nome_arquivo_funcionarios='funcionarios.csv',
    nome_arquivo_eventos='eventos.csv',
    nome_arquivo_sql='upgrade_supervisao_evento.sql',
    nome_arquivo_csv='supervisao_evento.csv'
)
