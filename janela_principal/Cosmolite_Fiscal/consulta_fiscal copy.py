import os
import subprocess
from PySimpleGUI import PySimpleGUI as sg

# Definir constantes e variáveis
API_URL = 'https://api.cosmos.bluesoft.com.br/gtins/'
API_HEADERS = {
    'X-Cosmos-Token': 'UJTBhybMZx96n33FzUfp2w',
}
HISTORICO_DIR = os.path.join(os.environ["ROOT_DIR"], "historico")

def load_historico():
    try:
        with open(HISTORICO_FILE, 'r') as f:
            historico_data = [line.strip() for line in f.readlines()]
            historico = [eval(d) for d in historico_data]
    except FileNotFoundError:
        pass

def save_historico():
    with open(HISTORICO_FILE, 'w') as f:
        for d in historico:
            f.write(str(d) + '\n')

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


def cadastrar_produto(produto_info):
    # Cadastrando o produto
    print("Cadastrando produto:")
    print(produto_info)


def main():
    check_create_folder(HISTORICO_DIR)
    load_historico()

    window['-HISTORICO-'].update(format_historico(historico))

    event = ""
    values = {}

    while True:
        event, values = sg.Window("Consulta de Produto", layout).read()
        if event == "-CADASTRO-":
            open_cadastro_produto()

        if event == "Buscar":
            buscar_produtos(values)

        # Outros eventos
        if event == "-INSTAGRAM-":
            webbrowser.open("https://www.instagram.com/RAFAELMOREIRAFERNANDES")

        if event == "-WHATSAPP-":
            webbrowser.open("https://wa.me/message/556WDBERNK3MM1")

        # Botões de ação
        if event == "-COPY-":
            clipboard.copy(window["-RETORNO-"].get())

        if event == "-TERMS-":
            open_terms_of_use()

        if event == "-Sair":
            break

    save_historico()
    window.close()


def format_produto(produto):
    formatted_produto = ''
    produto_info = get_produto_info(produto)

    for label, attribute_path in produto_info:
        attributes = attribute_path.split('.')
        value = produto
        for attribute in attributes:
            value = value.get(attribute)
            if not value:
                break

        if value:
            formatted_produto += f"{label}: {value}\n"

    url = produto.get("url")
    if url:
        formatted_produto = f'<a href="{url}" style="text-decoration: none; color: inherit;">{formatted_produto}</a>'

    return formatted_produto


def cadastrar_produto_from_consulta(values):
    # Cadastrando o produto usando as informações fornecidas
    search_term = values["-SEARCH-"]
    if not search_term:
        window["-RETORNO-"].update("Insira um valor para a pesquisa.")
    else:
        if values["-EAN-"]:
            search_type = "gtin"
        else:
            search_type = "description"

        produto = next((p for p in historico if p.get(
            search_type) == search_term), None)

        if produto:
            result = format_produto(produto)
            window["-RETORNO-"].update(result)
            save_historico()
            window["-HISTORICO-"].update(format_historico(historico))

            # Obter as informações do produto consultado
            produto_info = get_produto_info(produto)

            # Usar as informações para cadastrar o produto
            cadastrar_produto(produto_info)
        else:
            produto = consultar_produto(search_term)
            if produto:
                result = format_produto(produto)
                window["-RETORNO-"].update(result)
                save_historico()
                window["-HISTORICO-"].update(format_historico(historico))

                # Obter as informações do produto consultado
                produto_info = get_produto_info(produto)

                # Usar as informações para cadastrar o produto
                cadastrar_produto(produto_info)
            else:
                window["-RETORNO-"].update(
                    f"Produto {search_term} não encontrado.")
    window["-SEARCH-"].update('')


def open_cadastro_produto():
    global token

    # Obter a caminho do diretório "janela_principal"
    current_dir = os.getcwd()

    # Obter o caminho relativo para o arquivo "controle_estoque.py" no diretório atual
    controle_estoque_dir = os.path.join(
        current_dir, "janela_principal", "Controle_estoque")

    # Obter a caminho do arquivo "controle_estoque.py"
    controle_estoque_path = os.path.join(
        controle_estoque_dir, "controle_estoque.py")

    # Print o caminho para testes
    print("Caminho de teste:", controle_estoque_path)

    # Verificar se o arquivo está presente
    if not os.path.exists(controle_estoque_path):
        print("Arquivo 'controle_estoque.py' não encontrado.")
    else:
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


if __name__ == "__main__":
    main()
