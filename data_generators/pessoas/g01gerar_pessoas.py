from faker import Faker
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession


# Função para gerar CPF válido
def gerar_cpf():
    def calcular_dv(cpf_base):
        cpf_base = [int(d) for d in cpf_base]
        for i in range(2):
            peso = list(range(10 - i, 1, -1)) if i == 0 else list(range(11 - i, 1, -1))
            soma = sum([cpf_base[j] * peso[j] for j in range(len(peso))])
            resto = soma % 11
            digito = 0 if resto < 2 else 11 - resto
            cpf_base.append(digito)
        return "".join(map(str, cpf_base))

    while True:
        cpf_base = [str(random.randint(0, 9)) for _ in range(9)]
        cpf = calcular_dv(cpf_base)
        if cpf[0] != "0":  # opcional, evitar CPF começando com 0
            return cpf


# Inicializa Faker
fake = Faker("pt_BR")

# Email fixo para login de testes
EMAIL_TESTE = "teste@usp.br"


def gerar_pessoas(dbsession, quantidade):
    cpfs_gerados = set()  # Garante CPFs únicos
    emails_usados = set()  # Garante emails únicos

    pessoas_data = []

    print(f"Gerando {quantidade} pessoas...")

    # Primeira pessoa sempre terá o email fixo para testes
    primeiro_cpf = gerar_cpf()
    while primeiro_cpf in cpfs_gerados:
        primeiro_cpf = gerar_cpf()
    cpfs_gerados.add(primeiro_cpf)

    primeiro_nome = "Usuário Teste"
    primeiro_celular = (
        f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    )
    primeiro_data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80)

    pessoas_data.append(
        (
            primeiro_cpf,
            primeiro_nome,
            EMAIL_TESTE,
            primeiro_celular,
            primeiro_data_nascimento,
        )
    )
    emails_usados.add(EMAIL_TESTE)

    print(f"   📧 Email fixo para login: {EMAIL_TESTE} (CPF: {primeiro_cpf})")

    for i in range(1, quantidade):
        # Gera CPF único
        cpf = gerar_cpf()
        while cpf in cpfs_gerados:
            cpf = gerar_cpf()
        cpfs_gerados.add(cpf)

        nome = fake.name()

        # Gera email único
        email = fake.email()
        while email in emails_usados:
            email = fake.email()
        emails_usados.add(email)

        celular = f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80)

        pessoas_data.append((cpf, nome, email, celular, data_nascimento))

    # Inserir diretamente no banco usando executemany
    query = """
        INSERT INTO PESSOA (CPF, NOME, EMAIL, CELULAR, DATA_NASCIMENTO)
        VALUES (%s, %s, %s, %s, %s)
    """

    print(f"Inserindo {len(pessoas_data)} pessoas no banco...")
    dbsession.executemany(query, pessoas_data)
    print(f"✅ {len(pessoas_data)} pessoas inseridas com sucesso!")


if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_pessoas(dbsession, 10000)
    finally:
        dbsession.close()
