import os
import glob

def apagar_arquivos_sql_csv(pasta='.'):
    arquivos = glob.glob(os.path.join(pasta, '*.sql')) + glob.glob(os.path.join(pasta, '*.csv'))
    for arquivo in arquivos:
        os.remove(arquivo)
        print(f"Apagado: {arquivo}")
    print("\nTodos os arquivos .sql e .csv foram removidos da pasta dados_ficticios.\n")

import os
import glob
from pathlib import Path

def apagar_upgrades_mocked_full():
    """
    Remove apenas os arquivos SQL que começam com 'upgrade' dentro da pasta:
    ../sql/populate_mocked_full_db
    """
    # Caminho para a pasta de destino
    pasta_mocked_full = Path("..") / "sql" / "populate_mocked_full_db"

    if not pasta_mocked_full.exists():
        print(f"Pasta não encontrada: {pasta_mocked_full}")
        return

    # Buscar apenas os arquivos .sql que começam com 'upgrade'
    arquivos_upgrade_sql = glob.glob(str(pasta_mocked_full / "upgrade_*.sql"))

    if not arquivos_upgrade_sql:
        print("Nenhum arquivo upgrade_*.sql encontrado para exclusão.")
        return

    # Remover cada arquivo encontrado
    for arquivo in arquivos_upgrade_sql:
        try:
            os.remove(arquivo)
            print(f"Apagado: {arquivo}")
        except Exception as e:
            print(f"Erro ao apagar {arquivo}: {e}")

    print(f"\nTotal de arquivos apagados: {len(arquivos_upgrade_sql)}")
    print("Todos os arquivos upgrade_*.sql foram removidos da pasta mocked_full.\n")

apagar_upgrades_mocked_full()
apagar_arquivos_sql_csv('.')
