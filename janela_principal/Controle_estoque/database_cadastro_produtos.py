import sqlite3
import os

class Database:
    connection = None

    def __init__(self, arquivo_banco_dados):
        self.arquivo_banco_dados = os.path.join(os.path.dirname(__file__), arquivo_banco_dados)
        self.criar_tabela()

    def criar_tabela(self):
        if not Database.connection:
            Database.connection = sqlite3.connect(self.arquivo_banco_dados)

        cursor = Database.connection.cursor()

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

        Database.connection.commit()
        print("Banco de dados gerado com sucesso.")

    def check_product(self, ean):
        cursor = Database.connection.cursor()

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

        cursor = Database.connection.cursor()

        if self.check_product(ean):
            print("Produto já existe.")
            return

        cursor.execute("""
            INSERT INTO products (ean, description, sector, unit, cost_price, avg_price, sale_price, quantity, internal_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ean, description, sector, unit, cost_price, avg_price, sale_price, quantity, internal_code))

        Database.connection.commit()
        print("Produto cadastrado com sucesso.")

    def add_fiscal_info(self, ean, base_icms, aliquot_icms, base_calculo_icms, aliquot_ipi, cst_csosn, cest):
        if not all(isinstance(val, (int, float)) for val in (base_icms, aliquot_icms, base_calculo_icms, aliquot_ipi)):
            print("Os valores fiscais devem ser números.")
            return

        cursor = Database.connection.cursor()

        cursor.execute("""
            INSERT INTO fiscal_info (ean, base_icms, aliquot_icms, base_calculo_icms, aliquot_ipi, cst_csosn, cest)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ean, base_icms, aliquot_icms, base_calculo_icms, aliquot_ipi, cst_csosn, cest))

        Database.connection.commit()

    def get_all_products(self):
        cursor = Database.connection.cursor()

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        return products


if __name__ == '__main__':
    try:
        # Cria o banco de dados 'cadastros_produtos.db' na pasta "janela_principal/Controle_estoque" e imprime a mensagem
        db = Database("cadastrosprodutos.db")
    except sqlite3.OperationalError as e:
        print("Erro ao abrir o banco de dados:", e)