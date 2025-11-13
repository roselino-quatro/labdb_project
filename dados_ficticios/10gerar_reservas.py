import csv
import random
from datetime import datetime, timedelta

# Função para gerar uma data de reserva aleatória
def gerar_data_reserva():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).date()

# Função para gerar horários de reserva coerentes (mínimo 1h, máximo 2h)
# e que comecem em hora cheia ou meia hora
def gerar_horarios_reserva():
    # Limites de operação
    start_hour = 6   # 06:00
    end_hour = 22    # 22:00

    # Gera horário inicial: pode ser em hora cheia ou meia hora
    hora = random.randint(start_hour, end_hour - 1)
    minuto = random.choice([0, 30])  # apenas 00 ou 30 minutos

    horario_inicio = datetime.strptime(f"{hora:02d}:{minuto:02d}", "%H:%M")

    # Duração aleatória entre 60 e 120 minutos (1h a 2h)
    duracao = random.randint(60, 120)
    horario_fim = horario_inicio + timedelta(minutes=duracao)

    # Evita que o horário ultrapasse o limite das 22h
    if horario_fim.hour >= 22 and (horario_fim.minute > 0 or horario_fim.hour > 22):
        horario_fim = datetime.strptime("22:00", "%H:%M")

    return horario_inicio.time(), horario_fim.time()

# Função para gerar as reservas
def gerar_reservas(nome_arquivo_internos, nome_arquivo_instalacoes, nome_arquivo_sql_reservas, nome_arquivo_csv_reservas):
    # Ler o arquivo de pessoas internas
    with open(nome_arquivo_internos, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header_pessoas = next(reader)
        pessoas = list(reader)

    # Ler o arquivo de instalações
    with open(nome_arquivo_instalacoes, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header_instalacoes = next(reader)
        instalacoes = list(reader)

    # Selecionar 50% das pessoas aleatoriamente
    total_pessoas = len(pessoas)
    percentual_50 = int(total_pessoas * 0.5)
    pessoas_50 = random.sample(pessoas, percentual_50)

    reservas = []
    reservas_existentes = set()  # Tuplas (id_instalacao, data_reserva, horario_inicio)

    # Gerar reservas sem duplicar a chave única
    for pessoa in pessoas_50:
        cpf_responsavel = pessoa[0]
        tentativas = 0
        while tentativas < 10:  # Evitar loop infinito
            id_instalacao = random.choice(instalacoes)[0]
            data_reserva = gerar_data_reserva()
            horario_inicio, horario_fim = gerar_horarios_reserva()
            chave = (id_instalacao, data_reserva, horario_inicio)

            if chave not in reservas_existentes:
                reservas_existentes.add(chave)
                reservas.append([id_instalacao, cpf_responsavel, data_reserva, horario_inicio, horario_fim])
                break
            tentativas += 1

    # Gerar arquivo SQL
    with open(nome_arquivo_sql_reservas, 'w', encoding='utf-8') as sql_file:
        for reserva in reservas:
            insert_sql = (
                "INSERT INTO RESERVA (ID_INSTALACAO, CPF_RESPONSAVEL_INTERNO, DATA_RESERVA, HORARIO_INICIO, HORARIO_FIM) "
                f"VALUES ('{reserva[0]}', '{reserva[1]}', '{reserva[2]}', '{reserva[3]}', '{reserva[4]}');\n"
            )
            sql_file.write(insert_sql)

    # Gerar arquivo CSV
    with open(nome_arquivo_csv_reservas, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_INSTALACAO', 'CPF_RESPONSAVEL_INTERNO', 'DATA_RESERVA', 'HORARIO_INICIO', 'HORARIO_FIM'])
        writer.writerows(reservas)

    print(f"Arquivo SQL de reservas gerado: {nome_arquivo_sql_reservas}")
    print(f"Arquivo CSV de reservas gerado: {nome_arquivo_csv_reservas}")

# Executa o gerador
gerar_reservas('pessoas_internas.csv', 'instalacoes.csv', 'upgrade_reserva.sql', 'reservas.csv')
