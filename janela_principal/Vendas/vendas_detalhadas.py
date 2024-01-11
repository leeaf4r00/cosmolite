import PySimpleGUI as sg
import os

class VendasDetalhadas:
    def __init__(self):
        self.cart = []
        self.db = Database('Controle_estoque/database.db')
        self.window = None
        self.desconto_type = 'porcentagem'

    def open_vendas_detalhadas(self):
        """
        Abre a janela de Vendas Detalhadas.
        """
        sg.theme('DarkBlue14')

        # Layout de informações gerais
        general_layout = [
            [sg.Text('Vendedor:', size=(15, 1)), sg.Input(key='-VENDEDOR-'), sg.Button('Selecionar Vendedor')],
            [sg.Text('Cliente:', size=(15, 1)), sg.Input(key='-CLIENTE-'), sg.Button('Selecionar Cliente')],
            [sg.Text('CPF:', size=(15, 1)), sg.Input(key='-CPF-')],
            [sg.Text('Desconto:', size=(15, 1)), sg.Input(key='-DESCONTO-'), sg.Radio('Porcentagem', 'RADIO1', key='-DESCONTO_PORCENTAGEM-', default=True), sg.Radio('Valor', 'RADIO1', key='-DESCONTO_VALOR-')],
        ]

        # Layout do carrinho de compras
        cart_layout = [
            [sg.Text('Carrinho de Compras:')],
            [sg.Column([
                [sg.Input(size=(10, 1), key='-QUANTIDADE-', enable_events=True, default_text='0')],
                [sg.Input(size=(30, 1), key='-PRODUTO-', enable_events=True)],
                [sg.Button('Adicionar', key='-ADD_PRODUCT-')]
            ]),
            sg.Listbox([], size=(40, 10), key='-CART-', enable_events=True)],
            [sg.Text('Total:'), sg.Text('R$ 0.00', key='-TOTAL-', size=(10, 1))],
        ]

        # Layout dos botões
        button_layout = [
            [sg.Button('Remover Produto', key='-REMOVE_PRODUCT-')],
            [sg.Button('Finalizar Venda'), sg.Button('Cancelar Venda')],
            [sg.Button('Cadastrar Produtos')],
        ]

        # Layout completo
        layout = [
            [sg.Text('Vendas Detalhadas', font=('Helvetica', 20))],
            [sg.Column(general_layout)],
            [sg.Column(cart_layout)],
            [sg.Column(button_layout)],
        ]

        self.window = sg.Window('Vendas Detalhadas', layout)

        while True:
            event, values = self.window.read()

            if event is None:
                break

            if event == 'Selecionar Vendedor':
                selected_vendedor = self.select_vendedor()
                if selected_vendedor:
                    self.update_selected_vendedor(selected_vendedor)

            if event == 'Selecionar Cliente':
                selected_client = self.select_client()
                if selected_client:
                    self.update_selected_client(selected_client)

            if event == '-DESCONTO_PORCENTAGEM-':
                self.desconto_type = 'porcentagem'

            if event == '-DESCONTO_VALOR-':
                self.desconto_type = 'valor'

            if event == '-ADD_PRODUCT-':
                self.add_product(values)

            if event == '-REMOVE_PRODUCT-':
                self.remove_product()

            if event == '-QUANTIDADE-':
                self.update_total()

            if event == '-CART-':
                self.update_total()

            if event == 'Finalizar Venda':
                self.show_payment_options()

            if event == 'Cancelar Venda':
                self.cancel_sale()
                
            if event == 'Cadastrar Produtos':
                self.cadastrar_produtos()

        self.window.close()

    def select_vendedor(self):
        """
        Abre uma janela para selecionar um vendedor.

        Returns:
            dict: O vendedor selecionado ou None caso não seja selecionado.
        """
        # Aqui você pode implementar a lógica para abrir a janela de seleção de vendedor
        # e retornar o vendedor selecionado da lista de vendedores do seu sistema
        # Por enquanto, vamos apenas retornar um vendedor de exemplo
        selected_vendedor = {
            'name': 'Vendedor de Exemplo',
            'id': '001'
        }
        return selected_vendedor

    def update_selected_vendedor(self, selected_vendedor):
        """
        Atualiza as informações do vendedor selecionado na interface.

        Args:
            selected_vendedor (dict): O vendedor selecionado.
        """
        self.window['-VENDEDOR-'].update(selected_vendedor['name'])

    def select_client(self):
        """
        Abre uma janela para selecionar um cliente.

        Returns:
            dict: O cliente selecionado ou None caso não seja selecionado.
        """
        # Aqui você pode implementar a lógica para abrir a janela de seleção de cliente
        # e retornar o cliente selecionado da lista de clientes do seu sistema
        # Por enquanto, vamos apenas retornar um cliente de exemplo
        selected_client = {
            'name': 'Cliente de Exemplo',
            'cpf': '123.456.789-00'
        }
        return selected_client

    def update_selected_client(self, selected_client):
        """
        Atualiza as informações do cliente selecionado na interface.

        Args:
            selected_client (dict): O cliente selecionado.
        """
        self.window['-CLIENTE-'].update(selected_client['name'])
        self.window['-CPF-'].update(selected_client['cpf'])

    def add_product(self, values):
        """
        Adiciona o produto ao carrinho de compras.

        Args:
            values (dict): Os valores dos elementos da interface.
        """
        product_code = values['-PRODUTO-']
        quantity = int(values['-QUANTIDADE-'])
        if product_code and quantity > 0:
            product = self.get_product_by_code(product_code)
            if product:
                product['quantity'] = quantity
                self.cart.append(product)
                self.update_cart_list()
                self.update_total()

    def remove_product(self):
        """
        Remove o produto selecionado do carrinho de compras.
        """
        selected_product = self.get_selected_product()
        if selected_product:
            self.cart.remove(selected_product)
            self.update_cart_list()
            self.update_total()

    def get_selected_product(self):
        """
        Retorna o produto selecionado na lista de produtos do carrinho de compras.

        Returns:
            dict: O produto selecionado ou None caso nenhum produto seja selecionado.
        """
        selected_index = self.window['-CART-'].get_indexes()
        if selected_index:
            return self.cart[selected_index[0]]
        return None

    def update_cart_list(self):
        """
        Atualiza a lista de produtos no carrinho de compras.
        """
        cart_list = [f"{product['description']} - R$ {product['sale_price']:.2f} x {product['quantity']}" for product in self.cart]
        self.window['-CART-'].update(cart_list)

    def update_total(self):
        """
        Atualiza o valor total da venda.
        """
        total = self.calculate_total()
        self.window['-TOTAL-'].update(f"R$ {total:.2f}")

    def get_product_by_code(self, product_code):
        """
        Retorna o produto com base no código do produto.

        Args:
            product_code (str): O código do produto.

        Returns:
            dict: O produto encontrado ou None caso não exista.
        """
        products = self.db.get_all_products()
        for product in products:
            if product['ean'] == product_code:
                return product
        return None

    def show_payment_options(self):
        """
        Exibe as opções de pagamento.
        """
        layout = [
            [sg.Text('Forma de Pagamento')],
            [sg.Radio('Dinheiro', 'RADIO1', key='-DINHEIRO-'), sg.Input(key='-VALOR_DINHEIRO-', enable_events=True)],
            [sg.Radio('Vale', 'RADIO1', key='-VALE-'), sg.Input(key='-VALOR_VALE-', enable_events=True)],
            [sg.Radio('Débito', 'RADIO1', key='-DEBITO-'), sg.Input(key='-VALOR_DEBITO-', enable_events=True)],
            [sg.Radio('Crédito', 'RADIO1', key='-CREDITO-'), sg.Input(key='-VALOR_CREDITO-', enable_events=True)],
            [sg.Radio('PIX', 'RADIO1', key='-PIX-'), sg.Input(key='-VALOR_PIX-', enable_events=True)],
            [sg.Radio('Cobrança Bancária', 'RADIO1', key='-COBRANCA_BANCARIA-'), sg.Input(key='-VALOR_COBRANCA_BANCARIA-', enable_events=True)],
            [sg.Button('Pagamento Misto', key='-PAGAMENTO_MISTO-')],
            [sg.Text('Total:'), sg.Text('R$ 0.00', key='-TOTAL_PAGAMENTO-', size=(10, 1))],
            [sg.Button('Finalizar Venda'), sg.Button('Cancelar Venda'), sg.Button('Voltar')]
        ]

        window = sg.Window('Opções de Pagamento', layout)

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == 'Voltar':
                break

            if event == '-DINHEIRO-' or event == '-VALOR_DINHEIRO-' or event == '-VALE-' or event == '-VALOR_VALE-' or \
                    event == '-DEBITO-' or event == '-VALOR_DEBITO-' or event == '-CREDITO-' or event == '-VALOR_CREDITO-' or \
                    event == '-PIX-' or event == '-VALOR_PIX-' or event == '-COBRANCA_BANCARIA-' or event == '-VALOR_COBRANCA_BANCARIA-':
                self.update_total_pagamento(values)

            if event == 'Pagamento Misto':
                window.close()
                self.show_mixed_payment_options()
                break

            if event == 'Finalizar Venda':
                self.finalize_payment(values)

            if event == 'Cancelar Venda':
                self.cancel_sale()

        window.close()

    def show_mixed_payment_options(self):
        """
        Exibe as opções de pagamento misto.
        """
        layout = [
            [sg.Text('Pagamento Misto')],
            [sg.Column([
                [sg.Text('Dinheiro:'), sg.Input(key='-MISTO_DINHEIRO-', enable_events=True)],
                [sg.Text('Vale:'), sg.Input(key='-MISTO_VALE-', enable_events=True)],
                [sg.Text('Débito:'), sg.Input(key='-MISTO_DEBITO-', enable_events=True)],
                [sg.Text('Crédito:'), sg.Input(key='-MISTO_CREDITO-', enable_events=True)],
                [sg.Text('PIX:'), sg.Input(key='-MISTO_PIX-', enable_events=True)],
                [sg.Text('Cobrança Bancária:'), sg.Input(key='-MISTO_COBRANCA_BANCARIA-', enable_events=True)],
            ])],
            [sg.Button('Finalizar Venda'), sg.Button('Cancelar Venda'), sg.Button('Voltar')]
        ]

        window = sg.Window('Pagamento Misto', layout)

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == 'Voltar':
                break

            if event == '-MISTO_DINHEIRO-' or event == '-MISTO_VALE-' or event == '-MISTO_DEBITO-' or event == '-MISTO_CREDITO-' or \
                    event == '-MISTO_PIX-' or event == '-MISTO_COBRANCA_BANCARIA-':
                self.update_total_pagamento(values)

            if event == 'Finalizar Venda':
                self.finalize_mixed_payment(values)

            if event == 'Cancelar Venda':
                self.cancel_sale()

        window.close()

    def update_total_pagamento(self, values):
        """
        Atualiza o valor total do pagamento.

        Args:
            values (dict): Os valores dos elementos da interface.
        """
        total = self.calculate_total()
        total_pagamento = 0.0

        if values['-DINHEIRO-'] and values['-VALOR_DINHEIRO-']:
            total_pagamento += float(values['-VALOR_DINHEIRO-'])

        if values['-VALE-'] and values['-VALOR_VALE-']:
            total_pagamento += float(values['-VALOR_VALE-'])

        if values['-DEBITO-'] and values['-VALOR_DEBITO-']:
            total_pagamento += float(values['-VALOR_DEBITO-'])

        if values['-CREDITO-'] and values['-VALOR_CREDITO-']:
            total_pagamento += float(values['-VALOR_CREDITO-'])

        if values['-PIX-'] and values['-VALOR_PIX-']:
            total_pagamento += float(values['-VALOR_PIX-'])

        if values['-COBRANCA_BANCARIA-'] and values['-VALOR_COBRANCA_BANCARIA-']:
            total_pagamento += float(values['-VALOR_COBRANCA_BANCARIA-'])

        if total_pagamento > total:
            total_pagamento = total

        self.window['-TOTAL_PAGAMENTO-'].update(f"R$ {total_pagamento:.2f}")

    def finalize_payment(self, values):
        """
        Finaliza a venda.

        Args:
            values (dict): Os valores dos elementos da interface.
        """
        total = self.calculate_total()
        total_pagamento = 0.0

        if values['-DINHEIRO-'] and values['-VALOR_DINHEIRO-']:
            total_pagamento += float(values['-VALOR_DINHEIRO-'])

        if values['-VALE-'] and values['-VALOR_VALE-']:
            total_pagamento += float(values['-VALOR_VALE-'])

        if values['-DEBITO-'] and values['-VALOR_DEBITO-']:
            total_pagamento += float(values['-VALOR_DEBITO-'])

        if values['-CREDITO-'] and values['-VALOR_CREDITO-']:
            total_pagamento += float(values['-VALOR_CREDITO-'])

        if values['-PIX-'] and values['-VALOR_PIX-']:
            total_pagamento += float(values['-VALOR_PIX-'])

        if values['-COBRANCA_BANCARIA-'] and values['-VALOR_COBRANCA_BANCARIA-']:
            total_pagamento += float(values['-VALOR_COBRANCA_BANCARIA-'])

        if total_pagamento >= total:
            self.save_sale()
            sg.popup('Venda finalizada com sucesso!')
            self.clear_fields()
        else:
            sg.popup('Valor de pagamento insuficiente!')

    def finalize_mixed_payment(self, values):
        """
        Finaliza a venda com pagamento misto.

        Args:
            values (dict): Os valores dos elementos da interface.
        """
        total = self.calculate_total()
        total_pagamento = 0.0

        if values['-MISTO_DINHEIRO-']:
            total_pagamento += float(values['-MISTO_DINHEIRO-'])

        if values['-MISTO_VALE-']:
            total_pagamento += float(values['-MISTO_VALE-'])

        if values['-MISTO_DEBITO-']:
            total_pagamento += float(values['-MISTO_DEBITO-'])

        if values['-MISTO_CREDITO-']:
            total_pagamento += float(values['-MISTO_CREDITO-'])

        if values['-MISTO_PIX-']:
            total_pagamento += float(values['-MISTO_PIX-'])

        if values['-MISTO_COBRANCA_BANCARIA-']:
            total_pagamento += float(values['-MISTO_COBRANCA_BANCARIA-'])

        if total_pagamento >= total:
            self.save_sale()
            sg.popup('Venda finalizada com sucesso!')
            self.clear_fields()
        else:
            sg.popup('Valor de pagamento insuficiente!')

    def save_sale(self):
        """
        Salva a venda no banco de dados.
        """
        # Aqui você pode implementar a lógica para salvar a venda no banco de dados
        # Utilize as informações do carrinho de compras e dos elementos da interface
        # para registrar a venda corretamente

        # Exemplo de código para salvar a venda
        for product in self.cart:
            product_code = product['code']
            product_quantity = product['quantity']
            self.db.update_product_quantity(product_code, product_quantity)

        # Limpando o carrinho de compras
        self.cart = []
        self.update_cart_list()
        self.update_total()

    def cancel_sale(self):
        """
        Cancela a venda.
        """
        # Aqui você pode implementar a lógica para cancelar a venda
        # por exemplo, removendo os produtos do carrinho de compras
        # e atualizando a interface

        # Limpando o carrinho de compras
        self.cart = []
        self.update_cart_list()
        self.update_total()

    def clear_fields(self):
        """
        Limpa os campos da interface.
        """
        self.window['-VENDEDOR-'].update('')
        self.window['-CLIENTE-'].update('')
        self.window['-CPF-'].update('')
        self.window['-DESCONTO-'].update('')
        self.window['-DESCONTO_PORCENTAGEM-'].update(True)
        self.window['-DESCONTO_VALOR-'].update(False)
        self.window['-QUANTIDADE-'].update('0')
        self.window['-PRODUTO-'].update('')
        self.window['-CART-'].update([])
        self.window['-TOTAL-'].update('R$ 0.00')

    def calculate_total(self):
        """
        Calcula o valor total da venda.

        Returns:
            float: O valor total da venda.
        """
        total = 0.0
        for product in self.cart:
            total += product['sale_price'] * product['quantity']

        desconto = self.get_desconto()

        if self.desconto_type == 'porcentagem':
            total -= total * desconto / 100
        else:
            total -= desconto

        return total

    def get_desconto(self):
        """
        Retorna o valor do desconto.

        Returns:
            float: O valor do desconto.
        """
        desconto = self.window['-DESCONTO-'].get()
        if desconto:
            return float(desconto)
        return 0.0

    def cadastrar_produtos(self):
        """
        Abre a janela de cadastro de produtos.
        """
        layout = [
            [sg.Text('Cadastro de Produtos')],
            [sg.Text('Código:', size=(15, 1)), sg.Input(key='-CODIGO-')],
            [sg.Text('Descrição:', size=(15, 1)), sg.Input(key='-DESCRICAO-')],
            [sg.Text('Preço de Venda:', size=(15, 1)), sg.Input(key='-PRECO_VENDA-')],
            [sg.Text('Quantidade:', size=(15, 1)), sg.Input(key='-QUANTIDADE_PRODUTO-')],
            [sg.Button('Cadastrar'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Cadastro de Produtos', layout)

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break

            if event == 'Cadastrar':
                codigo = values['-CODIGO-']
                descricao = values['-DESCRICAO-']
                preco_venda = float(values['-PRECO_VENDA-'])
                quantidade = int(values['-QUANTIDADE_PRODUTO-'])

                product = {
                    'code': codigo,
                    'description': descricao,
                    'sale_price': preco_venda,
                    'quantity': quantidade
                }

                self.db.insert_product(product)
                sg.popup('Produto cadastrado com sucesso!')
                window.close()
                break

        window.close()


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_tables()

    def create_tables(self):
        """
        Cria as tabelas do banco de dados.
        """
        # Aqui você pode implementar a lógica para criar as tabelas
        # do banco de dados utilizando a biblioteca de sua escolha
        # Por enquanto, vamos apenas criar uma tabela de exemplo
        if not os.path.exists(self.db_file):
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    code TEXT PRIMARY KEY,
                    description TEXT,
                    sale_price REAL,
                    quantity INTEGER
                )
            ''')
            connection.commit()
            connection.close()

    def insert_product(self, product):
        """
        Insere um produto no banco de dados.

        Args:
            product (dict): O produto a ser inserido.
        """
        # Aqui você pode implementar a lógica para inserir um produto
        # no banco de dados utilizando a biblioteca de sua escolha
        # Por enquanto, vamos apenas inserir um produto de exemplo
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO products VALUES (?, ?, ?, ?)', (
            product['code'],
            product['description'],
            product['sale_price'],
            product['quantity']
        ))
        connection.commit()
        connection.close()

    def update_product_quantity(self, product_code, quantity):
        """
        Atualiza a quantidade de um produto no banco de dados.

        Args:
            product_code (str): O código do produto.
            quantity (int): A nova quantidade do produto.
        """
        # Aqui você pode implementar a lógica para atualizar a quantidade de um produto
        # no banco de dados utilizando a biblioteca de sua escolha
        # Por enquanto, vamos apenas atualizar a quantidade de um produto de exemplo
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute('UPDATE products SET quantity = ? WHERE code = ?', (quantity, product_code))
        connection.commit()
        connection.close()

    def get_all_products(self):
        """
        Retorna todos os produtos cadastrados no banco de dados.

        Returns:
            list: Uma lista com todos os produtos.
        """
        # Aqui você pode implementar a lógica para retornar todos os produtos
        # cadastrados no banco de dados utilizando a biblioteca de sua escolha
        # Por enquanto, vamos apenas retornar uma lista com produtos de exemplo
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM products')
        products = []
        for row in cursor.fetchall():
            product = {
                'code': row[0],
                'description': row[1],
                'sale_price': row[2],
                'quantity': row[3]
            }
            products.append(product)
        connection.close()
        return products


if __name__ == '__main__':
    vendas_detalhadas = VendasDetalhadas()
    vendas_detalhadas.open_vendas_detalhadas()
