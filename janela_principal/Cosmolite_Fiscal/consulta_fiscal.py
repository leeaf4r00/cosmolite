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
            [],
            size=(80, 10),
            key="-HISTORICO-",
            font=("Helvetica", 10),
            enable_events=True,
            auto_size_text=True
        )
    ],
    [
        sg.Text("Software Licenciado e Produzido por Rafael Fernandes, Rurópolis-Pará",
                font=("Helvetica", 10, "underline"),
                text_color="white",
                background_color="red")
    ],
    [
        sg.Button(
            "Instagram",
            font=("Helvetica", 10, "underline"),
            button_color=("white", "purple"),
            key="-INSTAGRAM-"
        ),
        sg.Button(
            "Whatsapp",
            font=("Helvetica", 10, "underline"),
            button_color=("white", "green"),
            key="-WHATSAPP-"
        ),
        sg.Button("Copiar resultado", font=("Helvetica", 10), key="-COPY-"),
        sg.Button("Cadastro de Produto", font=(
            "Helvetica", 10), key="-CADASTRO-")
    ],
    [
        sg.Text("Tenha controle total de seu negócio e acessando as informações de qualquer lugar e a qualquer hora.")
    ],
    [
        sg.Button("TERMOS DE USO", font=(
            "Helvetica", 10, "underline"), key="-TERMS-")
    ]
]

window = sg.Window("Consulta de Produto", layout, size=(
    800, 600), resizable=True, finalize=True)

API_URL = 'https://api.cosmos.bluesoft.com.br/gtins/'
API_HEADERS = {
    'X-Cosmos-Token': 'UJTBhybMZx96n33FzUfp2w',
    'User-Agent': 'API Request'
}

historico = []


def consultar_produto(gtin):
    produto = None

    try:
        r = requests.get(f'{API_URL}{gtin}.json', headers=API_HEADERS)
        r.raise_for_status()
        resultado = r.json()
        historico.append(resultado)
        produto = resultado
    except requests.exceptions.RequestException as e:
        sg.popup_error(f'Erro ao consultar o produto: {str(e)}')

    return produto


def save_historico():
    with open('historico.txt', 'w') as f:
        for d in historico:
            f.write(str(d) + '\n')


def load_historico():
    global historico
    try:
        with open('historico.txt', 'r') as f:
            historico_data = [line.strip() for line in f.readlines()]
            historico = [eval(d) for d in historico_data]
    except FileNotFoundError:
        pass


def format_produto(produto):
    ean = produto.get("gtin")
    description = produto.get("description")
    ncm = produto.get("ncm")
    price = produto.get("price")
    quantity = produto.get("quantity")
    url = produto.get("url")
    avg_price = produto.get("avg_price")
    brand = produto.get("brand")
    gpc = produto.get("gpc")
    gross_weight = produto.get("gross_weight")
    height = produto.get("height")
    length = produto.get("length")
    max_price = produto.get("max_price")
    net_weight = produto.get("net_weight")
    thumbnail = produto.get("thumbnail")
    width = produto.get("width")

    formatted_produto = f"Código EAN: {ean}\nDescrição: {description}\nNCM: {ncm}\nPreço: {price}\nQuantidade: {quantity}\n"

    if avg_price:
        formatted_produto += f"Preço Médio: {avg_price}\n"

    if brand:
        brand_name = brand.get("name")
        formatted_produto += f"Marca: {brand_name}\n"

    if gpc:
        gpc_code = gpc.get("code")
        gpc_description = gpc.get("description")
        formatted_produto += f"GPC: {gpc_code} - {gpc_description}\n"

    if gross_weight:
        formatted_produto += f"Peso Bruto: {gross_weight} g\n"

    if height:
        formatted_produto += f"Altura: {height} cm\n"

    if length:
        formatted_produto += f"Comprimento: {length} cm\n"

    if max_price:
        formatted_produto += f"Preço Máximo: {max_price}\n"

    if net_weight:
        formatted_produto += f"Peso Líquido: {net_weight} g\n"

    if thumbnail:
        formatted_produto += f"Imagem: {thumbnail}\n"

    if width:
        formatted_produto += f"Largura: {width} cm\n"

    if url:
        formatted_produto = f'<a href="{url}" style="text-decoration: none; color: inherit;">{formatted_produto}</a>'

    return formatted_produto


def format_historico(historico):
    formatted_history = []
    for produto in historico:
        formatted_produto = format_produto(produto)
        formatted_history.append(formatted_produto)

    return formatted_history


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
        event, values = error_window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-COPY-":
            clipboard.copy(error_message)
    error_window.close()


def open_cadastro_produto():
    subprocess.Popen(["python", "cadastro_produto.py"])


def open_terms_of_use():
    sg.popup("""
Termos de Uso:
A RR SISTEMAS não se responsabiliza pela utilização das informações tributárias do programa Cosmos.

Antes da coleta e utilização de qualquer informação e dados pessoais, o USUÁRIO da Cosmos deverá:

a) somente coletar dados pessoais se o motivo estiver fundamentado em uma das bases legais previstas no artigo 7º da Lei nº 13.709/2018, que trata da Lei Geral de Proteção de Dados (LGPD);

b) obter a aprovação de um contador que se responsabilize legalmente pela classificação das informações tributárias inseridas na plataforma.

A inobservância das regras contidas neste termos e condições de uso poderá culminar em demandas judiciais e/ou administrativas em desfavor do USUÁRIO.
""")


def save_historico():
    with open('historico.txt', 'w') as f:
        for d in historico:
            f.write(str(d) + '\n')


def load_historico():
    global historico
    try:
        with open('historico.txt', 'r') as f:
            historico_data = [line.strip() for line in f.readlines()]
            historico = [eval(d) for d in historico_data]
    except FileNotFoundError:
        pass


load_historico()

window['-HISTORICO-'].update(format_historico(historico))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    if event == "Buscar":
        search_term = values["-SEARCH-"]
        if not search_term:
            window["-RETORNO-"].update("Insira um valor para a pesquisa.")
        else:
            if values["-EAN-"]:
                search_type = "ean"
            else:
                search_type = "description"

            produto = None
            for p in historico:
                if search_type == "ean" and p.get("gtin") == search_term:
                    produto = p
                    break
                elif search_type == "description" and p.get("description") == search_term:
                    produto = p
                    break

            if produto:
                result = format_produto(produto)
                window["-RETORNO-"].update(result)
                save_historico()
                window["-HISTORICO-"].update(format_historico(historico))
            else:
                produto = consultar_produto(search_term)
                if produto:
                    result = format_produto(produto)
                    window["-RETORNO-"].update(result)
                    save_historico()
                    window["-HISTORICO-"].update(format_historico(historico))
                else:
                    window["-RETORNO-"].update(
                        f"Produto {search_term} não encontrado."
                    )
        window["-SEARCH-"].update('')

    if event == "-INSTAGRAM-":
        webbrowser.open("https://www.instagram.com/RAFAELMOREIRAFERNANDES")

    if event == "-WHATSAPP-":
        webbrowser.open("https://wa.me/message/556WDBERNK3MM1")

    if event == "-COPY-":
        clipboard.copy(window["-RETORNO-"].get())

    if event == "-TERMS-":
        open_terms_of_use()

    if event == "-CADASTRO-":
        open_cadastro_produto()

window.close()
