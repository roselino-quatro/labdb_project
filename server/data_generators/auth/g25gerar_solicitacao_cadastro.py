import random
import sys
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

fake = Faker('pt_BR')

# Status possíveis para solicitações
STATUS_SOLICITACAO = ['PENDENTE', 'APROVADA', 'REJEITADA']

def gerar_nusp():
    """Gera um NUSP aleatório (5 a 8 dígitos)."""
    return f"{random.randint(10000, 99999999)}"

def gerar_solicitacao_cadastro(dbsession):
    """
    Gera solicitações de cadastro para pessoas não-internas.
    Status variados: PENDENTE, APROVADA, REJEITADA.
    """
    # Buscar pessoas que não são internas (candidatos a solicitação)
    pessoas_externas_result = dbsession.fetch_all("""
        SELECT CPF, EMAIL
        FROM PESSOA
        WHERE CPF NOT IN (SELECT CPF_PESSOA FROM INTERNO_USP)
        ORDER BY CPF
    """)
    pessoas_externas = [(row['cpf'], row['email']) for row in pessoas_externas_result]

    if not pessoas_externas:
        print("⚠️  Nenhuma pessoa externa encontrada. Pulando geração de solicitações de cadastro.")
        return

    # Buscar funcionários que podem ser aprovadores (admins)
    funcionarios_result = dbsession.fetch_all("""
        SELECT F.CPF_INTERNO
        FROM FUNCIONARIO F
        ORDER BY F.CPF_INTERNO
    """)
    cpfs_admins = [row['cpf_interno'] for row in funcionarios_result]

    # Se não houver funcionários, usar internos como fallback
    if not cpfs_admins:
        internos_result = dbsession.fetch_all("SELECT CPF_PESSOA FROM INTERNO_USP ORDER BY CPF_PESSOA")
        cpfs_admins = [row['cpf_pessoa'] for row in internos_result]

    if not cpfs_admins:
        print("⚠️  Nenhum admin encontrado. Pulando geração de solicitações de cadastro.")
        return

    # Gerar solicitações: 30-50% das pessoas externas fazem solicitação
    percentual_solicitacoes = random.uniform(0.3, 0.5)
    num_solicitacoes = int(len(pessoas_externas) * percentual_solicitacoes)
    pessoas_selecionadas = random.sample(pessoas_externas, min(num_solicitacoes, len(pessoas_externas)))

    solicitacoes_data = []
    nusps_gerados = set()

    # Data base para solicitações (últimos 12 meses)
    data_base = datetime.now() - timedelta(days=365)

    for cpf_pessoa, email in pessoas_selecionadas:
        # Gerar NUSP único
        nusp = gerar_nusp()
        while nusp in nusps_gerados:
            nusp = gerar_nusp()
        nusps_gerados.add(nusp)

        # Status aleatório (mais PENDENTE, menos REJEITADA)
        pesos_status = [0.5, 0.4, 0.1]  # PENDENTE, APROVADA, REJEITADA
        status = random.choices(STATUS_SOLICITACAO, weights=pesos_status)[0]

        # Data da solicitação (últimos 12 meses)
        dias_aleatorios = random.randint(0, 365)
        data_solicitacao = data_base + timedelta(days=dias_aleatorios)

        # Admin aprovador (apenas se APROVADA ou REJEITADA)
        cpf_admin_aprovador = None
        data_aprovacao = None

        if status in ['APROVADA', 'REJEITADA']:
            cpf_admin_aprovador = random.choice(cpfs_admins)
            # Data de aprovação/rejeição (1-30 dias após solicitação)
            # Se dias_aleatorios é 0, a aprovação é no mesmo dia (0 dias)
            if dias_aleatorios == 0:
                dias_aprovacao = 0
            else:
                dias_aprovacao = random.randint(1, min(30, dias_aleatorios))
            data_aprovacao = data_solicitacao + timedelta(days=dias_aprovacao)

        # Observações (40% de chance)
        observacoes = None
        if random.random() < 0.4:
            if status == 'APROVADA':
                observacoes_list = [
                    "Cadastro aprovado após verificação de documentos",
                    "Aprovado conforme regulamento",
                    "Documentação completa e válida"
                ]
            elif status == 'REJEITADA':
                observacoes_list = [
                    "Documentação incompleta",
                    "NUSP inválido",
                    "Cadastro não atende aos requisitos"
                ]
            else:
                observacoes_list = [
                    "Aguardando análise de documentos",
                    "Em processo de verificação",
                    "Pendente de validação"
                ]
            observacoes = random.choice(observacoes_list)

        solicitacoes_data.append((
            cpf_pessoa,
            nusp,
            status,
            cpf_admin_aprovador,
            data_solicitacao,
            data_aprovacao,
            observacoes
        ))

    # Inserir diretamente no banco
    query_com_obs = """
        INSERT INTO SOLICITACAO_CADASTRO (
            CPF_PESSOA,
            NUSP,
            STATUS,
            CPF_ADMIN_APROVADOR,
            DATA_SOLICITACAO,
            DATA_APROVACAO,
            OBSERVACOES
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    query_sem_obs = """
        INSERT INTO SOLICITACAO_CADASTRO (
            CPF_PESSOA,
            NUSP,
            STATUS,
            CPF_ADMIN_APROVADOR,
            DATA_SOLICITACAO,
            DATA_APROVACAO
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    print(f"Inserindo {len(solicitacoes_data)} solicitações de cadastro no banco...")

    # Separar por tipo para executar queries apropriadas
    com_obs = [(c, n, s, a, ds, da, o)
               for c, n, s, a, ds, da, o in solicitacoes_data if o is not None]
    sem_obs = [(c, n, s, a, ds, da)
               for c, n, s, a, ds, da, o in solicitacoes_data if o is None]

    if com_obs:
        dbsession.executemany(query_com_obs, com_obs)
    if sem_obs:
        dbsession.executemany(query_sem_obs, sem_obs)

    print(f"✅ {len(solicitacoes_data)} solicitações de cadastro inseridas com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_solicitacao_cadastro(dbsession)
    finally:
        dbsession.close()
