import random
import sys
from faker import Faker
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

fake = Faker('pt_BR')

def gerar_eventos(dbsession):
    # Buscar reservas existentes do banco
    reservas_result = dbsession.fetch_all("SELECT ID_RESERVA FROM RESERVA ORDER BY ID_RESERVA")
    ids_reservas = [row['id_reserva'] for row in reservas_result]

    total_reservas = len(ids_reservas)

    # Seleciona 50% das reservas para gerar eventos
    reservas_evento = random.sample(ids_reservas, int(total_reservas * 0.5))
    total_eventos = len(reservas_evento)

    # Gerar os eventos com nomes únicos usando índice
    eventos_data = []
    for i, id_reserva in enumerate(reservas_evento, start=1):
        nome_evento = f"{fake.catch_phrase()} #{i}"  # Sufixo garante unicidade
        descricao = fake.paragraph(nb_sentences=random.randint(2, 5))
        eventos_data.append((nome_evento, descricao, id_reserva))

    # Inserir diretamente no banco
    query = """
        INSERT INTO EVENTO (NOME, DESCRICAO, ID_RESERVA)
        VALUES (%s, %s, %s)
    """

    print(f"Inserindo {len(eventos_data)} eventos no banco...")
    dbsession.executemany(query, eventos_data)
    print(f"✅ {len(eventos_data)} eventos inseridos com sucesso!")
    print(f"Total de reservas: {total_reservas}")
    print(f"Total de eventos gerados: {len(eventos_data)} ({len(eventos_data)/total_reservas:.0%})")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_eventos(dbsession)
    finally:
        dbsession.close()
