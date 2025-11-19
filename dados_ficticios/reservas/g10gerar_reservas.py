import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from dbsession import DBSession

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
def gerar_reservas(dbsession):
    # Buscar pessoas internas
    internos_result = dbsession.fetch_all("SELECT CPF_PESSOA FROM INTERNO_USP ORDER BY CPF_PESSOA")
    cpfs_internos = [row['cpf_pessoa'] for row in internos_result]

    # Buscar instalações
    instalacoes_result = dbsession.fetch_all("SELECT ID_INSTALACAO FROM INSTALACAO ORDER BY ID_INSTALACAO")
    ids_instalacoes = [row['id_instalacao'] for row in instalacoes_result]

    # Selecionar 50% das pessoas aleatoriamente
    total_pessoas = len(cpfs_internos)
    percentual_50 = int(total_pessoas * 0.5)
    cpfs_selecionados = random.sample(cpfs_internos, percentual_50)

    reservas_data = []
    reservas_existentes = set()  # Tuplas (id_instalacao, data_reserva, horario_inicio)

    # Gerar reservas sem duplicar a chave única
    for cpf_responsavel in cpfs_selecionados:
        tentativas = 0
        while tentativas < 10:  # Evitar loop infinito
            id_instalacao = random.choice(ids_instalacoes)
            data_reserva = gerar_data_reserva()
            horario_inicio, horario_fim = gerar_horarios_reserva()
            chave = (id_instalacao, data_reserva, horario_inicio)

            if chave not in reservas_existentes:
                reservas_existentes.add(chave)
                reservas_data.append((id_instalacao, cpf_responsavel, data_reserva, horario_inicio, horario_fim))
                break
            tentativas += 1

    # Inserir diretamente no banco
    query = """
        INSERT INTO RESERVA (ID_INSTALACAO, CPF_RESPONSAVEL_INTERNO, DATA_RESERVA, HORARIO_INICIO, HORARIO_FIM)
        VALUES (%s, %s, %s, %s, %s)
    """

    print(f"Inserindo {len(reservas_data)} reservas no banco...")
    dbsession.executemany(query, reservas_data)
    print(f"✅ {len(reservas_data)} reservas inseridas com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_reservas(dbsession)
    finally:
        dbsession.close()
