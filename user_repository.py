import sqlite3
import logging

class UserRepository:
    def __init__(self, database_file):
        self.database_file = database_file
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        try:
            conn = sqlite3.connect(self.database_file)
            cursor = conn.cursor()

            # Create the 'users' table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL
                              )''')

            conn.commit()

        except sqlite3.Error as error:
            logging.exception(f"Erro ao conectar ao banco de dados: {error}")

        finally:
            conn.close()

    def has_users(self):
        try:
            conn = sqlite3.connect(self.database_file)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]

        except sqlite3.Error as error:
            logging.exception(f"Erro ao conectar ao banco de dados: {error}")
            return False

        finally:
            conn.close()

        return user_count > 0

    def validate_login(self, username, password):
        try:
            conn = sqlite3.connect(self.database_file)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user and user[2] == password:
                return True

        except sqlite3.Error as error:
            logging.exception(f"Erro ao conectar ao banco de dados: {error}")

        finally:
            conn.close()

        return False
