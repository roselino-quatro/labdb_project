import csv
import random
import re

def gerar_atividade_grupo_extensao(
    nome_arquivo_atividades,
    nome_arquivo_grupos,
    nome_arquivo_sql,
    nome_arquivo_csv
):
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

    #Ler atividades (ID e Nome)
    atividades_extensao = {}  # Ex: {"karate": [1, 5, 7], "kungfu": [3]}
    try:
        with open(nome_arquivo_atividades, 'r', encoding='utf-8') as f_ativ:
            reader = csv.reader(f_ativ)
            header = next(reader)
            try:
                idx_id_ativ = header.index('ID_ATIVIDADE')
                idx_nome_ativ = header.index('NOME')
            except ValueError:
                print("Erro: Cabeçalhos 'ID_ATIVIDADE' ou 'NOME' não encontrados no CSV de atividades.")
                return

            for i, row in enumerate(reader):
                try:
                    id_ativ_str = row[idx_id_ativ].strip()
                    id_atividade = int(id_ativ_str) if id_ativ_str else i + 1
                    nome_atividade = row[idx_nome_ativ].lower()

                    # Verifica se a atividade contém uma das palavras-chave
                    for chave, palavras in mapa_semantico.items():
                        for palavra in palavras:
                            if palavra in nome_atividade:
                                atividades_extensao.setdefault(chave, []).append(id_atividade)
                                break
                except (IndexError, ValueError):
                    continue

        if not atividades_extensao:
            print("Aviso: Nenhuma atividade de extensão encontrada (ex: Karatê, Kung Fu, etc.).")
            return

    except FileNotFoundError:
        print(f"Erro: Arquivo de atividades '{nome_arquivo_atividades}' não encontrado.")
        return

    #Ler grupos de extensão (Nome)
    grupos_extensao = {}  # Ex: {"karate": "Grupo de Karatê Shotokan"}
    try:
        with open(nome_arquivo_grupos, 'r', encoding='utf-8') as f_grupos:
            reader = csv.reader(f_grupos)
            header = next(reader)
            try:
                idx_nome_grupo = header.index('NOME_GRUPO')
            except ValueError:
                print("Erro: Cabeçalho 'NOME_GRUPO' não encontrado no CSV de grupos.")
                return

            for row in reader:
                if not row or len(row) <= idx_nome_grupo:
                    continue
                nome_grupo_exato = row[idx_nome_grupo].strip()
                nome_grupo_lower = nome_grupo_exato.lower()

                for chave, palavras in mapa_semantico.items():
                    for palavra in palavras:
                        if palavra in nome_grupo_lower:
                            grupos_extensao[chave] = nome_grupo_exato
                            break

        if not grupos_extensao:
            print("Aviso: Nenhum grupo de extensão correspondente encontrado (ex: Karatê, Kung Fu, etc.).")
            return

    except FileNotFoundError:
        print(f"Erro: Arquivo de grupos '{nome_arquivo_grupos}' não encontrado.")
        return

    #Associar atividades a grupos com base na semântica
    registros = []
    print("Mapeando atividades para grupos com base em palavras-chave...")

    for chave in mapa_semantico.keys():
        if chave in atividades_extensao and chave in grupos_extensao:
            ids_ativ = atividades_extensao[chave]
            nome_grupo = grupos_extensao[chave]
            print(f"  - {chave.capitalize()}: {len(ids_ativ)} atividade(s) → grupo '{nome_grupo}'")

            for id_atividade in ids_ativ:
                registros.append([id_atividade, nome_grupo])
        else:
            print(f"  - {chave.capitalize()}: sem correspondência encontrada (ignorando).")

    if not registros:
        print("Nenhuma correspondência semântica encontrada. Nenhum registro gerado.")
        return

    #Criar arquivo SQL
    with open(nome_arquivo_sql, 'w', encoding='utf-8') as sql_file:
        for id_atividade, nome_grupo in registros:
            nome_sql = nome_grupo.replace("'", "''")
            sql_file.write(
                f"INSERT INTO ATIVIDADE_GRUPO_EXTENSAO (ID_ATIVIDADE, NOME_GRUPO) "
                f"VALUES ({id_atividade}, '{nome_sql}');\n"
            )

    #Criar arquivo CSV
    with open(nome_arquivo_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_ATIVIDADE', 'NOME_GRUPO'])
        writer.writerows(registros)

    #Exibir resumo
    print(f"\nArquivo SQL gerado: {nome_arquivo_sql}")
    print(f"Arquivo CSV gerado: {nome_arquivo_csv}")
    print(f"Total de vínculos semânticos gerados: {len(registros)}")


# Executa o gerador
gerar_atividade_grupo_extensao(
    nome_arquivo_atividades='atividades.csv',
    nome_arquivo_grupos='grupos_extensao.csv',
    nome_arquivo_sql='upgrade_atividade_grupo_extensao.sql',
    nome_arquivo_csv='atividade_grupo_extensao.csv'
)
