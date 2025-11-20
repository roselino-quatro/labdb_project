import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

# Função para gerar um número de conselho aleatório
def gerar_numero_conselho():
    return f"CREF {random.randint(100000, 999999)}-{random.choice(['G', 'M', 'X', 'P', 'T', 'Q', 'R', 'S', 'U', 'V'])}"

# Função para gerar os dados de educador físico para 10% dos funcionários
def gerar_educadores_fisicos(dbsession):
    # Buscar todos os funcionários do banco
    funcionarios_result = dbsession.fetch_all("SELECT CPF_INTERNO FROM FUNCIONARIO ORDER BY CPF_INTERNO")
    cpfs_funcionarios = [row['cpf_interno'] for row in funcionarios_result]

    # Calcular 10% dos funcionários
    total_funcionarios = len(cpfs_funcionarios)
    percentual_10 = int(total_funcionarios * 0.1)

    # Selecionar aleatoriamente 10% dos funcionários
    cpfs_selecionados = random.sample(cpfs_funcionarios, percentual_10)

    # Montar os dados para o educador físico
    educadores_data = []
    for cpf_funcionario in cpfs_selecionados:
        numero_conselho = gerar_numero_conselho()
        educadores_data.append((cpf_funcionario, numero_conselho))

    # Inserir diretamente no banco
    query = """
        INSERT INTO EDUCADOR_FISICO (CPF_FUNCIONARIO, NUMERO_CONSELHO)
        VALUES (%s, %s)
    """

    print(f"Inserindo {len(educadores_data)} educadores físicos no banco...")
    dbsession.executemany(query, educadores_data)
    print(f"✅ {len(educadores_data)} educadores físicos inseridos com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_educadores_fisicos(dbsession)
    finally:
        dbsession.close()
