import os
import subprocess
import random
import PySimpleGUI as sg
import shutil


def check_create_folder():
    """
    Verifica se a pasta "Controle_estoque" existe e a cria se não existir.
    """
    folder_name = "Controle_estoque"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def run_integration(filename):
    """
    Executa o arquivo de integração localizado na pasta "Controle_estoque".
    """
    folder_name = "Controle_estoque"
    filepath = os.path.join(folder_name, filename)
    subprocess.Popen(["python", filepath])


def open_cadastro_produto():
    """
    Abre a janela de cadastro de produto.
    """
    check_create_folder()

    sg.theme('DarkBlue14')

    # Layout de informações gerais do produto
    general_layout = [
        [sg.Text('Código EAN:', size=(15, 1)), sg.Input(key='-EAN-')],
        [sg.Text('Descrição:', size=(15, 1)), sg.Input(key='-DESCRIPTION-')],
        [sg.Text('Setor:', size=(15, 1)), sg.Input(key='-SECTOR-')],
        [sg.Text('Unidade:', size=(15, 1)), sg.Input(key='-UNIT-')],
        [sg.Text('Preço de Custo:', size=(15, 1)),
         sg.Input(key='-COST_PRICE-')],
        [sg.Text('Preço Médio:', size=(15, 1)), sg.Input(key='-AVG_PRICE-')],
        [sg.Text('Preço de Venda:', size=(15, 1)),
         sg.Input(key='-SALE_PRICE-')],
        [sg.Text('Quantidade:', size=(15, 1)), sg.Input(key='-QUANTITY-')],
        [sg.Text('Código Interno:', size=(15, 1)), sg.Text('', size=(
            10, 1), key='-INTERNAL_CODE-'), sg.Checkbox('Gerar', key='-GENERATE_CODE-')],
    ]

    # Layout de informações fiscais do produto
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

    # Layout de abas com as informações gerais e fiscais
    tab_layout = [
        sg.TabGroup([
            [sg.Tab('Informações Gerais', general_layout)],
            [sg.Tab('Informações Fiscais', fiscal_layout)],
        ])
    ]

    # Layout do contador
    counter_layout = [
        [sg.Text('Quantidade de Produtos:', size=(18, 1)),
         sg.Text('0', size=(10, 1), key='-PRODUCT_COUNT-')],
    ]

    # Layout do inventário físico
    physical_layout = [
        [sg.Text('Quantidade em Estoque:', size=(18, 1)), sg.Text(
            '0', size=(10, 1), key='-STOCK_QUANTITY-')],
        [sg.Text('Quantidade Mínima:', size=(18, 1)), sg.Text(
            '0', size=(10, 1), key='-MIN_QUANTITY-')],
    ]

    # Layout dos botões de módulo
    module_buttons_layout = [
        [sg.Button('Cadastro', key='-CADASTRO-'), sg.Button('PDV', key='-PDV-'),
         sg.Button('Atualização',
                   key='-UPDATE-'), sg.Button('Relatórios', key='-REPORTS-'),
         sg.Button('Listagem', key='-LIST-'), sg.Button('Imprimir',
                                                        key='-PRINT-'),
         sg.Button('Inativo', key='-INACTIVE-'), sg.Button('Configurações', key='-SETTINGS-')],
    ]

    # Layout completo com as abas, contador, inventário físico e botões de módulo
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
            internal_code = values['-INTERNAL_CODE-']
            generate_code = values['-GENERATE_CODE-']

            if generate_code:
                internal_code = generate_internal_code()

            base_icms = values['-BASE_ICMS-']
            aliquot_icms = values['-ALIQUOT_ICMS-']
            base_calculo_icms = values['-BASE_CALCULO_ICMS-']
            aliquot_ipi = values['-ALIQUOT_IPI-']
            cst_csosn = values['-CST_CSOSN-']
            cest = values['-CEST-']

            # Consultar o produto pelo código EAN
            produto = get_consultar_produto()(ean)

            if produto:
                # Atualizar os campos com as informações do produto consultado
                description = produto.get("description")

            db = get_database()
            db.add_product(ean, description, sector, unit, cost_price,
                           avg_price, sale_price, quantity, internal_code)
            db.add_fiscal_info(ean, base_icms, aliquot_icms,
                               base_calculo_icms, aliquot_ipi, cst_csosn, cest)
            print('Produto cadastrado com sucesso!')

        if event == '-QUERY-':
            db = get_database()
            products = db.get_all_products()
            for product in products:
                print(f'Produto: {product}')

        if event == '-UPDATE-':
            run_integration('Atualizacao.py')

        if event == '-REPORTS-':
            run_integration('Relatorios.py')

        if event == '-LIST-':
            run_integration('Listagem.py')

        if event == '-PRINT-':
            run_integration('Imprimir.py')

        if event == '-INACTIVE-':
            run_integration('Inativo.py')

        if event == '-SETTINGS-':
            run_integration('Configuracoes.py')

        if event == '-PDV-':
            run_integration('pdv.py')

    window.close()


def generate_internal_code():
    """
    Gera um código interno único para o produto.
    """
    code = random.randint(10000, 99999)
    return f'IC{code}'


def get_database():
    """
    Retorna uma instância do objeto Database para acessar o banco de dados.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    consultar_produtos_fiscais_path = os.path.join(
        current_dir, "consultar_produtos_fiscais.py")

    # Verifica se o arquivo consultar_produtos_fiscais.py existe na pasta correta
    if not os.path.exists(consultar_produtos_fiscais_path):
        print("Arquivo 'consultar_produtos_fiscais.py' não encontrado na pasta correta.")
        return None

    # Importa a função consultar_produto do módulo consultar_produtos_fiscais
    from consultar_produtos_fiscais import consultar_produto

    database_file = os.path.join("Controle_estoque", "database.db")
    database_module = os.path.join(
        "Controle_estoque", "database_cadastro_produtos.py")

    # Verifica se o arquivo database_cadastro_produtos.py existe na pasta Controle_estoque
    if not os.path.exists(database_module):
        # Copia o arquivo database_cadastro_produtos.py para a pasta Controle_estoque
        shutil.copy("database_cadastro_produtos.py", database_module)

    # Importa a classe Database do módulo database_cadastro_produtos
    from database_cadastro_produtos import Database

    return Database(database_file)


if __name__ == '__main__':
    open_cadastro_produto()
