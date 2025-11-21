import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

# Função para gerar uma restrição física aleatória
def gerar_restricao_fisica():
    restricoes = [
        'Lesão no joelho',
        'Problemas de coluna',
        'Deslocamento no ombro',
        'Restrição para atividades de impacto',
        'Hipertensão',
        'Problemas cardíacos',
        'Lesão no tornozelo',
        'Artrite',
        'Asma',
        'Deficiência auditiva'
    ]
    return random.choice(restricoes)

# Função para gerar os dados de restrição física para 10% dos funcionários
def gerar_restricoes_funcionario(dbsession):
    # Buscar todos os funcionários do banco
    funcionarios_result = dbsession.fetch_all("SELECT CPF_INTERNO FROM FUNCIONARIO ORDER BY CPF_INTERNO")
    cpfs_funcionarios = [row['cpf_interno'] for row in funcionarios_result]

    # Calcular 10% dos funcionários
    total_funcionarios = len(cpfs_funcionarios)
    percentual_10 = int(total_funcionarios * 0.1)

    # Selecionar aleatoriamente 10% dos funcionários
    cpfs_selecionados = random.sample(cpfs_funcionarios, percentual_10)

    # Montar os dados para a restrição física
    restricoes_data = []
    for cpf_funcionario in cpfs_selecionados:
        restricao_fisica = gerar_restricao_fisica()
        restricoes_data.append((cpf_funcionario, restricao_fisica))

    # Inserir diretamente no banco
    query = """
        INSERT INTO FUNCIONARIO_RESTRICAO (CPF_FUNCIONARIO, RESTRICAO_FISICA)
        VALUES (%s, %s)
    """

    print(f"Inserindo {len(restricoes_data)} restrições no banco...")
    dbsession.executemany(query, restricoes_data)
    print(f"✅ {len(restricoes_data)} restrições inseridas com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_restricoes_funcionario(dbsession)
    finally:
        dbsession.close()
