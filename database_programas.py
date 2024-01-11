import sqlite3

def create_table(database_file):
    """
    Cria a tabela 'programas' no banco de dados.
    """
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Código para criar a tabela
    create_table_query = """
    CREATE TABLE IF NOT EXISTS programas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        security_key TEXT NOT NULL,
        program_type TEXT NOT NULL
    )
    """
    cursor.execute(create_table_query)
    conn.commit()

    conn.close()
