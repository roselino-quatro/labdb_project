import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

# Função para gerar um NUSP aleatório (5 a 8 dígitos)
def gerar_nusp():
    return f"{random.randint(10000, 99999999)}"

# Função para gerar uma categoria aleatória
def gerar_categoria():
    categorias = ['ALUNO_GRADUACAO', 'ALUNO_MESTRADO', 'ALUNO_DOUTORADO', 'FUNCIONARIO']
    return random.choice(categorias)

# Função para dividir os dados em 90% para internos e 10% para pessoas restantes
def gerar_interno_usp(dbsession):
    # Emails fixos para garantir que sejam internos
    EMAILS_TESTE = ["admin@usp.br", "interno@usp.br", "funcionario@usp.br", "cadastro@usp.br"]

    # Buscar todas as pessoas do banco
    pessoas_result = dbsession.fetch_all("SELECT CPF, EMAIL FROM PESSOA ORDER BY CPF")
    cpfs = [row['cpf'] for row in pessoas_result]

    # Garantir que as pessoas com emails fixos sejam internas
    cpfs_teste = []
    for email_teste in EMAILS_TESTE:
        pessoa_teste_result = dbsession.fetch_one(f"SELECT CPF FROM PESSOA WHERE EMAIL = '{email_teste}'")
        if pessoa_teste_result:
            cpf_teste = pessoa_teste_result['cpf']
            if cpf_teste in cpfs:
                cpfs.remove(cpf_teste)
                cpfs_teste.append(cpf_teste)

    # Embaralhar os dados para garantir a aleatoriedade
    random.shuffle(cpfs)

    # Calcular a quantidade para 90% e 10%
    total_pessoas = len(cpfs) + len(cpfs_teste)
    percentual_90 = int(total_pessoas * 0.9)

    # Ajustar para garantir que os testes sejam incluídos
    if cpfs_teste:
        percentual_90 = max(percentual_90, len(cpfs_teste))

    # Separar os dados (garantir que testes estão nos internos)
    cpfs_internos = cpfs[:percentual_90 - len(cpfs_teste)]
    # Inserir os CPFs de teste no início para garantir
    cpfs_internos = cpfs_teste + cpfs_internos

    # Preparar dados para inserção no banco
    internos_data = []
    for cpf_pessoa in cpfs_internos:
        nusp = gerar_nusp()
        categoria = gerar_categoria()
        internos_data.append((cpf_pessoa, nusp, categoria))

    # Inserir diretamente no banco
    query = """
        INSERT INTO INTERNO_USP (CPF_PESSOA, NUSP, CATEGORIA)
        VALUES (%s, %s, %s)
    """

    print(f"Inserindo {len(internos_data)} internos no banco...")
    dbsession.executemany(query, internos_data)
    print(f"✅ {len(internos_data)} internos inseridos com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_interno_usp(dbsession)
    finally:
        dbsession.close()
