import PySimpleGUI as sg
import os
import sqlite3

# Caminho para o arquivo do banco de dados
database_file = 'janela principal/database_cadastro_produtos.db'

# Verifica se o arquivo do banco de dados existe e, caso não exista, cria-o
if not os.path.exists(database_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Cria a tabela 'products' caso não exista
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            ean TEXT,
            preco_custo REAL,
            preco_final REAL,
            preco_medio REAL
        )
    """)

    conn.commit()
    conn.close()

# Classe para interagir com o banco de dados
class Database:
    def __init__(self, database_file):
        self.database_file = database_file

    def check_product(self, nome_produto):
        """
        Verifica se o produto existe no banco de dados.

        Args:
            nome_produto (str): O nome do produto a ser verificado.

        Returns:
            bool: True se o produto existe, False caso contrário.
        """
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()

        # Verifica se o produto existe no banco de dados
        cursor.execute("SELECT * FROM products WHERE nome=?", (nome_produto,))
        existing_product = cursor.fetchone()

        conn.close()

        return existing_product is not None

    def add_product(self, nome_produto, ean, preco_custo, preco_final):
        """
        Adiciona um novo produto ao banco de dados.

        Args:
            nome_produto (str): O nome do produto.
            ean (str): O código EAN do produto.
            preco_custo (float): O preço de custo do produto.
            preco_final (float): O preço final do produto.
        """
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()

        # Verifica se o produto já existe no banco de dados
        if self.check_product(nome_produto):
            sg.popup('Produto já existe.')
        elif nome_produto.strip() == '' or ean.strip() == '' or preco_custo.strip() == '' or preco_final.strip() == '':
            sg.popup('Todos os campos devem ser preenchidos.')
        else:
            try:
                # Verifica se os preços são números válidos
                preco_custo = float(preco_custo)
                preco_final = float(preco_final)

                # Calcula o preço médio
                preco_medio = (preco_custo + preco_final) / 2

                # Adiciona o novo produto
                cursor.execute("""
                    INSERT INTO products (nome, ean, preco_custo, preco_final, preco_medio)
                    VALUES (?, ?, ?, ?, ?)
                """, (nome_produto, ean, preco_custo, preco_final, preco_medio))

                conn.commit()
                sg.popup(f'Produto cadastrado com sucesso! Preço médio: {preco_medio:.2f}')
            except ValueError:
                sg.popup('Os preços informados são inválidos.')

        conn.close()

    def list_products(self):
        """
        Lista todos os produtos cadastrados no banco de dados.
        """
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()

        # Seleciona todos os produtos
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        conn.close()

        if products:
            for product in products:
                sg.popup(f'ID: {product[0]}, Nome: {product[1]}, EAN: {product[2]}, Preço de Custo: {product[3]:.2f}, Preço Final: {product[4]:.2f}, Preço Médio: {product[5]:.2f}')
        else:
            sg.popup('Nenhum produto cadastrado.')

# Inicializa a instância da classe Database
db = Database(database_file)

# Definir o layout da janela
layout = [
    [sg.Text('Nome do Produto:'), sg.Input(key='-NOME-')],
    [sg.Text('EAN:'), sg.Input(key='-EAN-')],
    [sg.Text('Preço de Custo:'), sg.Input(key='-CUSTO-')],
    [sg.Text('Preço Final:'), sg.Input(key='-FINAL-')],
    [sg.Button('Cadastrar')],
    [sg.Button('Listar Produtos')],
]

# Criar a janela
window = sg.Window('Cadastrar Produto', layout)

# Loop para interação com a janela
while True:
    event, values = window.read()
    if event is None:
        break
    elif event == 'Cadastrar':
        nome_produto = values['-NOME-']
        ean = values['-EAN-']
        preco_custo = values['-CUSTO-']
        preco_final = values['-FINAL-']

        # Adiciona o novo produto ao banco de dados
        db.add_product(nome_produto, ean, preco_custo, preco_final)
    elif event == 'Listar Produtos':
        # Lista os produtos cadastrados no banco de dados
        db.list_products()

# Fechar a janela ao sair do loop
window.close()
