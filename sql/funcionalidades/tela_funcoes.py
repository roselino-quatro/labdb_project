import psycopg2
from psycopg2.extras import RealDictCursor

# Configuração de conexão
DB_CONFIG = {
    "dbname": "public",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

# Função para executar funções que retornam tabelas
def executar_funcao(funcao, params=()):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            placeholders = ', '.join(['%s'] * len(params))
            query = f"SELECT * FROM {funcao}({placeholders})"
            cur.execute(query, params)
            return cur.fetchall()

# Função para executar procedures
def executar_procedure(procedure, params=()):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            placeholders = ', '.join(['%s'] * len(params))
            query = f"CALL {procedure}({placeholders})"
            cur.execute(query, params)
            conn.commit()
            print("Procedimento executado com sucesso!")

# Menu interativo
def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Verificar capacidade de instalação")
        print("2 - Cadastrar evento")
        print("3 - Ver reservas de um interno USP")
        print("4 - Listar instalações disponíveis em determinado dia e horário")
        print("5 - Listar atividades de um educador físico")
        print("0 - Sair")

        opcao = input("Opção: ").strip()

        if opcao == "1":
            id_instalacao = int(input("ID da instalação: "))
            resultado = executar_funcao("verificar_capacidade_instalacao", (id_instalacao,))
            print("Capacidade disponível:", resultado[0]['verificar_capacidade_instalacao'])
        elif opcao == "2":
            nome = input("Nome do evento: ")
            descricao = input("Descrição do evento: ")
            id_reserva = int(input("ID da reserva: "))
            executar_procedure("cadastrar_evento", (nome, descricao, id_reserva))
        elif opcao == "3":
            cpf_interno = input("CPF do interno: ")
            resultado = executar_funcao("get_reservas_interno", (cpf_interno,))
            for row in resultado:
                print(row)
        elif opcao == "4":
            dia = input("Data (YYYY-MM-DD): ")
            hora_inicio = input("Hora início (HH:MM): ")
            hora_fim = input("Hora fim (HH:MM): ")
            resultado = executar_funcao("get_instalacoes_disponiveis_horario", (dia, hora_inicio, hora_fim))
            for row in resultado:
                print(row)
        elif opcao == "5":
            cpf_educador = input("CPF do educador físico: ")
            resultado = executar_funcao("get_atividades_educador", (cpf_educador,))
            for row in resultado:
                print(row)
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

# Executar menu
if __name__ == "__main__":
    menu()
