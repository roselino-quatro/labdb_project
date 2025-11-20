import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

# Função para gerar uma formação aleatória (exemplo)
def gerar_formacao():
    formacoes = ['Bacharelado', 'Mestrado', 'Doutorado', 'Técnico', 'Especialização']
    return random.choice(formacoes)

# Função para separar 20% dos dados dos 90% já processados
def gerar_funcionarios(dbsession):
    # Buscar todos os internos do banco
    internos_result = dbsession.fetch_all("SELECT CPF_PESSOA FROM INTERNO_USP ORDER BY CPF_PESSOA")
    cpfs_internos = [row['cpf_pessoa'] for row in internos_result]

    # Embaralhar os dados para garantir aleatoriedade
    random.shuffle(cpfs_internos)

    # Calcular a quantidade de 20% dos dados dos 90%
    total_internos = len(cpfs_internos)
    percentual_20 = int(total_internos * 0.2)

    # Separar os 20% dos dados
    cpfs_funcionarios = cpfs_internos[:percentual_20]

    # Preparar dados para inserção no banco
    funcionarios_data = []
    for cpf_pessoa in cpfs_funcionarios:
        formacao = gerar_formacao()
        funcionarios_data.append((cpf_pessoa, formacao))

    # Inserir diretamente no banco
    query = """
        INSERT INTO FUNCIONARIO (CPF_INTERNO, FORMACAO)
        VALUES (%s, %s)
    """

    print(f"Inserindo {len(funcionarios_data)} funcionários no banco...")
    dbsession.executemany(query, funcionarios_data)
    print(f"✅ {len(funcionarios_data)} funcionários inseridos com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_funcionarios(dbsession)
    finally:
        dbsession.close()
