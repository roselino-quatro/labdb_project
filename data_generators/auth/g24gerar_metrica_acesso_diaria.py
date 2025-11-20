import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

def gerar_metrica_acesso_diaria(dbsession):
    """
    Gera métricas diárias de acesso para os últimos 6 meses.
    Calcula totais baseados em dados existentes de internos, externos e funcionários.
    """
    # Buscar totais reais do banco
    total_internos_result = dbsession.fetch_one("SELECT COUNT(*) as total FROM INTERNO_USP")
    total_internos_real = total_internos_result['total'] if total_internos_result else 0

    total_externos_result = dbsession.fetch_one("""
        SELECT COUNT(*) as total
        FROM PESSOA
        WHERE CPF NOT IN (SELECT CPF_PESSOA FROM INTERNO_USP)
    """)
    total_externos_real = total_externos_result['total'] if total_externos_result else 0

    total_funcionarios_result = dbsession.fetch_one("SELECT COUNT(*) as total FROM FUNCIONARIO")
    total_funcionarios_real = total_funcionarios_result['total'] if total_funcionarios_result else 0

    if total_internos_real == 0:
        print("⚠️  Nenhum dado de pessoas encontrado. Pulando geração de métricas de acesso.")
        return

    # Gerar métricas para os últimos 6 meses (180 dias)
    metricas_data = []
    data_base = datetime.now().date() - timedelta(days=180)

    for i in range(180):
        data_referencia = data_base + timedelta(days=i)

        # Calcular acessos baseados em totais reais com variação aleatória
        # Variação de 10% a 100% dos totais (simulando que nem todos acessam diariamente)

        # Internos: 20-80% acessam diariamente
        percentual_internos = random.uniform(0.2, 0.8)
        total_internos = max(0, int(total_internos_real * percentual_internos))

        # Externos: 5-30% acessam diariamente (menos frequente)
        percentual_externos = random.uniform(0.05, 0.3)
        total_externos = max(0, int(total_externos_real * percentual_externos))

        # Funcionários: 40-90% acessam diariamente (mais frequente)
        percentual_funcionarios = random.uniform(0.4, 0.9)
        total_funcionarios = max(0, int(total_funcionarios_real * percentual_funcionarios))

        # Ajustar para fins de semana (menos acessos)
        if data_referencia.weekday() >= 5:  # Sábado ou Domingo
            total_internos = int(total_internos * 0.3)
            total_externos = int(total_externos * 0.2)
            total_funcionarios = int(total_funcionarios * 0.1)

        metricas_data.append((
            data_referencia,
            total_internos,
            total_externos,
            total_funcionarios
        ))

    # Inserir diretamente no banco
    query = """
        INSERT INTO METRICA_ACESSO_DIARIA (
            DATA_REFERENCIA,
            TOTAL_INTERNOS,
            TOTAL_EXTERNOS,
            TOTAL_FUNCIONARIOS
        )
        VALUES (%s, %s, %s, %s)
    """

    print(f"Inserindo {len(metricas_data)} métricas de acesso diárias no banco...")
    dbsession.executemany(query, metricas_data)
    print(f"✅ {len(metricas_data)} métricas de acesso diárias inseridas com sucesso!")
    print(f"   Período: {data_base} até {datetime.now().date()}")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_metrica_acesso_diaria(dbsession)
    finally:
        dbsession.close()
