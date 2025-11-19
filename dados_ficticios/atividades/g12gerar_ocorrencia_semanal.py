import random
import sys
from datetime import time, timedelta, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from dbsession import DBSession

# Função para gerar um horário aleatório de início
# (somente horas cheias ou meia hora, entre 08:00 e 18:00)
def gerar_horario_inicio():
    hora = random.randint(8, 18)  # Entre 08:00 e 18:00
    minuto = random.choice([0, 30])  # Apenas :00 ou :30
    return time(hora, minuto)

# Função para gerar um horário de fim (mínimo 1h e máximo 2h depois do início)
def gerar_horario_fim(horario_inicio):
    # Duração entre 60 e 120 minutos
    duracao_minutos = random.randint(60, 120)

    inicio_dt = datetime.combine(datetime.today(), horario_inicio)
    fim_dt = inicio_dt + timedelta(minutes=duracao_minutos)

    # Se ultrapassar 22h, ajusta para 22:00
    if fim_dt.hour >= 22:
        fim_dt = datetime.combine(datetime.today(), time(22, 0))

    return fim_dt.time()

# Função para gerar um dia da semana aleatório
def gerar_dia_semana():
    dias = ['SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO', 'DOMINGO']
    return random.choice(dias)

# Função para popular a tabela OCORRENCIA_SEMANAL
def popular_ocorrencias(dbsession):
    # Buscar atividades do banco
    atividades_result = dbsession.fetch_all("SELECT ID_ATIVIDADE FROM ATIVIDADE ORDER BY ID_ATIVIDADE")
    ids_atividades = [row['id_atividade'] for row in atividades_result]

    # Buscar instalações disponíveis do banco
    instacoes_result = dbsession.fetch_all("SELECT ID_INSTALACAO FROM INSTALACAO ORDER BY ID_INSTALACAO")
    ids_instalacoes = [row['id_instalacao'] for row in instacoes_result] if instacoes_result else []

    if not ids_instalacoes:
        raise ValueError("Nenhuma instalação encontrada no banco!")

    # Gerar ocorrências semanais
    ocorrencias_data = []
    for id_atividade in ids_atividades:
        for _ in range(3):  # 3 ocorrências por atividade
            id_instalacao = random.choice(ids_instalacoes)
            dia_semana = gerar_dia_semana()
            horario_inicio = gerar_horario_inicio()
            horario_fim = gerar_horario_fim(horario_inicio)

            ocorrencias_data.append((id_atividade, id_instalacao, dia_semana, horario_inicio, horario_fim))

    # Inserir diretamente no banco
    query = """
        INSERT INTO OCORRENCIA_SEMANAL (ID_ATIVIDADE, ID_INSTALACAO, DIA_SEMANA, HORARIO_INICIO, HORARIO_FIM)
        VALUES (%s, %s, %s, %s, %s)
    """

    print(f"Inserindo {len(ocorrencias_data)} ocorrências semanais no banco...")
    dbsession.executemany(query, ocorrencias_data)
    print(f"✅ {len(ocorrencias_data)} ocorrências semanais inseridas com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        popular_ocorrencias(dbsession)
    finally:
        dbsession.close()
