import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

# Senha padrão para testes (será hasheada pelo PostgreSQL)
SENHA_PADRAO = "senha123"
EMAIL_TESTE = "teste@usp.br"


def gerar_usuario_senha(dbsession):
    """
    Gera senhas para todos os internos USP (pessoas que podem fazer login).
    Usa a função hash_password()  para gerar hashes bcrypt.
    """
    # Buscar todos os internos USP
    internos_result = dbsession.fetch_all("SELECT CPF_PESSOA FROM INTERNO_USP")
    cpfs_internos = [row["cpf_pessoa"] for row in internos_result]

    # Verificar se o usuário de teste tem senha
    pessoa_teste_result = dbsession.fetch_one(f"""
        SELECT P.CPF
        FROM PESSOA P
        INNER JOIN INTERNO_USP I ON P.CPF = I.CPF_PESSOA
        WHERE P.EMAIL = '{EMAIL_TESTE}'
    """)

    if pessoa_teste_result:
        cpf_teste = pessoa_teste_result["cpf"]
        print(f"   📧 Usuário de teste encontrado: {EMAIL_TESTE} (CPF: {cpf_teste})")

    if not cpfs_internos:
        print("⚠️  Nenhum interno USP encontrado. Pulando geração de senhas.")
        return

    usuarios_data = []

    # Data base para criação (últimos 6 meses)
    data_base = datetime.now() - timedelta(days=180)

    for cpf_pessoa in cpfs_internos:
        # Gerar data de criação aleatória nos últimos 6 meses
        dias_aleatorios = random.randint(2, 180)
        data_criacao = data_base + timedelta(days=dias_aleatorios)

        # 20% de chance de ter alteração de senha
        if random.random() < 0.2:
            dias_alteracao = random.randint(1, dias_aleatorios)
            data_ultima_alteracao = data_criacao + timedelta(days=dias_alteracao)
        else:
            data_ultima_alteracao = None

        # 5% de chance de estar bloqueado
        bloqueado = random.random() < 0.05

        # Tentativas de login (0-4, se bloqueado pode ter 5+)
        if bloqueado:
            tentativas_login = random.randint(5, 10)
        else:
            tentativas_login = random.randint(0, 3)

        # Data do último login (se não bloqueado e teve tentativas)
        if not bloqueado and tentativas_login > 0:
            dias_ultimo_login = random.randint(1, min(dias_aleatorios, 30))
            data_ultimo_login = data_criacao + timedelta(days=dias_ultimo_login)
        else:
            data_ultimo_login = None

        # Usar função PostgreSQL hash_password() para gerar o hash
        # A senha padrão será "senha123" para facilitar testes
        usuarios_data.append(
            (
                cpf_pessoa,
                data_criacao,
                data_ultima_alteracao,
                bloqueado,
                tentativas_login,
                data_ultimo_login,
            )
        )

    # Inserir usando função PostgreSQL para hash da senha
    query = """
        INSERT INTO USUARIO_SENHA (
            CPF_PESSOA,
            SENHA_HASH,
            DATA_CRIACAO,
            DATA_ULTIMA_ALTERACAO,
            BLOQUEADO,
            TENTATIVAS_LOGIN,
            DATA_ULTIMO_LOGIN
        )
        VALUES (
            %s,
            hash_password(%s),
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """

    print(f"Inserindo {len(usuarios_data)} usuários com senhas no banco...")

    # Preparar dados com senha padrão
    dados_com_senha = [
        (cpf, SENHA_PADRAO, data_criacao, data_alt, bloqueado, tentativas, data_login)
        for cpf, data_criacao, data_alt, bloqueado, tentativas, data_login in usuarios_data
    ]

    dbsession.executemany(query, dados_com_senha)
    print(f"✅ {len(usuarios_data)} usuários com senhas inseridos com sucesso!")
    print(f"   Senha padrão para testes: '{SENHA_PADRAO}'")
    print(f"   📧 Email para login: '{EMAIL_TESTE}'")


if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_usuario_senha(dbsession)
    finally:
        dbsession.close()
