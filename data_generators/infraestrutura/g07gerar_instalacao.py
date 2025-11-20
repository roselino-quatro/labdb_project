import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

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

def gerar_instalacoes(dbsession, num_registros):
    """
    Gera dados únicos e coerentes para a tabela INSTALACAO
    e insere diretamente no banco.
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
    instalacoes_data = []
    for id_inst, (nome, tipo) in enumerate(instalacoes_selecionadas, start=1):
        capacidade = gerar_capacidade()
        eh_reservavel = gerar_reservavel(tipo)

        instalacoes_data.append((id_inst, nome, tipo, capacidade, eh_reservavel))

    # Inserir diretamente no banco
    query = """
        INSERT INTO INSTALACAO (ID_INSTALACAO, NOME, TIPO, CAPACIDADE, EH_RESERVAVEL)
        VALUES (%s, %s, %s, %s, %s)
    """

    print(f"Inserindo {len(instalacoes_data)} instalações no banco...")
    dbsession.executemany(query, instalacoes_data)
    print(f"✅ {len(instalacoes_data)} instalações inseridas com sucesso!")


if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_instalacoes(dbsession, 20)
    finally:
        dbsession.close()
