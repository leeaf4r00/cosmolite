import os
import subprocess
import random
import PySimpleGUI as sg
from database_cadastro_produtos import Database


class ProductRegistrationWindow:
    def __init__(self):
        self.folder_name = "Controle_estoque"
        self.database_module_name = "database_cadastro_produtos"
        self.database_file_name = "cadastrosprodutos.db"

    def check_create_folder(self):
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)

    def run_integration(self, filename: str):
        filepath = os.path.join(self.folder_name, filename)
        subprocess.Popen(["python", filepath])

    def open_product_registration_window(self):
        self.check_create_folder()

        sg.theme('DarkBlue14')

        general_layout = [
            [sg.Text('Código EAN:', size=(15, 1)), sg.Input(key='-EAN-')],
            [sg.Text('Descrição:', size=(15, 1)),
             sg.Input(key='-DESCRIPTION-')],
            [sg.Text('Setor:', size=(15, 1)), sg.Input(key='-SECTOR-')],
            [sg.Text('Unidade:', size=(15, 1)), sg.Input(key='-UNIT-')],
            [sg.Text('Preço de Custo:', size=(15, 1)),
             sg.Input(key='-COST_PRICE-')],
            [sg.Text('Preço Médio:', size=(15, 1)),
             sg.Input(key='-AVG_PRICE-')],
            [sg.Text('Preço de Venda:', size=(15, 1)),
             sg.Input(key='-SALE_PRICE-')],
            [sg.Text('Quantidade:', size=(15, 1)), sg.Input(key='-QUANTITY-')],
            [sg.Text('Código Interno:', size=(15, 1)), sg.Text('', size=(10, 1), key='-INTERNAL_CODE-'),
             sg.Checkbox('Gerar', key='-GENERATE_CODE-')],
        ]

        fiscal_layout = [
            [sg.Text('Base ICMS:', size=(15, 1)), sg.Input(key='-BASE_ICMS-')],
            [sg.Text('Alíquota ICMS:', size=(15, 1)),
             sg.Input(key='-ALIQUOT_ICMS-')],
            [sg.Text('Base de Cálculo ICMS:', size=(15, 1)),
             sg.Input(key='-BASE_CALCULO_ICMS-')],
            [sg.Text('Alíquota IPI:', size=(15, 1)),
             sg.Input(key='-ALIQUOT_IPI-')],
            [sg.Text('CST CSOSN:', size=(15, 1)), sg.Input(key='-CST_CSOSN-')],
            [sg.Text('CEST:', size=(15, 1)), sg.Input(key='-CEST-')],
        ]

        tab_layout = [
            sg.TabGroup([
                [sg.Tab('Informações Gerais', general_layout)],
                [sg.Tab('Informações Fiscais', fiscal_layout)],
            ])
        ]

        counter_layout = [
            [sg.Text('Quantidade de Produtos:', size=(18, 1)),
             sg.Text('0', size=(10, 1), key='-PRODUCT_COUNT-')],
        ]

        physical_layout = [
            [sg.Text('Quantidade em Estoque:', size=(18, 1)), sg.Text(
                '0', size=(10, 1), key='-STOCK_QUANTITY-')],
            [sg.Text('Quantidade Mínima:', size=(18, 1)), sg.Text(
                '0', size=(10, 1), key='-MIN_QUANTITY-')],
        ]

        module_buttons_layout = [
            [sg.Button('Cadastro', key='-CADASTRO-'), sg.Button('PDV', key='-PDV-'),
             sg.Button(
                 'Atualização', key='-UPDATE-'), sg.Button('Relatórios', key='-REPORTS-'),
             sg.Button(
                 'Listagem', key='-LIST-'), sg.Button('Imprimir', key='-PRINT-'),
             sg.Button('Inativo', key='-INACTIVE-'), sg.Button('Configurações', key='-SETTINGS-')],
        ]

        layout = [
            [sg.Text('Controle de Estoque', font=('Helvetica', 20))],
            [sg.Column(module_buttons_layout, justification='center')],
            tab_layout,
            [sg.Column(counter_layout), sg.Column(physical_layout)],
            [sg.Button('Cadastrar', key='-REGISTER-'),
             sg.Button('Consultar Banco de Dados', key='-QUERY-')]
        ]

        window = sg.Window('Controle de Estoque', layout)

        while True:
            event, values = window.read()

            if event is None:
                break

            if event == '-REGISTER-':
                ean = values['-EAN-']
                description = values['-DESCRIPTION-']
                sector = values['-SECTOR-']
                unit = values['-UNIT-']
                cost_price = values['-COST_PRICE-']
                avg_price = values['-AVG_PRICE-']
                sale_price = values['-SALE_PRICE-']
                quantity = values['-QUANTITY-']
                internal_code = values.get('-INTERNAL_CODE-', '')
                generate_code = values.get('-GENERATE_CODE-', False)

                if not self.is_valid_price(cost_price, avg_price, sale_price):
                    sg.popup_error(
                        'Por favor, preencha os preços corretamente (utilize apenas números).')
                    continue

                if generate_code:
                    internal_code = self.generate_internal_code()

                base_icms = values['-BASE_ICMS-']
                aliquot_icms = values['-ALIQUOT_ICMS-']
                base_calculo_icms = values['-BASE_CALCULO_ICMS-']
                aliquot_ipi = values['-ALIQUOT_IPI-']
                cst_csosn = values['-CST_CSOSN-']
                cest = values['-CEST-']

                db = self.get_database()
                db.add_product(ean, description, sector, unit, cost_price,
                               avg_price, sale_price, quantity, internal_code)
                db.add_fiscal_info(ean, base_icms, aliquot_icms,
                                   base_calculo_icms, aliquot_ipi, cst_csosn, cest)
                print('Produto cadastrado com sucesso!')

            if event == '-QUERY-':
                db = self.get_database()
                products = db.get_all_products()
                for product in products:
                    print(f'Produto: {product}')
                sg.popup("Banco de dados gerado com sucesso. Consulte o arquivo",
                         title="Consulta de Banco de Dados")

            if event == '-UPDATE-':
                self.run_integration('Atualizacao.py')

            if event == '-REPORTS-':
                self.run_integration('Relatorios.py')

            if event == '-LIST-':
                self.run_integration('Listagem.py')

            if event == '-PRINT-':
                self.run_integration('Imprimir.py')

            if event == '-INACTIVE-':
                self.run_integration('Inativo.py')

            if event == '-SETTINGS-':
                self.run_integration('Configuracoes.py')

            if event == '-PDV-':
                self.run_integration('pdv.py')

        window.close()

    def is_valid_price(self, *prices):
        for price in prices:
            try:
                float(price)
            except ValueError:
                return False
        return True

    def generate_internal_code(self) -> str:
        code = random.randint(10000, 99999)
        return f'IC{code}'

    def get_current_directory(self) -> str:
        return os.path.dirname(os.path.abspath(__file__))

    def get_database_file_path(self) -> str:
        # Obtém o diretório do script atual
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Constrói o caminho absoluto para o arquivo do banco de dados
        return os.path.abspath(os.path.join(current_dir, self.folder_name, self.database_file_name))

    def get_database(self):
        database_file = self.get_database_file_path()
        return Database(database_file)


if __name__ == '__main__':
    product_registration_window = ProductRegistrationWindow()
    product_registration_window.open_product_registration_window()
