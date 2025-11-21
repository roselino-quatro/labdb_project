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
    Gera um log de login bem-sucedido para o usuário admin de teste.
    """
    EMAIL_ADMIN = "admin@usp.br"

    # Verificar se o usuário admin de teste existe
    pessoa_admin_result = dbsession.fetch_one(f"""
        SELECT P.EMAIL
        FROM PESSOA P
        WHERE P.EMAIL = '{EMAIL_ADMIN}'
    """)

    if not pessoa_admin_result:
        print("⚠️  Usuário admin de teste não encontrado. Pulando geração de auditoria de login.")
        return

    # Criar apenas um log de login bem-sucedido para o usuário admin de teste
    timestamp = datetime.now() - timedelta(hours=1)  # Login há 1 hora
    status = 'SUCCESS'
    ip_origem = gerar_ip_aleatorio()
    mensagem = gerar_mensagem(status, EMAIL_ADMIN)

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

    auditoria_data = [(timestamp, EMAIL_ADMIN, ip_origem, status, mensagem)]

    print(f"Inserindo 1 log de auditoria de login para {EMAIL_ADMIN}...")
    dbsession.executemany(query, auditoria_data)
    print(f"✅ 1 log de auditoria de login inserido com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_auditoria_login(dbsession)
    finally:
        dbsession.close()
