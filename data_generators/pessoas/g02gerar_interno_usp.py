import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

# Função para gerar um NUSP aleatório (exemplo)
def gerar_nusp():
    return f"{random.randint(1000000000, 9999999999)}"

# Função para gerar uma categoria aleatória
def gerar_categoria():
    categorias = ['ALUNO_GRADUACAO', 'ALUNO_MESTRADO', 'ALUNO_DOUTORADO', 'FUNCIONARIO']
    return random.choice(categorias)

# Função para dividir os dados em 90% para internos e 10% para pessoas restantes
def gerar_interno_usp(dbsession):
    # Buscar todas as pessoas do banco
    pessoas_result = dbsession.fetch_all("SELECT CPF, EMAIL FROM PESSOA ORDER BY CPF")
    cpfs = [row['cpf'] for row in pessoas_result]

    # Garantir que a pessoa com email fixo seja interna
    pessoa_teste_result = dbsession.fetch_one("SELECT CPF FROM PESSOA WHERE EMAIL = 'teste@usp.br'")
    cpf_teste = pessoa_teste_result['cpf'] if pessoa_teste_result else None

    # Remover o CPF de teste da lista para garantir que será incluído
    if cpf_teste and cpf_teste in cpfs:
        cpfs.remove(cpf_teste)

    # Embaralhar os dados para garantir a aleatoriedade
    random.shuffle(cpfs)

    # Calcular a quantidade para 90% e 10%
    total_pessoas = len(cpfs) + (1 if cpf_teste else 0)
    percentual_90 = int(total_pessoas * 0.9)

    # Ajustar para garantir que o teste seja incluído
    if cpf_teste:
        percentual_90 = max(percentual_90, 1)

    # Separar os dados (garantir que teste está nos internos)
    cpfs_internos = cpfs[:percentual_90 - (1 if cpf_teste else 0)]
    if cpf_teste:
        cpfs_internos.insert(0, cpf_teste)  # Inserir no início para garantir

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
