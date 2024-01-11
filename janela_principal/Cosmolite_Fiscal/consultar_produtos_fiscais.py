import os
import subprocess
import random
import PySimpleGUI as sg
import requests
import webbrowser
import clipboard
import sys
import asyncio
import aiohttp
import cachetools
import csv
import json
import locale
import operator
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime
from typing import Dict, List, Optional

sg.theme('DarkBlue14')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["ROOT_DIR"] = ROOT_DIR

janela_principal_dir = os.path.join(os.environ["ROOT_DIR"], "janela_principal")

if janela_principal_dir not in sys.path:
    sys.path.append(janela_principal_dir)

API_DIR = os.path.join(ROOT_DIR, "api")
HISTORICO_DIR = os.path.join(ROOT_DIR, "historico")
HISTORICO_FILE = os.path.join(HISTORICO_DIR, "historico_data.txt")
VENDAS_DIR = os.path.join(ROOT_DIR, "vendas")
TERMS_DIR = os.path.join(ROOT_DIR, "termos")
CONTROLE_ESTOQUE_DIR = os.path.join(
    janela_principal_dir, "Vendas", "database_cadastro_produtos.py")

sg.theme('DarkBlue14')

pagina_atual = 1
itens_por_pagina = 5

layout = [
    [sg.Text("Escolha o tipo de pesquisa:"), sg.Radio("Código de barras", "RADIO1", default=True, key="-EAN-"),
     sg.Radio("Descrição", "RADIO1", key="-DESC-")],
    [sg.Text("Insira o código EAN ou descrição do produto:"), sg.Input(
        key="-SEARCH-"), sg.Button("Buscar", bind_return_key=True)],
    [sg.Multiline("", size=(100, 8), key="-RETORNO-",
                  font=("Helvetica", 10), auto_size_text=True)],
    [sg.Text("Histórico:")],
    [sg.Listbox([], size=(100, 10), key="-HISTORICO-",
                font=("Helvetica", 10), enable_events=True, auto_size_text=True)],
    [sg.Text("Token da API Cosmos:"), sg.Text("", size=(30, 1), key="-TOKEN-"),
     sg.Button("Trocar Token Cosmos", key="-CHANGE-TOKEN-")],
    [sg.Text("Software Licenciado e Desenvolvido por Rafael Moreira Fernandes | Todos Direitos Reservados ©", font=(
        "Helvetica", 10, "underline"), text_color="white", background_color="red")],
    [sg.Button("Instagram", font=("Helvetica", 10, "underline"), button_color=("white", "purple"), key="-INSTAGRAM-"),
     sg.Button("Whatsapp", font=("Helvetica", 10, "underline"),
               button_color=("white", "green"), key="-WHATSAPP-"),
     sg.Button("Copiar resultado", font=("Helvetica", 10), key="-COPY-"),
     sg.Button("Relatórios Fiscais", font=(
         "Helvetica", 10), key="-RELATORIOS-FISCAIS-"),
     sg.Button("Cadastro de Produto", font=("Helvetica", 10), key="-CADASTRO-")],
    [sg.Text("Tenha controle total de seu negócio e acessando as informações de qualquer lugar e a qualquer hora.")],
    [sg.Button("TERMOS DE USO", font=(
        "Helvetica", 10, "underline"), key="-TERMS-")],
    [sg.Button("Sair", font=("Helvetica", 10), button_color=("white", "red"))],
    # Botões de paginação
    [sg.Button("Anterior", key='-ANTERIOR-', size=(10, 1), disabled=True),
     sg.Text("", key='-PAGINA-', size=(10, 1), justification='center'),
     sg.Button("Próxima", key='-PROXIMA-', size=(10, 1))],
    [sg.Button("Favoritar Produto", font=("Helvetica", 10), key="-FAVORITAR-"),
     sg.Button("Reconsultar Produto", font=("Helvetica", 10), key="-RECONSULTAR-")]
]

window = sg.Window("Consulta de Produto", layout, size=(
    1000, 700), resizable=True, finalize=True)

API_URL = 'https://api.cosmos.bluesoft.com.br/gtins/'
API_HEADERS = {
    'X-Cosmos-Token': 'UJTBhybMZx96n33FzUfp2w',
    'User-Agent': 'API Request'
}

historico = []
cache = cachetools.LRUCache(maxsize=100)
token = 'UJTBhybMZx96n33FzUfp2w'


def check_create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def load_historico():
    global historico
    try:
        with open(HISTORICO_FILE, 'r') as f:
            historico_data = [line.strip() for line in f.readlines()]
            historico = [eval(d) for d in historico_data]
            historico.sort(key=operator.itemgetter(
                "data_consulta"), reverse=True)
            for produto in historico:
                cache[produto["gtin"]] = produto
    except FileNotFoundError:
        pass


def salvar_consulta(produto):
    produto["data_consulta"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historico.append(produto)
    historico.sort(key=operator.itemgetter("data_consulta"), reverse=True)
    save_historico()
    update_historico_display()


def save_historico():
    with open(HISTORICO_FILE, 'w') as f:
        for d in historico:
            f.write(str(d) + '\n')


class Produto:
    def __init__(self, gtin, description, ncm, price, quantity, avg_price, brand_name, gpc_code, gpc_description, gross_weight, height, length, max_price, net_weight, thumbnail, width, data_consulta):
        self.gtin = gtin
        self.description = description
        self.ncm = ncm
        self.price = price
        self.quantity = quantity
        self.avg_price = avg_price
        self.brand_name = brand_name
        self.gpc_code = gpc_code
        self.gpc_description = gpc_description
        self.gross_weight = gross_weight
        self.height = height
        self.length = length
        self.max_price = max_price
        self.net_weight = net_weight
        self.thumbnail = thumbnail
        self.width = width
        self.data_consulta = data_consulta

    def __str__(self):
        return f"Produto: {self.description}, Código EAN: {self.gtin}"


async def fetch_produto(gtin):
    produto = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API_URL}{gtin}.json', headers=API_HEADERS) as response:
                response.raise_for_status()
                produto = await response.json()
    except aiohttp.ClientError as e:
        sg.popup_error(f'Erro ao consultar o produto: {str(e)}')
    return produto


def consultar_produto(gtin):
    produto = None
    if gtin in cache:
        produto = cache[gtin]
    else:
        produto = asyncio.run(fetch_produto(gtin))
        if produto:
            cache[gtin] = produto
    return produto


def buscar_produto(search_term, search_type):
    if search_type == SEARCH_BY_GTIN:
        return next((p for p in historico if p.get('gtin') == search_term), None)
    elif search_type == SEARCH_BY_DESCRIPTION:
        return next((p for p in historico if p.get('description') == search_term), None)
    return None


def format_produto(produto):
    formatted_produto = ''
    produto_info = [
        ("Código EAN", "gtin"),
        ("CEST", "cest.code" if "cest" in produto else None),
        ("NCM", "ncm.code"),
        ("Descrição", "description"),
        ("Descrição NCM", "ncm.full_description"),
        ("Preço", "price"),
        ("Preço Médio", "avg_price"),
        ("Preço Máximo", "max_price"),
        ("Marca", "brand.name"),
        ("Imagem", "thumbnail"),
    ]

    for label, attribute_path in produto_info:
        if attribute_path is not None:
            value = get_nested_value(produto, attribute_path)
            if value is not None:
                formatted_produto += f"{label}: {value}\n"

    url = produto.get("url")
    if url:
        formatted_produto = f'<a href="{url}" style="text-decoration: none; color: inherit;">{formatted_produto}</a>'

    return formatted_produto


def get_nested_value(data, attribute_path):
    attributes = attribute_path.split('.')
    value = data
    for attribute in attributes:
        value = value.get(attribute)
        if not value:
            break
    return value


def format_lista_precos(prices):
    if not prices:
        return "N/A"

    if isinstance(prices, list):
        return " a ".join(prices)

    return prices


def format_imagem(thumbnail):
    if thumbnail:
        return f"<a href='{thumbnail}' target='_blank'><img src='{thumbnail}' width='100'></a>"

    return ""


def update_historico_display(produtos=None):
    global pagina_atual
    produtos_to_show = produtos if produtos else historico
    total_paginas = (len(produtos_to_show) - 1) // itens_por_pagina + 1
    if pagina_atual > total_paginas:
        pagina_atual = total_paginas

    inicio = (pagina_atual - 1) * itens_por_pagina
    fim = inicio + itens_por_pagina
    produtos_pagina = produtos_to_show[inicio:fim]

    historico_layout = []
    for produto in produtos_pagina:
        data_consulta = produto.get('data_consulta', '')
        description = produto.get('description', '')
        price = produto.get('price', '')
        quantity = produto.get('quantity', '')

        historico_layout.append(
            f"Data da Consulta: {data_consulta}, Produto: {description}, Preço: {price}, Quantidade: {quantity}"
        )

    window['-HISTORICO-'].update(historico_layout)
    window['-PAGINA-'].update(f'{pagina_atual} / {total_paginas}')
    window['-ANTERIOR-'].update(disabled=pagina_atual == 1)
    window['-PROXIMA-'].update(disabled=pagina_atual == total_paginas)


def buscar_produtos(values):
    SEARCH_BY_GTIN = "gtin"
    SEARCH_BY_DESCRIPTION = "description"

    search_term = values["-SEARCH-"].strip()
    if not search_term:
        window["-RETORNO-"].update("Insira um valor para a pesquisa.")
        return

    search_type = None

    if values["-EAN-"]:
        search_type = SEARCH_BY_GTIN
    elif values["-DESC-"]:
        search_type = SEARCH_BY_DESCRIPTION

    if search_type is not None:
        produto = buscar_produto(search_term, search_type)

        if not produto:
            window["-RETORNO-"].update(
                f"Produto {search_term} não encontrado na API.")
            return

        result = format_produto(produto)
        window["-RETORNO-"].update(result)
    else:
        window["-RETORNO-"].update(
            "Selecione o tipo de pesquisa: Código de barras ou Descrição.")
    window["-SEARCH-"].update('')


def buscar_produto(search_term, search_type):
    produto = next((p for p in historico if p.get(
        search_type) == search_term), None)
    if not produto:
        produto = consultar_produto(search_term)
        if produto:
            salvar_consulta(produto)
            cache[produto["gtin"]] = produto
    return produto


def format_historico(historico):
    formatted_historico = []
    for index, produto in enumerate(historico):
        formatted_produto = format_produto(produto)
        codigo_ean = produto.get("gtin", "N/A")
        formatted_produto_with_ean = f"Código EAN: {codigo_ean}\n{formatted_produto}"
        formatted_historico.append(formatted_produto_with_ean)
    return formatted_historico


def show_error_popup(error_message):
    layout = [
        [sg.Text("Ocorreu um erro durante a busca do produto.")],
        [
            sg.Multiline(
                error_message,
                size=(60, 10),
                font=("Helvetica", 10),
                key="-ERROR-",
                disabled=True,
                auto_size_text=True,
            )
        ],
        [sg.Button("Copiar Erro", font=("Helvetica", 10), key="-COPY-")]
    ]
    error_window = sg.Window("Erro", layout, finalize=True)
    while True:
        event, _ = error_window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-COPY-":
            clipboard.copy(error_message)
    error_window.close()


def open_cadastro_produto():
    current_dir = os.getcwd()
    controle_estoque_dir = os.path.join(
        current_dir, "janela_principal", "Controle_estoque")
    controle_estoque_path = os.path.join(
        controle_estoque_dir, "controle_estoque.py")
    if os.path.exists(controle_estoque_path):
        subprocess.Popen(["python", controle_estoque_path])


def open_terms_of_use():
    termos_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../termos",
        "termos.py"
    )
    with open(termos_path, "r", encoding="utf-8") as file:
        termos_code = file.read()
    sg.popup_scrolled(termos_code, title="Termos de Uso", size=(80, 20))


def change_token():
    global token
    layout = [
        [sg.Text("Token atual: "), sg.Text(token, key="-TOKEN-")],
        [sg.Text("Digite o novo token: "), sg.Input(key="-NEW-TOKEN-")],
        [sg.Button("Trocar", key="-CONFIRM-"),
         sg.Button("Cancelar", key="-CANCEL-")]
    ]
    token_window = sg.Window("Trocar Token Cosmos", layout, finalize=True)
    while True:
        event, values = token_window.read()
        if event is None:
            break
        if event == "-CONFIRM-":
            new_token = values["-NEW-TOKEN-"]
            if new_token:
                confirm_layout = [
                    [sg.Text(
                        f"Deseja trocar o token atual '{token}' por '{new_token}'?")],
                    [sg.Button("Sim", key="-YES-"),
                     sg.Button("Não", key="-NO-")]
                ]
                confirm_window = sg.Window(
                    "Confirmação", confirm_layout, finalize=True)
                while True:
                    confirm_event, _ = confirm_window.read()
                    if confirm_event == "-YES-":
                        token = new_token
                        sg.popup("Token trocado com sucesso!")
                        break
                    if confirm_event == "-NO-":
                        break
                confirm_window.close()
            else:
                sg.popup_error("O novo token não pode ser vazio!")
    token_window.close()


def get_produto_info(produto):
    produto_info = {
        "codigo_ean": produto.get("gtin"),
        "descricao": produto.get("description"),
        "ncm": produto.get("ncm"),
        "preco": produto.get("price"),
        "quantidade": produto.get("quantity"),
        "preco_medio": produto.get("avg_price"),
        "marca": produto.get("brand.name"),
        "gpc": produto.get("gpc.code - gpc.description"),
        "peso_bruto": produto.get("gross_weight"),
        "altura": produto.get("height"),
        "comprimento": produto.get("length"),
        "preco_maximo": produto.get("max_price"),
        "peso_liquido": produto.get("net_weight"),
        "imagem": produto.get("thumbnail"),
        "largura": produto.get("width")
    }
    return produto_info


def get_produto(gtin_or_description, produtos_dados):
    for produto_data in produtos_dados:
        if (
            gtin_or_description in produto_data['gtin']
            or gtin_or_description in produto_data['description']
        ):
            data_consulta = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            produto = {
                'data_consulta': data_consulta,
                'gtin': produto_data['gtin'],
                'description': produto_data['description'],
                'price': produto_data.get('price', ''),
                'quantity': produto_data.get('quantity', ''),
                'ncm': produto_data.get('ncm', ''),
            }
            return produto
    return None


def get_produto(gtin_or_description, produtos_dados):
    for produto_data in produtos_dados:
        if (
            gtin_or_description in produto_data['gtin']
            or gtin_or_description in produto_data['description']
        ):
            data_consulta = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            produto = {
                'data_consulta': data_consulta,
                'gtin': produto_data['gtin'],
                'description': produto_data['description'],
                'price': produto_data.get('price', ''),
                'quantity': produto_data.get('quantity', ''),
                'ncm': produto_data.get('ncm', ''),
            }
            return produto
    return None


def cadastrar_produto(produto_info):
    print("Cadastrando produto:")
    print(produto_info)


def exportar_historico_csv():
    if not historico:
        sg.popup("Não há histórico para exportar.")
        return

    filename = sg.popup_get_file(
        "Salvar histórico como...",
        save_as=True,
        file_types=(("CSV Files", "*.csv"),),
    )
    if not filename:
        return

    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = historico[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(historico)

        sg.popup(f"Histórico exportado com sucesso para '{filename}'!")
    except Exception as e:
        sg.popup_error(f"Erro ao exportar histórico: {str(e)}")


def exportar_historico_json():
    if not historico:
        sg.popup("Não há histórico para exportar.")
        return

    filename = sg.popup_get_file(
        "Salvar histórico como...",
        save_as=True,
        file_types=(("JSON Files", "*.json"),),
    )
    if not filename:
        return

    try:
        with open(filename, "w", encoding="utf-8") as jsonfile:
            json.dump(historico, jsonfile, indent=4, ensure_ascii=False)

        sg.popup(f"Histórico exportado com sucesso para '{filename}'!")
    except Exception as e:
        sg.popup_error(f"Erro ao exportar histórico: {str(e)}")


def gerar_graficos():
    if not historico:
        sg.popup("Não há histórico para gerar o histograma de preços.")
        return

    all_prices = []
    for produto in historico:
        prices = get_prices(produto)
        all_prices.extend(prices)

    plt.hist(all_prices, bins=20, edgecolor='k', alpha=0.7)
    plt.xlabel("Preço")
    plt.ylabel("Quantidade")
    plt.title("Histograma de Preços")
    plt.show()


def show_favoritar_produto():
    favorito_window = sg.Window("Favoritar Produto", [
        [sg.Text("Selecione um produto para favoritar:")],
        [sg.Listbox(values=format_historico(historico),
                    size=(80, 10), key="-FAVORITAR-PRODUTO-")],
        [sg.Button("Favoritar", key="-FAVORITAR-CONFIRMAR-"),
         sg.Button("Cancelar", key="-FAVORITAR-CANCELAR-")]
    ], finalize=True)
    while True:
        event, values = favorito_window.read()
        if event == sg.WINDOW_CLOSED or event == "-FAVORITAR-CANCELAR-":
            break
        if event == "-FAVORITAR-CONFIRMAR-":
            selected_index = values["-FAVORITAR-PRODUTO-"][0]
            if selected_index is not None:
                selected_produto = historico[selected_index]
                favoritos_path = os.path.join(HISTORICO_DIR, "favoritos.txt")
                with open(favoritos_path, "a") as favoritos_file:
                    favoritos_file.write(str(selected_produto) + "\n")
                sg.popup("Produto favoritado com sucesso!")
                favorito_window.close()
                break
            else:
                sg.popup("Selecione um produto para favoritar.")
    favorito_window.close()


def show_reconsultar_produto():
    reconsultar_window = sg.Window("Reconsultar Produto", [
        [sg.Text("Selecione um produto para reconsultar:")],
        [sg.Listbox(values=format_historico(historico),
                    size=(80, 10), key="-RECONSULTAR-PRODUTO-")],
        [sg.Button("Reconsultar", key="-RECONSULTAR-CONFIRMAR-"),
         sg.Button("Cancelar", key="-RECONSULTAR-CANCELAR-")]
    ], finalize=True)
    while True:
        event, values = reconsultar_window.read()
        if event == sg.WINDOW_CLOSED or event == "-RECONSULTAR-CANCELAR-":
            break
        if event == "-RECONSULTAR-CONFIRMAR-":
            selected_index = values["-RECONSULTAR-PRODUTO-"][0]
            if selected_index is not None:
                selected_produto = historico[selected_index]
                sg.popup(format_produto(selected_produto))
                reconsultar_window.close()
                break
            else:
                sg.popup("Selecione um produto para reconsultar.")
    reconsultar_window.close()


def get_prices(produto):
    price = produto.get('price')
    if not price:
        return []

    if isinstance(price, list):
        # Se o preço for uma lista de preços, retorna os valores numéricos
        return [float(p.replace('R$', '').replace(',', '').strip()) for p in price]
    elif ' a ' in price:
        # Se o preço estiver no formato "R$ 1,24 a R$ 1,81", retorna a lista de preços
        price_range = price.split(' a ')
        return [float(p.replace('R$', '').replace(',', '').strip()) for p in price_range]

    # Se o preço for um único valor, retorna uma lista com esse valor
    return [float(price.replace('R$', '').replace(',', '').strip())]


def plot_price_histogram():
    if not historico:
        sg.popup("Não há histórico para gerar o histograma de preços.")
        return

    all_prices = []
    for produto in historico:
        prices = get_prices(produto)
        all_prices.extend(prices)

    plt.hist(all_prices, bins=20, edgecolor='k', alpha=0.7)
    plt.xlabel("Preço")
    plt.ylabel("Quantidade")
    plt.title("Histograma de Preços")
    plt.show()


def handle_event(event, values):
    global pagina_atual

    if event in (sg.WINDOW_CLOSED, "Sair"):
        window.close()

    elif event == "Buscar":
        buscar_produtos(values)

    elif event == "-INSTAGRAM-":
        webbrowser.open("https://www.instagram.com/RAFAELMOREIRAFERNANDES")

    elif event == "-WHATSAPP-":
        webbrowser.open("https://wa.me/message/556WDBERNK3MM1")

    elif event == "-TERMS-":
        open_terms_of_use()

    elif event == "-CHANGE-TOKEN-":
        change_token()

    elif event == "-COPY-":
        clipboard.copy(values["-RETORNO-"])

    elif event == "-FAVORITAR-":
        show_favoritar_produto()

    elif event == "-RECONSULTAR-":
        show_reconsultar_produto()

    elif event == "-RELATORIOS-FISCAIS-":
        export_layout = [
            [sg.Text("Escolha o formato do relatório:")],
            [sg.Button("CSV", key="-EXPORT-CSV-", font=("Helvetica", 10))],
            [sg.Button("JSON", key="-EXPORT-JSON-", font=("Helvetica", 10))],
            [sg.Button("Histograma de Gráficos",
                       key="-GERAR-GRAFICOS-", font=("Helvetica", 10))]
        ]
        relatorios_fiscais_window = sg.Window(
            "Relatórios Fiscais", export_layout, finalize=True)
        while True:
            event_rf, _ = relatorios_fiscais_window.read()
            if event_rf in (sg.WINDOW_CLOSED, None):
                break
            if event_rf == "-EXPORT-CSV-":
                exportar_historico_csv()
            elif event_rf == "-EXPORT-JSON-":
                exportar_historico_json()
            elif event_rf == "-GERAR-GRAFICOS-":
                gerar_graficos()
        relatorios_fiscais_window.close()

    elif event == "-ANTERIOR-":
        pagina_atual -= 1
        update_historico_display()

    elif event == "-PROXIMA-":
        pagina_atual += 1
        update_historico_display()

    elif event == "-CADASTRO-":
        open_cadastro_produto()


def main():
    load_historico()
    update_historico_display()

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        handle_event(event, values)

    window.close()


if __name__ == "__main__":
    main()
