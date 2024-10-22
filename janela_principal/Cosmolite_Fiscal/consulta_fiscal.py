    import os
    import subprocess
    import random
    import PySimpleGUI as sg
    import requests
    import webbrowser
    import clipboard
    import sys

    sg.theme('DarkBlue14')

    # Definir a variável de ambiente ROOT_DIR com o caminho base
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    os.environ["ROOT_DIR"] = ROOT_DIR

    # Obter o diretório "janela_principal" usando a variável de ambiente
    janela_principal_dir = os.path.join(os.environ["ROOT_DIR"], "janela_principal")

    # Adicionar o diretório "janela_principal" ao PYTHONPATH se ainda não estiver presente
    if janela_principal_dir not in sys.path:
        sys.path.append(janela_principal_dir)

    API_DIR = os.path.join(ROOT_DIR, "api")
    HISTORICO_DIR = os.path.join(ROOT_DIR, "historico")
    HISTORICO_FILE = os.path.join(HISTORICO_DIR, "historico_data.txt")
    VENDAS_DIR = os.path.join(ROOT_DIR, "vendas")
    TERMS_DIR = os.path.join(ROOT_DIR, "termos")
    CONTROLE_ESTOQUE_DIR = "janela_principal/Controle_estoque/controle_estoque.py"


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
            sg.Text("Token da API Cosmos:"),
            sg.Text("", size=(30, 1), key="-TOKEN-"),
            sg.Button("Trocar Token Cosmos", key="-CHANGE-TOKEN-")
        ],
        [
            sg.Text("Software Licenciado e Desenvolvido por Rafael Moreira Fernandes | Todos Direitos Reservados ©",
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
            sg.Button("Relatórios Fiscais", font=(
                "Helvetica", 10), key="-RELATORIOS-FISCAIS-"),
            sg.Button("Cadastro de Produto", font=(
                "Helvetica", 10), key="-CADASTRO-")
        ],
        [
            sg.Text("Tenha controle total de seu negócio e acessando as informações de qualquer lugar e a qualquer hora.")
        ],
        [
            sg.Button("TERMOS DE USO", font=(
                "Helvetica", 10, "underline"), key="-TERMS-")
        ],
        [
            sg.Button("Sair", font=("Helvetica", 10),
                    button_color=("white", "red"))
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
        except FileNotFoundError:
            pass


    def save_historico():
        with open(HISTORICO_FILE, 'w') as f:
            for d in historico:
                f.write(str(d) + '\n')


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


    def format_produto(produto):
        formatted_produto = ''
        produto_info = [
            ("Código EAN", "gtin"),
            ("Descrição", "description"),
            ("NCM", "ncm"),
            ("Preço", "price"),
            ("Quantidade", "quantity"),
            ("Preço Médio", "avg_price"),
            ("Marca", "brand.name"),
            ("GPC", "gpc.code - gpc.description"),
            ("Peso Bruto", "gross_weight"),
            ("Altura", "height"),
            ("Comprimento", "length"),
            ("Preço Máximo", "max_price"),
            ("Peso Líquido", "net_weight"),
            ("Imagem", "thumbnail"),
            ("Largura", "width")
        ]

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


    def buscar_produtos(values):
        # Access the user's input directly from the 'values' dictionary
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


    def format_historico(historico):
        return [format_produto(produto) for produto in historico]


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
        # Get the current working directory
        current_dir = os.getcwd()

        # Navigate to the "Controle_estoque" directory relative to the current working directory
        controle_estoque_dir = os.path.join(
            current_dir, "janela_principal", "Controle_estoque")

        # Combine the directory path with the file name
        controle_estoque_path = os.path.join(
            controle_estoque_dir, "controle_estoque.py")

        # Print the full path (optional, for debugging purposes)
        print("Caminho do arquivo:", controle_estoque_path)

        # Check if the file exists and open it
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


    def cadastrar_produto(produto_info):
        # Lógica para cadastrar o produto usando as informações fornecidas
        # Substitua este código pela lógica real de cadastro de produtos
        print("Cadastrando produto:")
        print(produto_info)


    def cadastrar_produto_from_consulta(values):  # Add the 'values' argument
        # Access the user's input directly from the 'values' dictionary
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


    def main():
        check_create_folder(HISTORICO_DIR)
        load_historico()

        window['-HISTORICO-'].update(format_historico(historico))

        event = ""
        values = {}

        while event not in (sg.WINDOW_CLOSED, 'Quit', 'Sair'):
            event, values = window.read()

            if event == "-CADASTRO-":
                open_cadastro_produto()

            if event == "Buscar":
                buscar_produtos(values)

            if event == "-INSTAGRAM-":
                webbrowser.open("https://www.instagram.com/RAFAELMOREIRAFERNANDES")

            if event == "-WHATSAPP-":
                webbrowser.open("https://wa.me/message/556WDBERNK3MM1")

            if event == "-COPY-":
                clipboard.copy(window["-RETORNO-"].get())

            if event == "-TERMS-":
                open_terms_of_use()

            if event == "-CHANGE-TOKEN-":
                change_token()
                window["-TOKEN-"].update(token)

            if event == "-RELATORIOS-FISCAIS-":
                subprocess.Popen(
                    ["python", os.path.join(API_DIR, "relatorios_fiscais.py")])

        save_historico()
        window.close()


    if __name__ == "__main__":
        main()
