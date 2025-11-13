import csv
import random
from faker import Faker

fake = Faker('pt_BR')

def gerar_eventos(nome_arquivo_reservas, nome_arquivo_sql_eventos, nome_arquivo_csv_eventos):
    # Ler reservas existentes
    with open(nome_arquivo_reservas, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Ignora cabeçalho
        reservas = list(reader)

    total_reservas = len(reservas)
    ids_reservas = list(range(1, total_reservas + 1))

    # Seleciona 50% das reservas para gerar eventos
    reservas_evento = random.sample(ids_reservas, int(total_reservas * 0.5))
    total_eventos = len(reservas_evento)

    # Gerar os eventos com nomes únicos usando índice
    eventos = []
    for i, id_reserva in enumerate(reservas_evento, start=1):
        nome_evento = f"{fake.catch_phrase()} #{i}"  # Sufixo garante unicidade
        descricao = fake.paragraph(nb_sentences=random.randint(2, 5))
        eventos.append([nome_evento, descricao, id_reserva])

    # Gerar arquivo SQL
    with open(nome_arquivo_sql_eventos, 'w', encoding='utf-8') as sql_file:
        for evento in eventos:
            nome = evento[0].replace("'", "''")       # Escapa aspas simples
            descricao = evento[1].replace("'", "''")
            id_reserva = evento[2]
            insert_sql = (
                f"INSERT INTO EVENTO (NOME, DESCRICAO, ID_RESERVA) "
                f"VALUES ('{nome}', '{descricao}', {id_reserva});\n"
            )
            sql_file.write(insert_sql)

    # Gerar arquivo CSV
    with open(nome_arquivo_csv_eventos, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['NOME', 'DESCRICAO', 'ID_RESERVA'])
        writer.writerows(eventos)

    print(f"Arquivo SQL de eventos gerado: {nome_arquivo_sql_eventos}")
    print(f"Arquivo CSV de eventos gerado: {nome_arquivo_csv_eventos}")
    print(f"Total de reservas: {total_reservas}")
    print(f"Total de eventos gerados: {len(eventos)} ({len(eventos)/total_reservas:.0%})")

# Executa o gerador
gerar_eventos('reservas.csv', 'upgrade_evento.sql', 'eventos.csv')
