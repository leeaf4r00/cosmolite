import sqlite3


class DbManager:
    def __init__(self):
        """
        Inicializa a classe DbManager e conecta ao banco de dados.
        """
        self.conn = sqlite3.connect("users.db")

    def perform_login(self, username, password):
        """
        Realiza a autenticação do usuário com o nome de usuário e senha fornecidos.

        Args:
            username (str): Nome de usuário.
            password (str): Senha.

        Raises:
            ValueError: Se as credenciais forem inválidas ou não forem preenchidas corretamente.
        """
        if not username or not password:
            raise ValueError("Por favor, preencha todos os campos.")

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()

        if not result:
            raise ValueError("Credenciais inválidas. Tente novamente.")

    def perform_register(self, username, password):
        """
        Realiza o cadastro de um novo usuário com o nome de usuário e senha fornecidos.

        Args:
            username (str): Nome de usuário.
            password (str): Senha.

        Raises:
            ValueError: Se o nome de usuário já estiver em uso ou se algum campo não for preenchido corretamente.
        """
        if not username or not password:
            raise ValueError("Por favor, preencha todos os campos.")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

        if result:
            raise ValueError(
                "Nome de usuário já em uso. Escolha outro nome de usuário.")

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def get_connected_username(self):
        """
        Obtém o nome de usuário conectado.

        Returns:
            str: Nome de usuário conectado.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT username FROM users")
        result = cursor.fetchone()
        return result[0] if result else "Desconhecido"

    def get_connected_users_count(self):
        """
        Obtém o número de usuários conectados.

        Returns:
            int: Número de usuários conectados.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        return result[0]
