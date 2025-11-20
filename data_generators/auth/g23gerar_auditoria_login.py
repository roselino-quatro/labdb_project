import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

# Status possíveis para auditoria
STATUS_AUDITORIA = ['SUCCESS', 'FAILURE', 'LOCKED']

def gerar_ip_aleatorio():
    """Gera um IP aleatório para simular origens diferentes."""
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def gerar_mensagem(status, email):
    """Gera mensagem apropriada baseada no status."""
    if status == 'SUCCESS':
        return f"Login bem-sucedido para {email}"
    elif status == 'FAILURE':
        mensagens = [
            f"Senha incorreta para {email}",
            f"Tentativa de login falhou para {email}",
            f"Credenciais inválidas para {email}"
        ]
        return random.choice(mensagens)
    else:  # LOCKED
        return f"Conta bloqueada após múltiplas tentativas falhas para {email}"

def gerar_auditoria_login(dbsession):
    """
    Gera logs históricos de tentativas de login.
    Mistura SUCCESS, FAILURE e LOCKED com timestamps distribuídos.
    """
    # Buscar emails de pessoas existentes
    pessoas_result = dbsession.fetch_all("SELECT EMAIL FROM PESSOA ORDER BY EMAIL")
    emails = [row['email'] for row in pessoas_result]

    if not emails:
        print("⚠️  Nenhuma pessoa encontrada. Pulando geração de auditoria de login.")
        return

    # Buscar emails de pessoas com senha (mais prováveis de ter tentativas de login)
    usuarios_result = dbsession.fetch_all("""
        SELECT P.EMAIL
        FROM PESSOA P
        INNER JOIN USUARIO_SENHA U ON P.CPF = U.CPF_PESSOA
        ORDER BY P.EMAIL
    """)
    emails_com_senha = [row['email'] for row in usuarios_result]

    # Usar 70% de emails com senha e 30% de outros emails
    emails_prioritarios = emails_com_senha if emails_com_senha else emails
    outros_emails = [e for e in emails if e not in emails_com_senha]

    # Gerar logs: 3-10 logs por email com senha, 1-3 por outros emails
    auditoria_data = []

    # Data base para logs (últimos 6 meses)
    data_base = datetime.now() - timedelta(days=180)

    # Logs para emails com senha
    for email in emails_prioritarios:
        num_logs = random.randint(3, 10)

        for _ in range(num_logs):
            # Timestamp aleatório nos últimos 6 meses
            dias_aleatorios = random.randint(0, 180)
            horas_aleatorias = random.randint(0, 23)
            minutos_aleatorios = random.randint(0, 59)
            segundos_aleatorios = random.randint(0, 59)

            timestamp = data_base + timedelta(
                days=dias_aleatorios,
                hours=horas_aleatorias,
                minutes=minutos_aleatorios,
                seconds=segundos_aleatorios
            )

            # Status: mais SUCCESS, menos LOCKED
            pesos_status = [0.7, 0.25, 0.05]  # SUCCESS, FAILURE, LOCKED
            status = random.choices(STATUS_AUDITORIA, weights=pesos_status)[0]

            ip_origem = gerar_ip_aleatorio()
            mensagem = gerar_mensagem(status, email)

            auditoria_data.append((timestamp, email, ip_origem, status, mensagem))

    # Logs para outros emails (menos frequentes)
    for email in random.sample(outros_emails, min(len(outros_emails), len(emails_prioritarios) // 3)):
        num_logs = random.randint(1, 3)

        for _ in range(num_logs):
            dias_aleatorios = random.randint(0, 180)
            horas_aleatorias = random.randint(0, 23)
            minutos_aleatorios = random.randint(0, 59)
            segundos_aleatorios = random.randint(0, 59)

            timestamp = data_base + timedelta(
                days=dias_aleatorios,
                hours=horas_aleatorias,
                minutes=minutos_aleatorios,
                seconds=segundos_aleatorios
            )

            # Para emails sem senha, mais FAILURE
            pesos_status = [0.2, 0.75, 0.05]  # SUCCESS, FAILURE, LOCKED
            status = random.choices(STATUS_AUDITORIA, weights=pesos_status)[0]

            ip_origem = gerar_ip_aleatorio()
            mensagem = gerar_mensagem(status, email)

            auditoria_data.append((timestamp, email, ip_origem, status, mensagem))

    # Ordenar por timestamp para manter ordem cronológica
    auditoria_data.sort(key=lambda x: x[0])

    # Inserir diretamente no banco
    query = """
        INSERT INTO AUDITORIA_LOGIN (
            TIMESTAMP_EVENTO,
            EMAIL_USUARIO,
            IP_ORIGEM,
            STATUS,
            MENSAGEM
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    print(f"Inserindo {len(auditoria_data)} logs de auditoria no banco...")
    dbsession.executemany(query, auditoria_data)
    print(f"✅ {len(auditoria_data)} logs de auditoria inseridos com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_auditoria_login(dbsession)
    finally:
        dbsession.close()
