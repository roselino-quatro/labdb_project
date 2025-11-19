import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from dbsession import DBSession

def gerar_data_reserva():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).date()

def gerar_horarios_reserva():
    start_hour = 8
    end_hour = 20
    hora = random.randint(start_hour, end_hour - 1)
    minuto = random.choice([0, 30])
    horario_inicio = datetime.strptime(f"{hora:02d}:{minuto:02d}", "%H:%M")

    # Reservas de equipamento costumam ser mais curtas
    duracao = random.choice([60, 120])
    horario_fim = horario_inicio + timedelta(minutes=duracao)

    return horario_inicio.time(), horario_fim.time()

def gerar_reservas_equipamento(dbsession):
    # Buscar pessoas internas do banco
    internos_result = dbsession.fetch_all("SELECT CPF_PESSOA FROM INTERNO_USP ORDER BY CPF_PESSOA")
    cpfs_internos = [row['cpf_pessoa'] for row in internos_result]

    # Buscar equipamentos reserváveis do banco
    equipamentos_result = dbsession.fetch_all("SELECT ID_PATRIMONIO FROM EQUIPAMENTO WHERE EH_RESERVAVEL = 'S' ORDER BY ID_PATRIMONIO")
    ids_equipamentos = [row['id_patrimonio'] for row in equipamentos_result]

    if not ids_equipamentos:
        print("ERRO: Nenhum equipamento reservável encontrado no banco.")
        return

    reservas_data = []
    reservas_check = set()

    # Gerar cerca de 500 reservas fictícias
    for _ in range(500):
        cpf_responsavel = random.choice(cpfs_internos)
        id_equipamento = random.choice(ids_equipamentos)

        tentativas = 0
        while tentativas < 5:
            data_reserva = gerar_data_reserva()
            h_inicio, h_fim = gerar_horarios_reserva()

            # Chave única simplificada para evitar colisões no gerador
            chave = (id_equipamento, data_reserva, h_inicio)

            if chave not in reservas_check:
                reservas_check.add(chave)
                reservas_data.append((id_equipamento, cpf_responsavel, data_reserva, h_inicio, h_fim))
                break
            tentativas += 1

    # Inserir diretamente no banco
    query = """
        INSERT INTO RESERVA_EQUIPAMENTO (ID_EQUIPAMENTO, CPF_RESPONSAVEL_INTERNO, DATA_RESERVA, HORARIO_INICIO, HORARIO_FIM)
        VALUES (%s, %s, %s, %s, %s)
    """

    print(f"Inserindo {len(reservas_data)} reservas de equipamento no banco...")
    dbsession.executemany(query, reservas_data)
    print(f"✅ {len(reservas_data)} reservas de equipamento inseridas com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_reservas_equipamento(dbsession)
    finally:
        dbsession.close()
