import sqlite3


def create_connection(database_file):
    """Cria uma conexão com o banco de dados SQLite"""
    try:
        connection = sqlite3.connect(database_file)
        return connection
    except sqlite3.Error as e:
        print(f"Erro ao conectar-se ao banco de dados: {e}")
        return None


class User:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password


class Database:
    def __init__(self, connection=None):
        self.connection = connection
        if self.connection:
            self.create_table()

    def create_table(self):
        if not self.connection:
            raise ValueError("Conexão com o banco de dados não fornecida.")

        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)"
        )
        self.connection.commit()

    def check_user(self, username):
        if not self.connection:
            raise ValueError("Conexão com o banco de dados não fornecida.")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        return existing_user is not None

    def add_user(self, username, password):
        if not self.connection:
            raise ValueError("Conexão com o banco de dados não fornecida.")

        cursor = self.connection.cursor()

        if self.check_user(username):
            return False

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.connection.commit()
        return True

    def remove_user(self, username):
        if not self.connection:
            raise ValueError("Conexão com o banco de dados não fornecida.")

        cursor = self.connection.cursor()

        if not self.check_user(username):
            return False

        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        self.connection.commit()
        return True

    def update_user_password(self, username, new_password):
        if not self.connection:
            raise ValueError("Conexão com o banco de dados não fornecida.")

        cursor = self.connection.cursor()

        if not self.check_user(username):
            return False

        cursor.execute(
            "UPDATE users SET password=? WHERE username=?", (new_password, username))
        self.connection.commit()
        return True

    def get_user_by_username(self, username):
        if not self.connection:
            raise ValueError("Conexão com o banco de dados não fornecida.")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()

        if user_data:
            user = User(*user_data)
            return user

        return None

    def get_all_users(self):
        if not self.connection:
            raise ValueError("Conexão com o banco de dados não fornecida.")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        users_data = cursor.fetchall()

        users = []
        for user_data in users_data:
            user = User(*user_data)
            users.append(user)

        return users

    def close_connection(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection:
            self.connection.close()
