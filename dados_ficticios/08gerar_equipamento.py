import csv
import random
from datetime import datetime, timedelta

# Listas separadas logicamente
ITENS_RESERVAVEIS = [
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
    "Boia de Natação", "Prancha de Stand-Up Paddle", "Cinto de Flutuação", "Máscara de Mergulho"
]

ITENS_NAO_RESERVAVEIS = [
     # Musculação
    "Halter de 5kg", "Halter de 10kg", "Barras Olímpicas", "Banco de Musculação", "Anilha de 5kg",
    "Anilha de 10kg", "Peso para Tornozelo", "Rack para Agachamento", "Leg Press", "Máquina de Abdominal",
    
    # Outros Equipamentos
    "Bicicleta Ergométrica", "Elíptico", "Colchonete de Exercício", "Barra de Apoio", "Rolo de Alta Performance",
    "Colchonete de Pilates", "Cordas de Escada", "Protetores de Tornozelo", "Bola de Basquete de Rua"
]

def gerar_id_patrimonio(ids_gerados):
    while True:
        id_patrimonio = f"EQ{random.randint(100000, 999999)}"
        if id_patrimonio not in ids_gerados:
            ids_gerados.add(id_patrimonio)
            return id_patrimonio

def gerar_preco_aquisicao(eh_reservavel):
    if eh_reservavel == 'N':
        return round(random.uniform(1000.00, 15000.00), 2)
    if eh_reservavel == 'S':
        return round(random.uniform(100.00, 500.00), 2)

def gerar_data_aquisicao():
    start_date = datetime(2018, 1, 1)
    end_date = datetime(2023, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_days)).date()

def gerar_equipamentos(nome_arquivo_csv_instalacao, nome_arquivo_sql_equipamento, nome_arquivo_csv_equipamento):
    # Ler as instalações do arquivo CSV
    with open(nome_arquivo_csv_instalacao, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        instalacoes = list(reader)

    # Classificar as instalações para saber onde guardar as coisas
    locais_academia = []
    locais_deposito = []
    todos_locais = []

    for inst in instalacoes:
        id_inst = int(inst[0])
        nome = inst[1].upper()
        tipo = inst[2].upper()
        todos_locais.append(id_inst)
        
        # Regra para Academia
        if 'ACADEMIA' in tipo or 'MUSCULAÇÃO' in nome or 'MUSCULACAO' in nome:
            locais_academia.append(id_inst)
        
        # Regra para Depósito
        if 'DEPÓSITO' in nome or 'DEPOSITO' in nome or 'SALA' in tipo:
            locais_deposito.append(id_inst)
    
    # Fallbacks de segurança (caso não encontre nenhum específico, usa qualquer um para não quebrar)
    if not locais_academia:
        print("AVISO: Nenhuma instalação do tipo 'Academia' encontrada. Usando locais aleatórios.")
        locais_academia = todos_locais
    if not locais_deposito:
        print("AVISO: Nenhuma instalação do tipo 'Sala' ou 'Depósito' encontrada. Usando locais aleatórios.")
        locais_deposito = todos_locais

    equipamentos = []
    ids_gerados = set()

    for _ in range(200):
        id_patrimonio = gerar_id_patrimonio(ids_gerados)
        
        if random.choice([True, False]):
            # Caso: Item NÃO RESERVÁVEL (Academia)
            nome_equipamento = random.choice(ITENS_NAO_RESERVAVEIS)
            eh_reservavel = 'N'
            # Logica: Se é não reservável e de academia, fica na academia
            id_instalacao_local = random.choice(locais_academia)
        else:
            # Caso: Item RESERVÁVEL (Depósito)
            nome_equipamento = random.choice(ITENS_RESERVAVEIS)
            eh_reservavel = 'S'
            # Logica: Caso contrário (reservável), fica na sala de depósito
            id_instalacao_local = random.choice(locais_deposito)

        preco_aquisicao = gerar_preco_aquisicao(eh_reservavel)
        data_aquisicao = gerar_data_aquisicao()

        equipamentos.append([id_patrimonio, nome_equipamento, id_instalacao_local, preco_aquisicao, data_aquisicao, eh_reservavel])

    # Gerar o arquivo SQL
    with open(nome_arquivo_sql_equipamento, 'w', encoding='utf-8') as sql_file:
        for eq in equipamentos:
            insert_sql = f"INSERT INTO EQUIPAMENTO (ID_PATRIMONIO, NOME, ID_INSTALACAO_LOCAL, PRECO_AQUISICAO, DATA_AQUISICAO, EH_RESERVAVEL) " \
                         f"VALUES ('{eq[0]}', '{eq[1]}', '{eq[2]}', {eq[3]}, '{eq[4]}', '{eq[5]}');\n"
            sql_file.write(insert_sql)

    # Gerar o arquivo CSV
    with open(nome_arquivo_csv_equipamento, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_PATRIMONIO', 'NOME', 'ID_INSTALACAO_LOCAL', 'PRECO_AQUISICAO', 'DATA_AQUISICAO', 'EH_RESERVAVEL'])
        writer.writerows(equipamentos)

    print(f"Arquivo SQL de equipamentos gerado: {nome_arquivo_sql_equipamento}")
    print(f"Arquivo CSV de equipamentos gerado: {nome_arquivo_csv_equipamento}")

# Executa o gerador
if __name__ == "__main__":
    gerar_equipamentos('instalacoes.csv', 'upgrade_equipamento.sql', 'equipamentos.csv')