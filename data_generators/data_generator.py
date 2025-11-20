"""
Módulo centralizado para geração de dados sintéticos no banco de dados.

Este módulo unifica todas as formas de popular o banco, usando os scripts Python
existentes nesta pasta como fonte única de verdade.
"""

from pathlib import Path
import sys

# Adiciona o diretório raiz ao path para importar os módulos de geração
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Importa todas as funções de geração
from data_generators.pessoas.g01gerar_pessoas import gerar_pessoas
from data_generators.pessoas.g02gerar_interno_usp import gerar_interno_usp
from data_generators.pessoas.g03gerar_funcionario import gerar_funcionarios
from data_generators.pessoas.g04gerar_atribuicoes import gerar_atribuicoes_funcionario
from data_generators.pessoas.g05gerar_restricao import gerar_restricoes_funcionario
from data_generators.pessoas.g06gerar_educador_fisico import gerar_educadores_fisicos
from data_generators.pessoas.g20gerar_usuario_senha import gerar_usuario_senha
from data_generators.infraestrutura.g07gerar_instalacao import gerar_instalacoes
from data_generators.infraestrutura.g08gerar_equipamento import gerar_equipamentos
from data_generators.infraestrutura.g09gerar_doacao_equipamento import gerar_doacoes
from data_generators.infraestrutura.g10gerar_emprestimo_equipamento import (
    gerar_emprestimo_equipamento,
)
from data_generators.reservas.g10gerar_reservas import gerar_reservas
from data_generators.atividades.g11gerar_atividade import gerar_atividades
from data_generators.atividades.g12gerar_ocorrencia_semanal import popular_ocorrencias
from data_generators.atividades.g13gerar_conduz_atividade import gerar_conduz_atividade
from data_generators.atividades.g14gerar_participacao_atividade import (
    gerar_participacao_atividade,
)
from data_generators.atividades.g21gerar_convite_externo import gerar_convite_externo
from data_generators.eventos.g15gerar_evento import gerar_eventos
from data_generators.eventos.g16gerar_supervisores_eventos import (
    gerar_supervisao_evento,
)
from data_generators.grupos.g17gerar_grupo_extensao import gerar_grupos_extensao
from data_generators.grupos.g18gerar_atividade_grupo_extensao import (
    gerar_atividade_grupo_extensao,
)
from data_generators.reservas.g19gerar_reserva_equipamento import (
    gerar_reservas_equipamento,
)
from data_generators.auth.g23gerar_auditoria_login import gerar_auditoria_login
from data_generators.auth.g24gerar_metrica_acesso_diaria import (
    gerar_metrica_acesso_diaria,
)
from data_generators.auth.g25gerar_solicitacao_cadastro import (
    gerar_solicitacao_cadastro,
)


# Ordem de execução das funções de geração (respeitando dependências)
GENERATION_ORDER = [
    # Domínio: Pessoas
    ("pessoa", gerar_pessoas, {"quantidade": 5000}),
    ("interno_usp", gerar_interno_usp, {}),
    ("usuario_senha", gerar_usuario_senha, {}),
    ("funcionario", gerar_funcionarios, {}),
    ("funcionario_atribuicao", gerar_atribuicoes_funcionario, {}),
    ("funcionario_restricao", gerar_restricoes_funcionario, {}),
    ("educador_fisico", gerar_educadores_fisicos, {}),
    # Domínio: Infraestrutura
    ("instalacao", gerar_instalacoes, {"num_registros": 20}),
    ("equipamento", gerar_equipamentos, {}),
    ("doacao", gerar_doacoes, {}),
    ("emprestimo_equipamento", gerar_emprestimo_equipamento, {}),
    # Domínio: Reservas
    ("reserva", gerar_reservas, {}),
    ("reserva_equipamento", gerar_reservas_equipamento, {}),
    # Domínio: Atividades
    ("atividade", gerar_atividades, {"quantidade": 16}),
    ("ocorrencia_semanal", popular_ocorrencias, {}),
    ("conduz_atividade", gerar_conduz_atividade, {}),
    ("participacao_atividade", gerar_participacao_atividade, {}),
    ("convite_externo", gerar_convite_externo, {}),
    # Domínio: Eventos
    ("evento", gerar_eventos, {}),
    ("supervisao_evento", gerar_supervisao_evento, {}),
    # Domínio: Grupos
    ("grupo_extensao", gerar_grupos_extensao, {"quantidade_grupos": 4}),
    ("atividade_grupo_extensao", gerar_atividade_grupo_extensao, {}),
    # Domínio: Autenticação e Auditoria
    ("auditoria_login", gerar_auditoria_login, {}),
    ("solicitacao_cadastro", gerar_solicitacao_cadastro, {}),
    ("metrica_acesso_diaria", gerar_metrica_acesso_diaria, {}),
]


def populate_database(dbsession):
    """
    Popula o banco de dados com todos os dados sintéticos.

    Args:
        dbsession: Instância de DBSession para executar as operações
    """
    print("=" * 60)
    print("Iniciando população do banco de dados...")
    print("=" * 60)

    for table_name, generator_func, kwargs in GENERATION_ORDER:
        print(f"\n{'=' * 60}")
        print(f"Gerando dados para: {table_name}")
        print(f"{'=' * 60}")
        try:
            generator_func(dbsession, **kwargs)
            print(f"✅ {table_name} concluído.\n")
        except Exception as e:
            print(f"❌ Erro ao gerar {table_name}: {e}")
            raise

    print("\n" + "=" * 60)
    print("✅ Todos os dados foram gerados e inseridos no banco com sucesso!")
    print("=" * 60)
