import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date, time

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
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                placeholders = ', '.join(['%s'] * len(params))
                query = f"SELECT * FROM {funcao}({placeholders})"
                cur.execute(query, params)
                return cur.fetchall()
    except Exception as e:
        print(f"Erro ao executar a função {funcao}: {e}")
        return []

# Função para executar procedures
def executar_procedure(procedure, params=()):
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                placeholders = ', '.join(['%s'] * len(params))
                query = f"CALL {procedure}({placeholders})"
                cur.execute(query, params)
                conn.commit()
                print("Procedimento executado com sucesso!")
    except Exception as e:
        print(f"Erro ao executar a procedure {procedure}: {e}")

# Função para validar e converter data e hora
def validar_data_hora(data_input, hora_str):
    """
    Converte e valida a data e a hora.
    data_input: pode ser string 'YYYY-MM-DD' ou datetime.date
    hora_str: string 'HH:MM'
    Retorna: (datetime.date, datetime.time) ou (None, None) em caso de erro
    """
    # Tratar data
    if isinstance(data_input, date):
        data_valida = data_input
    elif isinstance(data_input, str):
        try:
            data_valida = datetime.strptime(data_input, "%Y-%m-%d").date()
        except ValueError:
            print("Erro: Formato de data inválido. Use 'YYYY-MM-DD'.")
            return None, None
    else:
        print("Erro: Tipo de data inválido. Deve ser string ou datetime.date.")
        return None, None

    # Tratar hora
    try:
        hora_valida = datetime.strptime(hora_str, "%H:%M").time()
    except ValueError:
        print("Erro: Formato de hora inválido. Use 'HH:MM'.")
        return None, None

    return data_valida, hora_valida

# Menu interativo
def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Cadastrar evento")
        print("2 - Ver reservas de um interno USP")
        print("3 - Listar instalações disponíveis em determinado dia e horário")
        print("4 - Listar atividades de um educador físico")
        print("5 - Calcular total de acessos ao Cefer em um período")
        print("6 - Listar atividades com filtros")
        print("7 - Inscrever participante em atividade")
        print("0 - Sair")

        opcao = input("Opção: ").strip()

        if opcao == "1":
            nome = input("Nome do evento: ")
            descricao = input("Descrição do evento: ")
            try:
                id_reserva = int(input("ID da reserva: "))
                executar_procedure("cadastrar_evento", (nome, descricao, id_reserva))
            except ValueError:
                print("Erro: O ID da reserva deve ser um número inteiro.")
        
        elif opcao == "2":
            cpf_interno = input("CPF do interno: ").strip()
            resultado = executar_funcao("get_reservas_interno", (cpf_interno,))
            if resultado:
                for row in resultado:
                    print(row)
            else:
                print("Nenhuma reserva encontrada para este CPF.")
        
        elif opcao == "3":
            dia_input = input("Data (YYYY-MM-DD): ").strip()
            hora_inicio_input = input("Hora início (HH:MM): ").strip()
            hora_fim_input = input("Hora fim (HH:MM): ").strip()

            # Validação de data e hora
            dia, hora_inicio = validar_data_hora(dia_input, hora_inicio_input)
            _, hora_fim = validar_data_hora(dia, hora_fim_input)

            if dia and hora_inicio and hora_fim:
                resultado = executar_funcao("get_instalacoes_disponiveis_horario", (dia, hora_inicio, hora_fim))
                if resultado:
                    for row in resultado:
                        print(row)
                else:
                    print("Nenhuma instalação disponível para o horário informado.")
        
        elif opcao == "4":
            cpf_educador = input("CPF do educador físico: ").strip()
            resultado = executar_funcao("get_atividades_educador", (cpf_educador,))
            if resultado:
                for row in resultado:
                    print(row)
            else:
                print("Nenhuma atividade encontrada para este CPF.")
        
        elif opcao == "5":
            try:
                data_inicio = input("Data início (YYYY-MM-DD): ").strip()
                data_fim = input("Data fim (YYYY-MM-DD): ").strip()

                # Validação de data
                data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
                data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()

                resultado = executar_funcao("total_acessos_cefer", (data_inicio, data_fim))
                if resultado:
                    print("Total de acessos ao Cefer:", resultado[0]['total_acessos_cefer'])
            except ValueError:
                print("Erro: Formato de data inválido. Use 'YYYY-MM-DD'.")
        
        elif opcao == "6":
            dia_semana = input("Dia da semana (Opcional, ex: Segunda): ").strip().upper() or None
            grupo_extensao = input("Grupo de Extensão (Opcional): ").strip() or None
            modalidade = input("Modalidade (Opcional): ").strip() or None

            resultado = executar_funcao("listar_atividades", (dia_semana, grupo_extensao, modalidade))
            if resultado:
                for row in resultado:
                    print(row)
            else:
                print("Nenhuma atividade encontrada com os filtros informados.")
        
        elif opcao == "7":
            cpf_participante = input("CPF do participante: ").strip()
            try:
                id_atividade = int(input("ID da atividade: "))
                executar_procedure("inscrever_participante", (cpf_participante, id_atividade))
            except ValueError:
                print("Erro: O ID da atividade deve ser um número inteiro.")
        
        elif opcao == "0":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida, tente novamente.")

# Executar menu
if __name__ == "__main__":
    menu()
