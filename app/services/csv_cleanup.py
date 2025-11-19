"""Utilitário para limpeza de arquivos CSV após população do banco."""
from pathlib import Path


def delete_csv_files(csv_folder: Path) -> None:
    """Remove todos os arquivos CSV da pasta especificada.

    Args:
        csv_folder: Caminho para a pasta contendo os arquivos CSV.
    """
    csv_files = list(csv_folder.glob("*.csv"))
    if not csv_files:
        print("Nenhum arquivo CSV encontrado para remover.")
        return

    print(f"Removendo {len(csv_files)} arquivo(s) CSV...")
    for csv_file in csv_files:
        try:
            csv_file.unlink()
            print(f"Removido: {csv_file.name}")
        except Exception as e:
            print(f"Erro ao remover {csv_file.name}: {e}")
    print("Todos os arquivos CSV foram removidos com sucesso.\n")
