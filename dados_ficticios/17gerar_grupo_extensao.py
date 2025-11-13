import csv
import random

# Lista fixa de nomes de grupos de extensão
NOMES_GRUPOS_EXTENSAO = [
    'Grupo de Karatê Shotokan', 
    'Equipe Kung Fu Garra de Águia', 
    'Grupo de Estudos Tai Chi Chuan', 
    'Projeto Capoeira Angola'
]

def gerar_grupos_extensao(
    nome_arquivo_internos,
    nome_arquivo_sql,
    nome_arquivo_csv,
    quantidade_grupos=4
):
    """
    Gera dados fictícios para GRUPO_EXTENSAO com base em nomes fixos
    e salva em arquivos SQL e CSV.
    """

    # 1. Ler CPFs dos internos
    cpfs_internos = []
    try:
        with open(nome_arquivo_internos, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Lê o cabeçalho
            try:
                idx_cpf = header.index('CPF')  # Detecta a coluna do CPF
            except ValueError:
                print("Erro: Cabeçalho 'CPF' não encontrado no arquivo de internos.")
                return
            for row in reader:
                if len(row) > idx_cpf:
                    cpfs_internos.append(row[idx_cpf])
        if not cpfs_internos:
            print("Aviso: Nenhum CPF de interno encontrado.")
            return
    except FileNotFoundError:
        print(f"Erro: Arquivo {nome_arquivo_internos} não encontrado.")
        return

    # 2. Definir quantos grupos gerar
    num_a_selecionar = min(quantidade_grupos, len(NOMES_GRUPOS_EXTENSAO))
    if quantidade_grupos > len(NOMES_GRUPOS_EXTENSAO):
        print(f"Aviso: Solicitados {quantidade_grupos} grupos, mas só existem {len(NOMES_GRUPOS_EXTENSAO)} nomes disponíveis.")
    
    nomes_selecionados = random.sample(NOMES_GRUPOS_EXTENSAO, num_a_selecionar)

    # 3. Gerar os dados dos grupos
    grupos = []
    for nome in nomes_selecionados:
        descricao = f"{nome} é um grupo de extensão promovido pelo CEFER."
        cpf_responsavel = random.choice(cpfs_internos)
        grupos.append([nome, descricao, cpf_responsavel])

    # 4. Criar arquivo SQL
    with open(nome_arquivo_sql, mode='w', encoding='utf-8') as sql_file:
        for grupo in grupos:
            nome_sql = grupo[0].replace("'", "''")
            descricao_sql = grupo[1].replace("'", "''")
            cpf = grupo[2]
            insert_sql = (
                f"INSERT INTO GRUPO_EXTENSAO (NOME_GRUPO, DESCRICAO, CPF_RESPONSAVEL_INTERNO) "
                f"VALUES ('{nome_sql}', '{descricao_sql}', '{cpf}');\n"
            )
            sql_file.write(insert_sql)

    # 5. Criar arquivo CSV
    with open(nome_arquivo_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['NOME_GRUPO', 'DESCRICAO', 'CPF_RESPONSAVEL_INTERNO'])
        writer.writerows(grupos)

    # 6. Mensagens de confirmação
    print(f"Arquivo SQL de grupos gerado: {nome_arquivo_sql}")
    print(f"Arquivo CSV de grupos gerado: {nome_arquivo_csv}")
    print(f"Total de grupos gerados: {len(grupos)}")


# Executa o gerador
gerar_grupos_extensao(
    nome_arquivo_internos='pessoas_internas.csv',
    nome_arquivo_sql='upgrade_grupo_extensao.sql',
    nome_arquivo_csv='grupos_extensao.csv',
    quantidade_grupos=4  # Pode ajustar conforme quiser
)
