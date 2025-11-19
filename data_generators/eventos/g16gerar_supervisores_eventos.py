import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from dbsession import DBSession

def gerar_supervisao_evento(dbsession):
    # Buscar os funcionários do banco
    funcionarios_result = dbsession.fetch_all("SELECT CPF_INTERNO FROM FUNCIONARIO ORDER BY CPF_INTERNO")
    funcionarios = [row['cpf_interno'] for row in funcionarios_result]

    # Buscar eventos do banco
    eventos_result = dbsession.fetch_all("SELECT ID_EVENTO FROM EVENTO ORDER BY ID_EVENTO")
    ids_eventos = [row['id_evento'] for row in eventos_result] if eventos_result else []

    if not ids_eventos:
        print("Aviso: Nenhum evento encontrado no banco.")
        return

    total_eventos = len(ids_eventos)

    # Selecionar 80% dos eventos para serem supervisionados
    eventos_supervisionados = random.sample(ids_eventos, int(total_eventos * 0.8))

    supervisoes_data = []

    for id_evento in eventos_supervisionados:
        # Cada evento tem entre 1 e 3 supervisores
        qtd_supervisores = random.randint(1, 3)
        supervisores = random.sample(funcionarios, min(qtd_supervisores, len(funcionarios)))

        for cpf_funcionario in supervisores:
            supervisoes_data.append((cpf_funcionario, id_evento))

    # Inserir diretamente no banco
    query = """
        INSERT INTO SUPERVISAO_EVENTO (CPF_FUNCIONARIO, ID_EVENTO)
        VALUES (%s, %s)
    """

    print(f"Inserindo {len(supervisoes_data)} supervisões no banco...")
    dbsession.executemany(query, supervisoes_data)
    print(f"✅ {len(supervisoes_data)} supervisões inseridas com sucesso!")
    print(f"Total de eventos: {total_eventos}")
    print(f"Total de eventos supervisionados: {len(eventos_supervisionados)} ({len(eventos_supervisionados)/total_eventos:.0%})")
    print(f"Total de linhas geradas (supervisões): {len(supervisoes_data)}")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_supervisao_evento(dbsession)
    finally:
        dbsession.close()
