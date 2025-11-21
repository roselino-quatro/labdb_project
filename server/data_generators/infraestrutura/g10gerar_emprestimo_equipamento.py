import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

# Status possíveis para empréstimos
STATUS_EMPRESTIMO = ['EM_PREPARACAO', 'RETIRADO', 'DEVOLVIDO', 'CANCELADO']

def gerar_emprestimo_equipamento(dbsession):
    """
    Gera empréstimos de equipamentos reserváveis.
    Usa internos como responsáveis e inclui datas de devolução.
    """
    # Buscar equipamentos reserváveis
    equipamentos_result = dbsession.fetch_all("""
        SELECT ID_PATRIMONIO
        FROM EQUIPAMENTO
        WHERE EH_RESERVAVEL = 'S'
        ORDER BY ID_PATRIMONIO
    """)
    ids_equipamentos = [row['id_patrimonio'] for row in equipamentos_result]

    if not ids_equipamentos:
        print("⚠️  Nenhum equipamento reservável encontrado. Pulando geração de empréstimos.")
        return

    # Buscar internos que podem ser responsáveis
    internos_result = dbsession.fetch_all("SELECT CPF_PESSOA FROM INTERNO_USP ORDER BY CPF_PESSOA")
    cpfs_internos = [row['cpf_pessoa'] for row in internos_result]

    if not cpfs_internos:
        print("⚠️  Nenhum interno USP encontrado. Pulando geração de empréstimos.")
        return

    # Gerar empréstimos: 1-3 empréstimos por equipamento
    emprestimos_data = []

    # Data base para empréstimos (últimos 6 meses)
    data_base = datetime.now() - timedelta(days=180)

    for id_equipamento in ids_equipamentos:
        num_emprestimos = random.randint(1, 3)

        for _ in range(num_emprestimos):
            # Selecionar responsável interno aleatório
            cpf_responsavel = random.choice(cpfs_internos)

            # Quantidade (1-5 itens)
            quantidade = random.randint(1, 5)

            # Data do empréstimo (últimos 6 meses)
            dias_aleatorios = random.randint(0, 180)
            data_emprestimo = data_base + timedelta(days=dias_aleatorios)

            # Status aleatório (mais RETIRADO e DEVOLVIDO)
            pesos_status = [0.1, 0.3, 0.5, 0.1]  # EM_PREPARACAO, RETIRADO, DEVOLVIDO, CANCELADO
            status = random.choices(STATUS_EMPRESTIMO, weights=pesos_status)[0]

            # Data de devolução prevista (1-30 dias após empréstimo)
            dias_devolucao = random.randint(1, 30)
            data_devolucao_prevista = data_emprestimo + timedelta(days=dias_devolucao)

            # Data de devolução real (se DEVOLVIDO)
            if status == 'DEVOLVIDO':
                # Devolução pode ser antes ou depois da prevista
                dias_variacao = random.randint(-5, 10)
                data_devolucao_real = data_devolucao_prevista + timedelta(days=dias_variacao)
                # Garantir que não seja antes do empréstimo
                if data_devolucao_real < data_emprestimo:
                    data_devolucao_real = data_emprestimo + timedelta(days=1)
            else:
                data_devolucao_real = None

            # Observações (20% de chance)
            observacoes = None
            if random.random() < 0.2:
                observacoes_list = [
                    "Equipamento em bom estado",
                    "Necessita manutenção",
                    "Devolvido com atraso",
                    "Equipamento danificado",
                    "Devolvido antes do prazo"
                ]
                observacoes = random.choice(observacoes_list)

            emprestimos_data.append((
                id_equipamento,
                cpf_responsavel,
                quantidade,
                data_emprestimo,
                data_devolucao_prevista,
                data_devolucao_real,
                status,
                observacoes
            ))

    # Inserir diretamente no banco
    query_com_obs = """
        INSERT INTO EMPRESTIMO_EQUIPAMENTO (
            ID_EQUIPAMENTO,
            CPF_RESPONSAVEL_INTERNO,
            QUANTIDADE,
            DATA_EMPRESTIMO,
            DATA_DEVOLUCAO_PREVISTA,
            DATA_DEVOLUCAO_REAL,
            STATUS,
            OBSERVACOES
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    query_sem_obs = """
        INSERT INTO EMPRESTIMO_EQUIPAMENTO (
            ID_EQUIPAMENTO,
            CPF_RESPONSAVEL_INTERNO,
            QUANTIDADE,
            DATA_EMPRESTIMO,
            DATA_DEVOLUCAO_PREVISTA,
            DATA_DEVOLUCAO_REAL,
            STATUS
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    print(f"Inserindo {len(emprestimos_data)} empréstimos de equipamentos no banco...")

    # Separar por tipo para executar queries apropriadas
    com_obs = [(e, c, q, de, dp, dr, s, o)
               for e, c, q, de, dp, dr, s, o in emprestimos_data if o is not None]
    sem_obs = [(e, c, q, de, dp, dr, s)
               for e, c, q, de, dp, dr, s, o in emprestimos_data if o is None]

    if com_obs:
        dbsession.executemany(query_com_obs, com_obs)
    if sem_obs:
        dbsession.executemany(query_sem_obs, sem_obs)

    print(f"✅ {len(emprestimos_data)} empréstimos de equipamentos inseridos com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_emprestimo_equipamento(dbsession)
    finally:
        dbsession.close()
