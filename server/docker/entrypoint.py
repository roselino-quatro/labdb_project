#!/usr/bin/env python3
"""
Docker entrypoint script para inicializar a aplicação Flask.
Aguarda o PostgreSQL estar pronto e opcionalmente popula o banco de dados.
"""
import os
import sys
import time
import subprocess
from pathlib import Path

# Adiciona /app ao PYTHONPATH se não estiver presente
# Garante que imports funcionem (app e data_generators estão em /app)
app_dir = Path("/app")
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

def wait_for_postgres(max_attempts=30):
    """Aguarda o PostgreSQL estar pronto para conexões."""
    print("Aguardando PostgreSQL estar pronto...")

    for attempt in range(max_attempts):
        try:
            from app.database import DBSession
            dbsession = DBSession()
            dbsession.close()
            print("PostgreSQL está pronto!")
            return True
        except Exception as e:
            attempt_num = attempt + 1
            if attempt_num < max_attempts:
                print(f"Aguardando PostgreSQL... (tentativa {attempt_num}/{max_attempts})")
                time.sleep(2)
            else:
                print(f"ERRO: Não foi possível conectar ao PostgreSQL após {max_attempts} tentativas")
                return False

    return False

def check_db_populated():
    """Verifica se o banco de dados já foi populado."""
    try:
        from data_generators.check_populated import is_db_populated
        return is_db_populated()
    except Exception as e:
        print(f"Erro ao verificar banco: {e}")
        print("Assumindo que banco não está populado.")
        return False

def populate_database():
    """Popula o banco de dados com dados sintéticos usando o sistema unificado."""
    print("=== Iniciando população do banco de dados ===")

    try:
        from data_generators.populate import populate_db
        populate_db()
        print("=== População do banco concluída com sucesso! ===")
        return True
    except Exception as e:
        print(f"ERRO: Falha ao popular banco de dados: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal do entrypoint."""
    print("=== Docker Entrypoint iniciado ===")

    # Aguardar PostgreSQL estar pronto
    if not wait_for_postgres():
        sys.exit(1)

    # Verificar se deve popular o banco
    should_populate = os.environ.get("POPULATE_DB", "false").lower() == "true"

    if should_populate:
        print("=== Verificando se banco precisa ser populado ===")

        if check_db_populated():
            print("Banco de dados já está populado. Pulando população.")
        else:
            if not populate_database():
                print("ERRO: Falha ao popular banco de dados!")
                sys.exit(1)
    else:
        print("POPULATE_DB não está definido como 'true'. Pulando população do banco.")

    # Iniciar a aplicação Flask
    print("=== Iniciando aplicação Flask ===")

    # Executar Flask
    os.execvp("flask", ["flask", "run", "--host=0.0.0.0", "--port=5050"])

if __name__ == "__main__":
    main()
