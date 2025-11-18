import csv
import random

# Dicionário de instalações únicas e coerentes
NOMES_INSTALACOES_POR_TIPO = {
    'Quadra': [
        'Quadra Poliesportiva A', 'Quadra Poliesportiva B',
        'Quadra de Tênis 1', 'Quadra de Tênis 2',
        'Quadra de Peteca', 'Quadra de Areia Vôlei', 'Quadra de Areia Beach Tennis'
    ],
    'Piscina': ['Piscina Olímpica', 'Piscina Recreativa'],
    'Academia': ['Academia Principal', 'Espaço Multifuncional Musculação'],
    'Sala': ['Sala de Dança', 'Sala de Ginástica', 'Sala de Alongamento', 'Salão de Eventos', 'Sala de Depoisito'],
    'Campo': ['Campo de Futebol Principal', 'Campo de Futebol Society'],
    'Vestiário': ['Vestiário Masculino A', 'Vestiário Feminino A', 'Vestiário Masculino B', 'Vestiário Feminino B']
}

def gerar_capacidade():
    """Gera capacidade aleatória entre 10 e 200."""
    return random.randint(10, 200)

def gerar_reservavel(tipo):
    """Define se é reservável com base no tipo."""
    return 'N' if tipo == 'Vestiário' else random.choice(['S', 'N'])

def gerar_instalacoes(nome_arquivo_sql, nome_arquivo_csv, num_registros):
    """
    Gera dados únicos e coerentes para a tabela INSTALACAO
    e salva em arquivos CSV e SQL (sem uso de os/pathlib).
    """

    print(f"Gerando {num_registros} instalações únicas...")

    # Cria a lista completa de instalações únicas a partir do dicionário
    instalacoes_unicas = []
    for tipo, nomes in NOMES_INSTALACOES_POR_TIPO.items():
        for nome in nomes:
            instalacoes_unicas.append((nome, tipo))

    # Ajusta caso o número solicitado exceda o disponível
    if num_registros > len(instalacoes_unicas):
        print(f"Aviso: número solicitado ({num_registros}) maior que o total disponível ({len(instalacoes_unicas)}).")
        num_registros = len(instalacoes_unicas)

    # Seleciona instalações únicas aleatoriamente
    instalacoes_selecionadas = random.sample(instalacoes_unicas, num_registros)

    # Gera os registros com ID, capacidade e reservabilidade
    registros_csv = []
    registros_sql = []
    for id_inst, (nome, tipo) in enumerate(instalacoes_selecionadas, start=1):
        capacidade = gerar_capacidade()
        eh_reservavel = gerar_reservavel(tipo)

        registros_csv.append([id_inst, nome, tipo, capacidade, eh_reservavel])

        nome_sql = nome.replace("'", "''")
        tipo_sql = tipo.replace("'", "''")

        insert_sql = (
            f"INSERT INTO INSTALACAO (ID_INSTALACAO, NOME, TIPO, CAPACIDADE, EH_RESERVAVEL) "
            f"VALUES ({id_inst}, '{nome_sql}', '{tipo_sql}', {capacidade}, '{eh_reservavel}');"
        )
        registros_sql.append(insert_sql)

    # Gera o arquivo CSV
    with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['ID_INSTALACAO', 'NOME', 'TIPO', 'CAPACIDADE', 'EH_RESERVAVEL'])
        writer.writerows(registros_csv)

    # Gera o arquivo SQL
    with open(nome_arquivo_sql, 'w', encoding='utf-8') as sql_file:
        sql_file.write('\n'.join(registros_sql))

    print(f"Arquivo CSV gerado em: {nome_arquivo_csv}")
    print(f"Arquivo SQL gerado em: {nome_arquivo_sql}")

# Executa o gerador
gerar_instalacoes('upgrade_instalacao.sql', 'instalacoes.csv', 20)
