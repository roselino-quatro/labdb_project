import psycopg2
from tabulate import tabulate

# Configurações da conexão ao banco de dados
DB_CONFIG = {
    "dbname": "public",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

# Dicionário com os relatórios SQL
RELATORIOS = {
    1: {
        "descricao": "ROLLUP: Reservas por instalação e mês",
        "sql": """
            SELECT 
                i.nome AS nome_instalacao,
                EXTRACT(MONTH FROM r.data_reserva) AS mes,
                COUNT(*) AS total_reservas
            FROM reserva r
            JOIN instalacao i ON i.id_instalacao = r.id_instalacao
            GROUP BY ROLLUP (i.nome, EXTRACT(MONTH FROM r.data_reserva))
            ORDER BY i.nome, mes;
        """
    },
    2: {
        "descricao": "CUBE: Atividades conduzidas por educador e categoria",
        "sql": """
            SELECT 
                e.numero_conselho,
                iu.categoria,
                COUNT(a.id_atividade) AS total_atividades
            FROM conduz_atividade ca
            JOIN educador_fisico e ON ca.cpf_educador_fisico = e.cpf_funcionario
            JOIN funcionario f ON f.cpf_interno = e.cpf_funcionario
            JOIN interno_usp iu ON iu.cpf_pessoa = f.cpf_interno
            JOIN atividade a ON a.id_atividade = ca.id_atividade
            GROUP BY CUBE (e.numero_conselho, iu.categoria)
            ORDER BY e.numero_conselho, iu.categoria;
        """
    },
    3: {
        "descricao": "GROUPING SETS: Total de participantes por atividade",
        "sql": """
            SELECT 
                a.nome AS atividade,
                COUNT(pa.cpf_participante) AS total_participantes
            FROM participacao_atividade pa
            JOIN atividade a ON a.id_atividade = pa.id_atividade
            GROUP BY GROUPING SETS ((a.nome), ());
        """
    },
    4: {
        "descricao": "WINDOW FUNCTION: Ranking de instalações mais reservadas",
        "sql": """
            SELECT 
                i.nome,
                COUNT(r.id_reserva) AS total_reservas,
                RANK() OVER (ORDER BY COUNT(r.id_reserva) DESC) AS posicao
            FROM reserva r
            JOIN instalacao i ON i.id_instalacao = r.id_instalacao
            GROUP BY i.nome;
        """
    }
}

def executar_relatorio(opcao):
    relatorio = RELATORIOS.get(opcao)
    if not relatorio:
        print("Opção inválida.")
        return

    print(f"\nExecutando: {relatorio['descricao']}\n")

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(relatorio["sql"])
        resultados = cur.fetchall()
        colunas = [desc[0] for desc in cur.description]
        print(tabulate(resultados, headers=colunas, tablefmt="psql"))
        cur.close()
        conn.close()
    except Exception as e:
        print("Erro ao executar consulta:", e)

def menu():
    while True:
        print("\n=== MENU DE RELATÓRIOS ===")
        for num, rel in RELATORIOS.items():
            print(f"{num} - {rel['descricao']}")
        print("0 - Sair")

        try:
            opcao = int(input("\nEscolha uma opção: "))
        except ValueError:
            print("Digite um número válido.")
            continue

        if opcao == 0:
            print("Encerrando...")
            break

        executar_relatorio(opcao)

if __name__ == "__main__":
    menu()
