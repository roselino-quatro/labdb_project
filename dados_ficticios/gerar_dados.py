import subprocess
import sys
import os
import shutil
from pathlib import Path

# Lista de scripts geradores
scripts = [
    "01gerar_pessoas.py",
    "02gerar_interno_usp.py",
    "03gerar_funcionario.py",
    "04gerar_atribuicoes.py",
    "05gerar_restricao.py",
    "06gerar_educador_fisico.py",
    "07gerar_instalacao.py",
    "08gerar_equipamento.py",
    "09gerar_doacao_equipamento.py",
    "10gerar_reservas.py",
    "11gerar_atividade.py",
    "12gerar_ocorrencia_semanal.py",
    "13gerar_conduz_atividade.py",
    "14gerar_participacao_atividade.py",
    "15gerar_evento.py",
    "16gerar_supervisores_eventos.py",
    "17gerar_grupo_extensao.py",
    "18gerar_atividade_grupo_extensao.py"
]

# Caminhos
sql_folder = Path("..") / "sql"
target_folder = sql_folder / "populate_mocked_full_db"

# Garantir que a pasta de destino existe
target_folder.mkdir(parents=True, exist_ok=True)

# Rodar os scripts de geração
for script in scripts:
    print(f"Rodando {script}...")
    subprocess.run([sys.executable, script], check=True)
    print(f"{script} concluído.\n")

# Mover arquivos .sql para a pasta destino
for sql_file in Path(".").glob("*.sql"):
    destino = target_folder / sql_file.name
    print(f"Movendo {sql_file} → {destino}")
    shutil.move(str(sql_file), destino)

print("\nTodos os arquivos SQL foram movidos para:", target_folder)
