import sqlite3


class Database:
    def __init__(self, database_file):
        self.database_file = database_file

    def create_table(self):
        """
        Cria a tabela 'users' no banco de dados se ela não existir.
        """
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()

        # Cria a tabela 'users' caso não exista
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)

        conn.commit()
        conn.close()

    def check_user(self, username):
        """
        Verifica se o usuário existe no banco de dados.

        Args:
            username (str): O nome de usuário a ser verificado.

        Returns:
            bool: True se o usuário existe, False caso contrário.
        """
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()

        # Verifica se o usuário existe no banco de dados
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        conn.close()

        return existing_user is not None

    def add_user(self, username, password):
        """
        Adiciona um novo usuário ao banco de dados.

        Args:
            username (str): O nome de usuário do novo usuário.
            password (str): A senha do novo usuário.
        """
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()

        # Verifica se o usuário já existe no banco de dados
        if self.check_user(username):
            print("Usuário já existe.")
            conn.close()
            return

        # Adiciona o novo usuário
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Usuário adicionado com sucesso.")

        conn.close()


def main():
    database_file = "users.db"
    db = Database(database_file)
    db.create_table()

    # Restante do código específico para 'database.py'


if __name__ == "__main__":
    main()
