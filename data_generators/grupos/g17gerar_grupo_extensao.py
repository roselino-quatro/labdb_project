import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from dbsession import DBSession

# Lista fixa de nomes de grupos de extensão
NOMES_GRUPOS_EXTENSAO = [
    'Grupo de Karatê Shotokan',
    'Equipe Kung Fu Garra de Águia',
    'Grupo de Estudos Tai Chi Chuan',
    'Projeto Capoeira Angola'
]

def gerar_grupos_extensao(dbsession, quantidade_grupos=4):
    """
    Gera dados fictícios para GRUPO_EXTENSAO com base em nomes fixos
    e insere diretamente no banco.
    """

    # Buscar CPFs dos internos do banco
    internos_result = dbsession.fetch_all("SELECT CPF_PESSOA FROM INTERNO_USP ORDER BY CPF_PESSOA")
    cpfs_internos = [row['cpf_pessoa'] for row in internos_result]

    if not cpfs_internos:
        print("Aviso: Nenhum interno encontrado no banco.")
        return

    # Definir quantos grupos gerar
    num_a_selecionar = min(quantidade_grupos, len(NOMES_GRUPOS_EXTENSAO))
    if quantidade_grupos > len(NOMES_GRUPOS_EXTENSAO):
        print(f"Aviso: Solicitados {quantidade_grupos} grupos, mas só existem {len(NOMES_GRUPOS_EXTENSAO)} nomes disponíveis.")

    nomes_selecionados = random.sample(NOMES_GRUPOS_EXTENSAO, num_a_selecionar)

    # Gerar os dados dos grupos
    grupos_data = []
    for nome in nomes_selecionados:
        descricao = f"{nome} é um grupo de extensão promovido pelo CEFER."
        cpf_responsavel = random.choice(cpfs_internos)
        grupos_data.append((nome, descricao, cpf_responsavel))

    # Inserir diretamente no banco
    query = """
        INSERT INTO GRUPO_EXTENSAO (NOME_GRUPO, DESCRICAO, CPF_RESPONSAVEL_INTERNO)
        VALUES (%s, %s, %s)
    """

    print(f"Inserindo {len(grupos_data)} grupos de extensão no banco...")
    dbsession.executemany(query, grupos_data)
    print(f"✅ {len(grupos_data)} grupos inseridos com sucesso!")
    print(f"Total de grupos gerados: {len(grupos_data)}")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_grupos_extensao(dbsession, quantidade_grupos=4)
    finally:
        dbsession.close()
