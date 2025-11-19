import subprocess
import sys
from pathlib import Path

# Lista de scripts geradores (na ordem de dependência)
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

try:
    # Rodar os scripts de geração
    for script in scripts:
        print(f"\n{'='*60}")
        print(f"Rodando {script}...")
        print(f"{'='*60}")
        subprocess.run([sys.executable, script], check=True, cwd=Path(__file__).parent)
        print(f"✅ {script} concluído.\n")

    print("\n" + "="*60)
    print("✅ Todos os dados foram gerados e inseridos no banco com sucesso!")
    print("="*60)
except Exception as e:
    print(f"\n❌ Erro ao executar scripts: {e}")
    raise
