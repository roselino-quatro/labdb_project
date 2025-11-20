import random
import sys
import secrets
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

fake = Faker('pt_BR')

# Status possíveis para convites
STATUS_CONVITE = ['PENDENTE', 'ACEITO', 'RECUSADO', 'CANCELADO']

def gerar_token():
    """Gera um token único de 64 caracteres hexadecimais."""
    return secrets.token_hex(32)

def gerar_convite_externo(dbsession):
    """
    Gera convites externos para atividades existentes.
    Usa internos como convidantes e gera tokens únicos.
    """
    # Buscar atividades existentes
    atividades_result = dbsession.fetch_all("SELECT ID_ATIVIDADE FROM ATIVIDADE ORDER BY ID_ATIVIDADE")
    ids_atividades = [row['id_atividade'] for row in atividades_result]

    if not ids_atividades:
        print("⚠️  Nenhuma atividade encontrada. Pulando geração de convites externos.")
        return

    # Buscar internos que podem ser convidantes
    internos_result = dbsession.fetch_all("SELECT CPF_PESSOA FROM INTERNO_USP ORDER BY CPF_PESSOA")
    cpfs_internos = [row['cpf_pessoa'] for row in internos_result]

    if not cpfs_internos:
        print("⚠️  Nenhum interno USP encontrado. Pulando geração de convites externos.")
        return

    # Gerar convites: 2-5 convites por atividade
    convites_data = []
    tokens_gerados = set()

    # Data base para convites (últimos 3 meses)
    data_base = datetime.now() - timedelta(days=90)

    for id_atividade in ids_atividades:
        num_convites = random.randint(2, 5)

        for _ in range(num_convites):
            # Gerar token único
            token = gerar_token()
            while token in tokens_gerados:
                token = gerar_token()
            tokens_gerados.add(token)

            # Selecionar convidante interno aleatório
            cpf_convidante = random.choice(cpfs_internos)

            # Gerar dados do convidado externo
            documento_convidade = f"{random.randint(10000000000, 99999999999)}"  # CPF ou RG
            nome_convidade = fake.name()
            email_convidade = fake.email()
            telefone_convidade = f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

            # Status aleatório (mais PENDENTE e ACEITO)
            pesos_status = [0.4, 0.4, 0.1, 0.1]  # PENDENTE, ACEITO, RECUSADO, CANCELADO
            status = random.choices(STATUS_CONVITE, weights=pesos_status)[0]

            # Data do convite (últimos 3 meses)
            dias_aleatorios = random.randint(0, 90)
            data_convite = data_base + timedelta(days=dias_aleatorios)

            # Data de resposta (se não for PENDENTE)
            if status != 'PENDENTE':
                dias_resposta = random.randint(1, min(dias_aleatorios, 30))
                data_resposta = data_convite + timedelta(days=dias_resposta)
            else:
                data_resposta = None

            # Observações (30% de chance)
            observacoes = fake.sentence() if random.random() < 0.3 else None

            convites_data.append((
                cpf_convidante,
                documento_convidade,
                nome_convidade,
                email_convidade,
                telefone_convidade,
                id_atividade,
                status,
                token,
                data_convite,
                data_resposta,
                observacoes
            ))

    # Inserir diretamente no banco
    query_com_obs = """
        INSERT INTO CONVITE_EXTERNO (
            CPF_CONVIDANTE,
            DOCUMENTO_CONVIDADO,
            NOME_CONVIDADO,
            EMAIL_CONVIDADO,
            TELEFONE_CONVIDADO,
            ID_ATIVIDADE,
            STATUS,
            TOKEN,
            DATA_CONVITE,
            DATA_RESPOSTA,
            OBSERVACOES
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    query_sem_obs = """
        INSERT INTO CONVITE_EXTERNO (
            CPF_CONVIDANTE,
            DOCUMENTO_CONVIDADO,
            NOME_CONVIDADO,
            EMAIL_CONVIDADO,
            TELEFONE_CONVIDADO,
            ID_ATIVIDADE,
            STATUS,
            TOKEN,
            DATA_CONVITE,
            DATA_RESPOSTA
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    print(f"Inserindo {len(convites_data)} convites externos no banco...")

    # Separar por tipo para executar queries apropriadas
    com_obs = [(c, d, n, e, t, i, s, tok, dc, dr, o)
               for c, d, n, e, t, i, s, tok, dc, dr, o in convites_data if o is not None]
    sem_obs = [(c, d, n, e, t, i, s, tok, dc, dr)
               for c, d, n, e, t, i, s, tok, dc, dr, o in convites_data if o is None]

    if com_obs:
        dbsession.executemany(query_com_obs, com_obs)
    if sem_obs:
        dbsession.executemany(query_sem_obs, sem_obs)

    print(f"✅ {len(convites_data)} convites externos inseridos com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_convite_externo(dbsession)
    finally:
        dbsession.close()
