import csv
import random
from datetime import datetime, timedelta

# Função para gerar um ID de patrimônio único (simulando)
def gerar_id_patrimonio(ids_gerados):
    # Gerar um ID aleatório até que seja único
    while True:
        id_patrimonio = f"EQ{random.randint(100000, 999999)}"
        if id_patrimonio not in ids_gerados:
            ids_gerados.add(id_patrimonio)
            return id_patrimonio

# Função para gerar o nome do equipamento
def gerar_nome_equipamento():
    equipamentos = [
        # Musculação
        "Halter de 5kg", "Halter de 10kg", "Barras Olímpicas", "Banco de Musculação", "Anilha de 5kg",
        "Anilha de 10kg", "Peso para Tornozelo", "Rack para Agachamento", "Leg Press", "Máquina de Abdominal",
        
        # Treinamento Funcional
        "Corda de Pular", "Kettlebell", "Slamball", "Medicine Ball", "Cordas de Batalha", 
        "Caixa Pliométrica", "Cone de Agilidade", "Bolsa de Areia", "Ball Slam", "Bola de Pilates",

        # Esportes Coletivos
        "Bola de Futebol", "Bola de Vôlei", "Bola de Basquete", "Rede de Vôlei", "Cesta de Basquete", 
        "Trave de Futebol", "Goalball", "Mini Quadra de Futsal", "Bola de Handebol", "Bola de Rugby",

        # Esportes Individuais
        "Raquete de Tênis", "Raquete de Badminton", "Raquete de Ping-Pong", "Bola de Golfe", "Taco de Beisebol", 
        "Arco e Flecha", "Skateboard", "Bola de Skate", "Prancha de Surfe", "Bola de Tênis",

        # Yoga e Pilates
        "Tapete de Yoga", "Almofada de Meditação", "Faixa de Resistência", "Bola de Pilates", 
        "Rolo de Espuma", "Peso de Mão para Yoga", "Almofada de Descanso", "Rolo de Alta Performance",
        
        # Equipamentos Aquáticos
        "Prancha de Surfe", "Palmar de Natação", "Nadadeiras", "Bolha para Hidroginástica", 
        "Boia de Natação", "Prancha de Stand-Up Paddle", "Cinto de Flutuação", "Máscara de Mergulho",

        # Outros Equipamentos
        "Bicicleta Ergométrica", "Elíptico", "Colchonete de Exercício", "Barra de Apoio", "Rolo de Alta Performance",
        "Colchonete de Pilates", "Cordas de Escada", "Protetores de Tornozelo", "Bola de Basquete de Rua"
    ]
    return random.choice(equipamentos)

# Função para gerar o preço de aquisição aleatório
def gerar_preco_aquisicao():
    return round(random.uniform(50.00, 5000.00), 2)  # Preço entre 50 e 5000

# Função para gerar uma data de aquisição aleatória
def gerar_data_aquisicao():
    start_date = datetime(2015, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).date()

# Função para gerar os 1000 equipamentos
def gerar_equipamentos(nome_arquivo_csv_instalacao, nome_arquivo_sql_equipamento, nome_arquivo_csv_equipamento):
    # Ler as instalações do arquivo CSV
    with open(nome_arquivo_csv_instalacao, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Pega o cabeçalho
        instalacoes = list(reader)  # Lista de instalações

    equipamentos = []
    ids_gerados = set()  # Conjunto para armazenar os IDs de patrimônio já gerados

    # Gerar 1000 equipamentos
    for _ in range(1000):
        id_patrimonio = gerar_id_patrimonio(ids_gerados)  # Gera um ID único
        nome_equipamento = gerar_nome_equipamento()
        id_instalacao_local = int(random.choice(instalacoes)[0])  # Pega o ID_INSTALACAO
        preco_aquisicao = gerar_preco_aquisicao()
        data_aquisicao = gerar_data_aquisicao()

        # Adicionar o equipamento gerado à lista
        equipamentos.append([id_patrimonio, nome_equipamento, id_instalacao_local, preco_aquisicao, data_aquisicao])

    # Gerar o arquivo SQL com os dados dos equipamentos
    with open(nome_arquivo_sql_equipamento, 'w', encoding='utf-8') as sql_file:
        for eq in equipamentos:
            insert_sql = f"INSERT INTO EQUIPAMENTO (ID_PATRIMONIO, NOME, ID_INSTALACAO_LOCAL, PRECO_AQUISICAO, DATA_AQUISICAO) " \
                         f"VALUES ('{eq[0]}', '{eq[1]}', '{eq[2]}', {eq[3]}, '{eq[4]}');\n"
            sql_file.write(insert_sql)

    # Gerar o arquivo CSV com os equipamentos
    with open(nome_arquivo_csv_equipamento, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_PATRIMONIO', 'NOME', 'ID_INSTALACAO_LOCAL', 'PRECO_AQUISICAO', 'DATA_AQUISICAO'])  # Cabeçalho
        writer.writerows(equipamentos)

    print(f"Arquivo SQL de equipamentos gerado: {nome_arquivo_sql_equipamento}")
    print(f"Arquivo CSV de equipamentos gerado: {nome_arquivo_csv_equipamento}")

# Executa o gerador
gerar_equipamentos('instalacoes.csv', 'upgrade_equipamento.sql', 'equipamentos.csv')
