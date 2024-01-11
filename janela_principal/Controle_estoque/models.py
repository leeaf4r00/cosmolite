import sqlite3
import os


class Database:
    def __init__(self, arquivo_banco_dados):
        self.arquivo_banco_dados = arquivo_banco_dados
        self.criar_tabela()

    def criar_tabela(self):
        if not os.path.exists(self.arquivo_banco_dados):
            with sqlite3.connect(self.arquivo_banco_dados) as connection:
                cursor = connection.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ean TEXT,
                        description TEXT,
                        sector TEXT,
                        unit TEXT,
                        cost_price REAL,
                        avg_price REAL,
                        sale_price REAL,
                        quantity INTEGER,
                        internal_code TEXT
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fiscal_info (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ean TEXT,
                        base_icms REAL,
                        aliquot_icms REAL,
                        base_calculo_icms REAL,
                        aliquot_ipi REAL,
                        cst_csosn TEXT,
                        cest TEXT
                    )
                """)

            print("Banco de dados gerado com sucesso.")

    def check_product(self, ean):
        with sqlite3.connect(self.arquivo_banco_dados) as connection:
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM products WHERE ean=?", (ean,))
            existing_product = cursor.fetchone()

        return existing_product is not None

    def add_product(self, ean, description, sector, unit, cost_price, avg_price, sale_price, quantity, internal_code):
        if not all(isinstance(val, (int, float)) for val in (cost_price, avg_price, sale_price)):
            print("Os preços devem ser números.")
            return

        if not isinstance(quantity, int):
            print("A quantidade deve ser um número inteiro.")
            return

        with sqlite3.connect(self.arquivo_banco_dados) as connection:
            cursor = connection.cursor()

            if self.check_product(ean):
                print("Produto já existe.")
                return

            cursor.execute("""
                INSERT INTO products (ean, description, sector, unit, cost_price, avg_price, sale_price, quantity, internal_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (ean, description, sector, unit, cost_price, avg_price, sale_price, quantity, internal_code))

            print("Produto cadastrado com sucesso.")

    # Add other methods as required for your application

