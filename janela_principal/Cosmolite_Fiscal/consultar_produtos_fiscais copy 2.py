import PySimpleGUI as sg
import requests
import webbrowser
import clipboard
import subprocess

sg.theme('DarkBlue14')

layout = [
    [
        sg.Text("Escolha o tipo de pesquisa:"),
        sg.Radio("Código de barras", "RADIO1", default=True, key="-EAN-"),
        sg.Radio("Descrição", "RADIO1", key="-DESC-")
    ],
    [
        sg.Text("Insira o código EAN ou descrição do produto:"),
        sg.Input(key="-SEARCH-"),
        sg.Button("Buscar", bind_return_key=True),
    ],
    [
        sg.Multiline("", size=(80, 8), key="-RETORNO-",
                     font=("Helvetica", 10), auto_size_text=True)
    ],
    [
        sg.Text("Histórico:")
    ],
    [
        sg.Listbox(
            [], size=(80, 10), key="-HISTORICO-",
            font=("Helvetica", 10), enable_events=True, auto_size_text=True
        )
    ],
    [
        sg.Text("Software Licenciado e Produzido por Rafael Fernandes, Rurópolis-Pará",
                font=("Helvetica", 10, "underline"),
                text_color="white",
                background_color="red")
    ],
    [
        sg.Button("Instagram", font=("Helvetica", 10, "underline"), button_color=("white", "purple"), key="-INSTAGRAM-"),
        sg.Button("Whatsapp", font=("Helvetica", 10, "underline"), button_color=("white", "green"), key="-WHATSAPP-"),
        sg.Button("Copiar resultado", font=("Helvetica", 10), key="-COPY-"),
        sg.Button("Cadastro de Produto", font=("Helvetica", 10), key="-CADASTRO-")
    ],
    [
        sg.Text("Tenha controle total de seu negócio acessando as informações de qualquer lugar e a qualquer hora.")
    ],
    [
        sg.Button("TERMOS DE USO", font=("Helvetica", 10, "underline"), key="-TERMS-")
    ]
]

window = sg.Window("Consulta de Produto", layout, size=(800, 600), resizable=True, finalize=True)

API_URL = 'https://api.cosmos.bluesoft.com.br/gtins/'
API_HEADERS = {
    'X-Cosmos-Token': 'UJTBhybMZx96n33FzUfp2w',
    'User-Agent': 'API Request'
}

historico = []

def consultar_produto(gtin):
    try:
        r = requests.get(f'{API_URL}{gtin}.json', headers=API_HEADERS)
        r.raise_for_status()
        produto = r.json()
        historico.append(produto)
        return produto
    except requests.exceptions.RequestException as e:
        sg.popup_error(f'Erro ao consultar o produto: {str(e)}')
        return None

def save_historico():
    with open('historico.txt', 'w') as f:
        for d in historico:
            f.write(str(d) + '\n')

def load_historico():
    global historico
    try:
        with open('historico.txt', 'r') as f:
            historico_data = [line.strip() for line in f.readlines()]
            historico.extend([eval(d) for d in historico_data])
    except FileNotFoundError:
        pass

def format_produto(produto):
    ean = produto.get("gtin", "N/A")
    description = produto.get("description", "N/A")
    ncm = produto.get("ncm", "N/A")
    price = produto.get("price", "N/A")
    quantity = produto.get("quantity", "N/A")
    avg_price = produto.get("avg_price", "N/A")
    brand = produto.get("brand", {}).get("name", "N/A")
    gpc = produto.get("gpc", {})
    gpc_code = gpc.get("code", "N/A")
    gpc_description = gpc.get("description", "N/A")
    gross_weight = produto.get("gross_weight", "N/A")
    height = produto.get("height", "N/A")
    length = produto.get("length", "N/A")
    max_price = produto.get("max_price", "N/A")
    net_weight = produto.get("net_weight", "N/A")
    thumbnail = produto.get("thumbnail", "N/A")
    width = produto.get("width", "N/A")

    formatted_produto = (
        f"Código EAN: {ean}\n"
        f"Descrição: {description}\n"
        f"NCM: {ncm}\n"
        f"Preço: {price}\n"
        f"Quantidade: {quantity}\n"
        f"Preço Médio: {avg_price}\n"
        f"Marca: {brand}\n"
        f"GPC: {gpc_code} - {gpc_description}\n"
        f"Peso Bruto: {gross_weight} g\n"
        f"Altura: {height} cm\n"
        f"Comprimento: {length} cm\n"
        f"Preço Máximo: {max_price}\n"
        f"Peso Líquido: {net_weight} g\n"
        f"Imagem: {thumbnail}\n"
        f"Largura: {width} cm\n"
    )
    return formatted_produto

def format_historico():
    return [f"Código EAN: {p['gtin']} - Descrição: {p['description']}" for p in historico]

def open_cadastro_produto():
    subprocess.Popen(["python", "cadastro_produto.py"])

def open_terms_of_use():
    sg.popup("""Termos de Uso:
A RR SISTEMAS não se responsabiliza pela utilização das informações tributárias do programa Cosmos.

Antes da coleta e utilização de qualquer informação e dados pessoais, o USUÁRIO da Cosmos deverá:
a) somente coletar dados pessoais se o motivo estiver fundamentado em uma das bases legais previstas no artigo 7º da Lei nº 13.709/2018, que trata da Lei Geral de Proteção de Dados (LGPD);
b) obter a aprovação de um contador que se responsabilize legalmente pela classificação das informações tributárias inseridas na plataforma.

A inobservância das regras contidas neste termos e condições de uso poderá culminar em demandas judiciais e/ou administrativas em desfavor do USUÁRIO.
""")

load_historico()
window['-HISTORICO-'].update(format_historico())

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    if event == "Buscar":
        search_term = values["-SEARCH-"]
        if not search_term:
            window["-RETORNO-"].update("Insira um valor para a pesquisa.")
        else:
            search_type = "ean" if values["-EAN-"] else "description"
            produto = next((p for p in historico if (p.get("gtin") == search_term if search_type == "ean" else p.get("description") == search_term)), None)
            
            if produto:
                result = format_produto(produto)
                window["-RETORNO-"].update(result)
            else:
                produto = consultar_produto(search_term)
                if produto:
                    result = format_produto(produto)
                    window["-RETORNO-"].update(result)
                else:
                    window["-RETORNO-"].update(f"Produto {search_term} não encontrado.")
        window["-SEARCH-"].update('')

    if event == "-INSTAGRAM-":
        webbrowser.open("https://www.instagram.com/rafaelmoreirafernandes")

    if event == "-WHATSAPP-":
        webbrowser.open("https://wa.me/message/556WDBERNK3MM1")

    if event == "-COPY-":
        clipboard.copy(window["-RETORNO-"].get())

    if event == "-TERMS-":
        open_terms_of_use()

    if event == "-CADASTRO-":
        open_cadastro_produto()

window.close()
