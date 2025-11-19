"""
Ponto de entrada único para popular o banco de dados.

Este script cria o schema e popula o banco com dados sintéticos completos.
"""
from pathlib import Path
from dbsession import DBSession
from data_generators.data_generator import populate_database

def _database_has_data(dbsession):
    """Verifica se o banco já tem dados populados."""
    try:
        result = dbsession.fetch_one('SELECT COUNT(*) as count FROM pessoa;')
        return result and result['count'] > 0
    except Exception:
        return False


def _apply_schema_safe(dbsession):
    """Aplica o schema de forma segura, usando IF NOT EXISTS."""
    schema_file = Path('./sql/upgrade_schema.sql')

    try:
        # Ler o arquivo SQL
        with open(schema_file, 'r', encoding='utf-8') as file:
            query = file.read()

        # Verificar se o tipo DIA_SEMANA já existe antes de criar
        with dbsession.connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM pg_type
                WHERE typname = 'dia_semana'
            """)
            result = cursor.fetchone()
            dia_semana_exists = result and result[0] > 0

        # Modificar o SQL para usar CREATE TABLE IF NOT EXISTS
        modified_query = query.replace('CREATE TABLE ', 'CREATE TABLE IF NOT EXISTS ')

        # Para CREATE TYPE, remover a linha se o tipo já existir
        # PostgreSQL não suporta CREATE TYPE IF NOT EXISTS
        if dia_semana_exists:
            # Remover a criação do tipo DIA_SEMANA se já existir
            lines = modified_query.split('\n')
            new_lines = []
            skip_type_creation = False
            for line in lines:
                if 'CREATE TYPE DIA_SEMANA' in line.upper():
                    skip_type_creation = True
                    continue
                if skip_type_creation:
                    # Continuar pulando até encontrar o fechamento do enum
                    if line.strip() == ');':
                        skip_type_creation = False
                    continue
                new_lines.append(line)
            modified_query = '\n'.join(new_lines)

        # Executar o SQL modificado
        with dbsession.connection.cursor() as cursor:
            cursor.execute(modified_query)
        dbsession.connection.commit()
    except Exception as e:
        # Reverter transação em caso de erro
        dbsession.connection.rollback()
        # Re-raise para que o erro seja tratado pelo chamador
        raise


def populate_db():
    """Cria o schema e popula o banco de dados com dados completos."""
    dbsession = DBSession()

    try:
        # Sempre aplicar o schema de forma segura (usando IF NOT EXISTS)
        # Isso garante que todas as tabelas existam, mesmo se o schema estiver parcialmente criado
        print("=" * 60)
        print("Aplicando schema do banco de dados...")
        print("=" * 60)
        try:
            _apply_schema_safe(dbsession)
            print("✅ Schema aplicado com sucesso!\n")
        except Exception as e:
            # Garantir que a transação foi revertida
            try:
                dbsession.connection.rollback()
            except Exception:
                pass
            # Com IF NOT EXISTS, erros devem ser raros, mas se ocorrerem, vamos continuar
            # pois pode ser que algumas tabelas já existam e outras não
            print(f"⚠️  Aviso ao aplicar schema: {e}")
            print("Continuando mesmo assim (schema pode estar parcialmente criado)...\n")

        # Verificar se dados já existem
        if _database_has_data(dbsession):
            print("\n" + "=" * 60)
            print("Banco de dados já contém dados. Pulando população.")
            print("=" * 60)
            return

        # Popular banco com dados
        print("\n" + "=" * 60)
        print("Iniciando população do banco de dados...")
        print("=" * 60)
        populate_database(dbsession)

    finally:
        dbsession.close()


if __name__ == "__main__":
    populate_db()
