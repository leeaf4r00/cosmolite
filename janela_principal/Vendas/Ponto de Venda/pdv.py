import PySimpleGUI as sg
from database_cadastro_produtos import Database


class PDV:
    def __init__(self):
        self.window = None
        self.cart = []

    def open_pdv(self):
        """
        Abre a janela do Ponto de Venda.
        """
        self.create_window()
        self.load_products()

        while True:
            event, values = self.window.read()

            if event is None:
                break

            if event == 'Adicionar':
                product_code = values['-PRODUCT_CODE-']
                if product_code:
                    self.add_product(product_code)

            if event == 'Remover':
                self.remove_product()

            if event == 'Finalizar Venda':
                self.finalize_sale()

            if event == 'Cancelar Venda':
                self.cancel_sale()

        self.window.close()

    def create_window(self):
        """
        Cria a janela do PDV com o layout inicial.
        """
        sg.theme('DarkBlue14')

        layout = [
            [sg.Text('Ponto de Venda', font=('Helvetica', 20))],
            [sg.Text('Código do Produto:', size=(15, 1)), sg.Input(key='-PRODUCT_CODE-'), sg.Button('Adicionar')],
            [sg.Text('Quantidade:', size=(15, 1)), sg.Input(key='-QUANTITY-'), sg.Button('Remover')],
            [sg.Text('Total:', size=(15, 1)), sg.Text('R$ 0.00', size=(10, 1), key='-TOTAL-')],
            [sg.Text('Carrinho de Compras:')],
            [sg.Listbox([], size=(50, 10), key='-CART-')],
            [sg.Button('Finalizar Venda'), sg.Button('Cancelar Venda')]
        ]

        self.window = sg.Window('Ponto de Venda', layout, resizable=True, finalize=True)
        self.window.maximize()

    def load_products(self):
        """
        Carrega os produtos do banco de dados.
        """
        db = Database('Controle_estoque/database.db')
        self.products = db.get_all_products()

    def add_product(self, product_code):
        """
        Adiciona um produto ao carrinho de compras.

        Args:
            product_code (str): O código do produto.
        """
        product = self.get_product_by_code(product_code)
        if product:
            self.cart.append(product)
            self.update_cart_list()
            self.update_total()

    def remove_product(self):
        """
        Remove o último produto adicionado do carrinho de compras.
        """
        if self.cart:
            self.cart.pop()
            self.update_cart_list()
            self.update_total()

    def finalize_sale(self):
        """
        Finaliza a venda e exibe o total.
        """
        total = self.calculate_total()
        if total > 0:
            sg.popup(f"Venda finalizada! Total: R$ {total:.2f}")
            self.cart.clear()
            self.update_cart_list()
            self.update_total()

    def cancel_sale(self):
        """
        Cancela a venda e limpa o carrinho de compras.
        """
        sg.popup("Cancelando venda...")
        self.cart.clear()
        self.update_cart_list()
        self.update_total()

    def get_product_by_code(self, product_code):
        """
        Retorna o produto com base no código do produto.

        Args:
            product_code (str): O código do produto.

        Returns:
            dict: O produto encontrado ou None caso não exista.
        """
        for product in self.products:
            if product['ean'] == product_code:
                return product
        return None

    def update_cart_list(self):
        """
        Atualiza a lista de produtos no carrinho de compras.
        """
        cart_list = [f"{product['description']} - R$ {product['sale_price']:.2f}" for product in self.cart]
        self.window['-CART-'].update(cart_list)

    def update_total(self):
        """
        Atualiza o valor total da venda.
        """
        total = self.calculate_total()
        self.window['-TOTAL-'].update(f"R$ {total:.2f}")

    def calculate_total(self):
        """
        Calcula o valor total da venda.

        Returns:
            float: O valor total da venda.
        """
        total = 0
        for product in self.cart:
            total += product['sale_price']
        return total


if __name__ == '__main__':
    pdv = PDV()
    pdv.open_pdv()
