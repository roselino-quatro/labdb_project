import csv
import random
from datetime import time, timedelta, datetime

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
def popular_ocorrencias(nome_arquivo_atividades, nome_arquivo_sql, nome_arquivo_csv):
    # Ler CSV de atividades (com ID_ATIVIDADE na primeira coluna)
    atividades = []
    with open(nome_arquivo_atividades, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Pular cabeçalho
        for row in reader:
            atividades.append({
                'id': int(row[0]),
                'nome': row[1],
                'vagas_limite': int(row[2]),
                'data_inicio_periodo': row[3],
                'data_fim_periodo': row[4]
            })

    # Gerar ocorrências semanais
    ocorrencias = []
    for atividade in atividades:
        for _ in range(3):  # 3 ocorrências por atividade
            id_atividade = atividade['id']
            id_instalacao = random.randint(1, 16)  # Ajuste conforme seu banco
            dia_semana = gerar_dia_semana()
            horario_inicio = gerar_horario_inicio()
            horario_fim = gerar_horario_fim(horario_inicio)
            ocorrencias.append([id_atividade, id_instalacao, dia_semana, horario_inicio, horario_fim])

    # Salvar arquivo SQL
    with open(nome_arquivo_sql, 'w', encoding='utf-8') as sql_file:
        for ocorrencia in ocorrencias:
            insert_sql = (
                f"INSERT INTO OCORRENCIA_SEMANAL "
                f"(ID_ATIVIDADE, ID_INSTALACAO, DIA_SEMANA, HORARIO_INICIO, HORARIO_FIM) "
                f"VALUES ({ocorrencia[0]}, {ocorrencia[1]}, '{ocorrencia[2]}', "
                f"'{ocorrencia[3]}', '{ocorrencia[4]}');\n"
            )
            sql_file.write(insert_sql)

    # Salvar arquivo CSV
    with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_ATIVIDADE', 'ID_INSTALACAO', 'DIA_SEMANA', 'HORARIO_INICIO', 'HORARIO_FIM'])
        writer.writerows(ocorrencias)

    print(f"Arquivo SQL de ocorrências gerado: {nome_arquivo_sql}")
    print(f"Arquivo CSV de ocorrências gerado: {nome_arquivo_csv}")

# Executa o gerador
popular_ocorrencias('atividades.csv', 'upgrade_ocorrencia_semanal.sql', 'ocorrencias.csv')
