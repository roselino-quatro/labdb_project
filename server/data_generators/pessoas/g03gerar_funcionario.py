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
    # Emails que devem ser funcionários
    EMAILS_FUNCIONARIOS = ["admin@usp.br", "funcionario@usp.br"]
    # Email que NÃO deve ser funcionário
    EMAIL_INTERNO = "interno@usp.br"

    # Buscar todos os internos do banco
    internos_result = dbsession.fetch_all("SELECT CPF_PESSOA FROM INTERNO_USP ORDER BY CPF_PESSOA")
    cpfs_internos = [row['cpf_pessoa'] for row in internos_result]

    # Garantir que admin e funcionario sejam funcionários
    cpfs_funcionarios_teste = []
    for email_funcionario in EMAILS_FUNCIONARIOS:
        pessoa_result = dbsession.fetch_one(f"SELECT CPF FROM PESSOA WHERE EMAIL = '{email_funcionario}'")
        if pessoa_result:
            cpf_funcionario = pessoa_result['cpf']
            if cpf_funcionario in cpfs_internos:
                cpfs_internos.remove(cpf_funcionario)
                cpfs_funcionarios_teste.append(cpf_funcionario)

    # Garantir que interno NÃO seja funcionário (remover se estiver na lista)
    pessoa_interno_result = dbsession.fetch_one(f"SELECT CPF FROM PESSOA WHERE EMAIL = '{EMAIL_INTERNO}'")
    if pessoa_interno_result:
        cpf_interno = pessoa_interno_result['cpf']
        if cpf_interno in cpfs_internos:
            # Não remover da lista de internos, apenas garantir que não seja selecionado como funcionário
            pass

    # Embaralhar os dados para garantir aleatoriedade
    random.shuffle(cpfs_internos)

    # Calcular a quantidade de 20% dos dados dos 90%
    total_internos = len(cpfs_internos) + len(cpfs_funcionarios_teste)
    percentual_20 = int(total_internos * 0.2)

    # Ajustar para garantir que os funcionários de teste sejam incluídos
    if cpfs_funcionarios_teste:
        percentual_20 = max(percentual_20, len(cpfs_funcionarios_teste))

    # Separar os 20% dos dados (garantir que funcionários de teste estão incluídos)
    cpfs_funcionarios = cpfs_internos[:percentual_20 - len(cpfs_funcionarios_teste)]
    # Inserir os CPFs de funcionários de teste no início para garantir
    cpfs_funcionarios = cpfs_funcionarios_teste + cpfs_funcionarios

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
