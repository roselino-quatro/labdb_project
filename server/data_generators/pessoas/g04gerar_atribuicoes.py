import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

# Função para gerar uma atribuição aleatória para o contexto de Educação Física, Esportes e Recreação
def gerar_atribuicao():
    atribuicoes = [
        'Professor de Educação Física',
        'Coordenador de Atividades Esportivas',
        'Treinador de Atletismo',
        'Professor de Natação',
        'Preparador Físico',
        'Instrutor de Musculação',
        'Técnico de Futebol',
        'Técnico de Vôlei',
        'Assistente de Reabilitação Física',
        'Supervisor de Recreação',
        'Nutricionista Esportivo',
        'Psicólogo Esportivo',
        'Fisioterapeuta',
        'Analista de Performance',
        'Gerente de Eventos Esportivos',
        'Administrador de Ginásio',
        'Monitores de Atividades Recreativas',
        'Gestor de Programas Esportivos',
        'Professor de Yoga ou Pilates',
        'Especialista em Medicina Esportiva'
    ]
    return random.choice(atribuicoes)

def gerar_atribuicoes_funcionario(dbsession):
    # Buscar todos os funcionários do banco
    funcionarios_result = dbsession.fetch_all("SELECT CPF_INTERNO FROM FUNCIONARIO ORDER BY CPF_INTERNO")
    cpfs_funcionarios = [row['cpf_interno'] for row in funcionarios_result]

    # Buscar CPFs dos usuários de teste
    pessoa_admin_result = dbsession.fetch_one("SELECT CPF FROM PESSOA WHERE EMAIL = 'admin@usp.br'")
    cpf_admin = pessoa_admin_result['cpf'] if pessoa_admin_result else None

    pessoa_funcionario_result = dbsession.fetch_one("SELECT CPF FROM PESSOA WHERE EMAIL = 'funcionario@usp.br'")
    cpf_funcionario_teste = pessoa_funcionario_result['cpf'] if pessoa_funcionario_result else None

    # Montar os dados para atribuição
    atribuicoes_data = []
    for cpf_funcionario in cpfs_funcionarios:
        # Se for o admin, garantir atribuição de Administrador
        if cpf_admin and cpf_funcionario == cpf_admin:
            atribuicao = 'Administrador'
        # Se for o funcionario de teste, garantir atribuição aleatória (não Administrador)
        elif cpf_funcionario_teste and cpf_funcionario == cpf_funcionario_teste:
            atribuicao = gerar_atribuicao()
        else:
            atribuicao = gerar_atribuicao()
        atribuicoes_data.append((cpf_funcionario, atribuicao))

    # Inserir diretamente no banco
    query = """
        INSERT INTO FUNCIONARIO_ATRIBUICAO (CPF_FUNCIONARIO, ATRIBUICAO)
        VALUES (%s, %s)
    """

    print(f"Inserindo {len(atribuicoes_data)} atribuições no banco...")
    dbsession.executemany(query, atribuicoes_data)
    print(f"✅ {len(atribuicoes_data)} atribuições inseridas com sucesso!")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_atribuicoes_funcionario(dbsession)
    finally:
        dbsession.close()
