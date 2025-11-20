import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.database import DBSession

def gerar_atividade_grupo_extensao(dbsession):
    """
    Gera associações entre ATIVIDADE e GRUPO_EXTENSAO de forma semântica,
    baseada em palavras-chave (ex: 'karatê', 'kung fu', 'tai chi', 'capoeira').
    """

    print("Gerando vínculos semânticos entre ATIVIDADES e GRUPOS_DE_EXTENSAO...")

    #Definir o mapa semântico (palavras-chave que relacionam atividades e grupos)
    mapa_semantico = {
        "karate": ["karatê", "karate"],
        "kungfu": ["kung fu", "kungfu"],
        "taichi": ["tai chi", "taichi"],
        "capoeira": ["capoeira"],
    }

    #Buscar atividades (ID e Nome) do banco
    atividades_result = dbsession.fetch_all("SELECT ID_ATIVIDADE, NOME FROM ATIVIDADE ORDER BY ID_ATIVIDADE")
    atividades_extensao = {}  # Ex: {"karate": [1, 5, 7], "kungfu": [3]}

    for row in atividades_result:
        id_atividade = row['id_atividade']
        nome_atividade = row['nome'].lower()

        # Verifica se a atividade contém uma das palavras-chave
        for chave, palavras in mapa_semantico.items():
            for palavra in palavras:
                if palavra in nome_atividade:
                    atividades_extensao.setdefault(chave, []).append(id_atividade)
                    break

    if not atividades_extensao:
        print("Aviso: Nenhuma atividade de extensão encontrada (ex: Karatê, Kung Fu, etc.).")
        return

    #Buscar grupos de extensão (Nome) do banco
    grupos_result = dbsession.fetch_all("SELECT NOME_GRUPO FROM GRUPO_EXTENSAO ORDER BY NOME_GRUPO")
    grupos_extensao = {}  # Ex: {"karate": "Grupo de Karatê Shotokan"}

    for row in grupos_result:
        nome_grupo_exato = row['nome_grupo'].strip()
        nome_grupo_lower = nome_grupo_exato.lower()

        for chave, palavras in mapa_semantico.items():
            for palavra in palavras:
                if palavra in nome_grupo_lower:
                    grupos_extensao[chave] = nome_grupo_exato
                    break

    if not grupos_extensao:
        print("Aviso: Nenhum grupo de extensão correspondente encontrado (ex: Karatê, Kung Fu, etc.).")
        return

    #Associar atividades a grupos com base na semântica
    registros_data = []
    print("Mapeando atividades para grupos com base em palavras-chave...")

    for chave in mapa_semantico.keys():
        if chave in atividades_extensao and chave in grupos_extensao:
            ids_ativ = atividades_extensao[chave]
            nome_grupo = grupos_extensao[chave]
            print(f"  - {chave.capitalize()}: {len(ids_ativ)} atividade(s) → grupo '{nome_grupo}'")

            for id_atividade in ids_ativ:
                registros_data.append((id_atividade, nome_grupo))
        else:
            print(f"  - {chave.capitalize()}: sem correspondência encontrada (ignorando).")

    if not registros_data:
        print("Nenhuma correspondência semântica encontrada. Nenhum registro gerado.")
        return

    # Inserir diretamente no banco
    query = """
        INSERT INTO ATIVIDADE_GRUPO_EXTENSAO (ID_ATIVIDADE, NOME_GRUPO)
        VALUES (%s, %s)
    """

    print(f"Inserindo {len(registros_data)} registros no banco...")
    dbsession.executemany(query, registros_data)
    print(f"✅ {len(registros_data)} registros inseridos com sucesso!")
    print(f"Total de vínculos semânticos gerados: {len(registros_data)}")

if __name__ == "__main__":
    dbsession = DBSession()
    try:
        gerar_atividade_grupo_extensao(dbsession)
    finally:
        dbsession.close()
