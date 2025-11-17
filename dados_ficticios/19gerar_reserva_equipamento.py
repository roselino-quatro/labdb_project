import csv
import random
from datetime import datetime, timedelta

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

def gerar_reservas_equipamento(arquivo_internos, arquivo_equipamentos, arquivo_sql, arquivo_csv):
    # Carregar Pessoas
    with open(arquivo_internos, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        pessoas = list(reader)

    # Carregar Equipamentos e FILTRAR apenas os reserváveis
    with open(arquivo_equipamentos, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) # Pula cabeçalho
        equipamentos_reservaveis = [row for row in reader if row[5] == 'S']

    if not equipamentos_reservaveis:
        print("ERRO: Nenhum equipamento reservável encontrado no CSV.")
        return

    reservas = []
    reservas_check = set()

    # Gerar cerca de 500 reservas fictícias
    for _ in range(500):
        pessoa = random.choice(pessoas)
        cpf_responsavel = pessoa[0]
        
        equipamento = random.choice(equipamentos_reservaveis)
        id_equipamento = equipamento[0]
        
        tentativas = 0
        while tentativas < 5:
            data_reserva = gerar_data_reserva()
            h_inicio, h_fim = gerar_horarios_reserva()
            
            # Chave única simplificada para evitar colisões no gerador
            chave = (id_equipamento, data_reserva, h_inicio)
            
            if chave not in reservas_check:
                reservas_check.add(chave)
                reservas.append([id_equipamento, cpf_responsavel, data_reserva, h_inicio, h_fim])
                break
            tentativas += 1

    # Gerar SQL
    with open(arquivo_sql, 'w', encoding='utf-8') as sql_file:
        for r in reservas:
            # Observação: Não passamos o ID da reserva, pois é SERIAL/IDENTITY
            insert_sql = (
                "INSERT INTO RESERVA_EQUIPAMENTO (ID_EQUIPAMENTO, CPF_RESPONSAVEL_INTERNO, DATA_RESERVA, HORARIO_INICIO, HORARIO_FIM) "
                f"VALUES ('{r[0]}', '{r[1]}', '{r[2]}', '{r[3]}', '{r[4]}');\n"
            )
            sql_file.write(insert_sql)

    # Gerar CSV
    with open(arquivo_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_EQUIPAMENTO', 'CPF_RESPONSAVEL_INTERNO', 'DATA_RESERVA', 'HORARIO_INICIO', 'HORARIO_FIM'])
        writer.writerows(reservas)

    print(f"Arquivo SQL de reservas de equipamento gerado: {arquivo_sql}")
    print(f"Arquivo CSV de reservas de equipamento gerado: {arquivo_csv}")

if __name__ == "__main__":
    gerar_reservas_equipamento('pessoas_internas.csv', 'equipamentos.csv', 'upgrade_reserva_equipamento.sql', 'reservas_equipamento.csv')