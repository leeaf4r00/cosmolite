import PySimpleGUI as sg

# Função para exibir a janela de produtos cadastrados
def exibir_produtos_cadastrados():
    # Dados fictícios de produtos cadastrados (substitua com seus próprios dados)
    produtos = [
        {"nome": "Produto 1", "preco": 10.99},
        {"nome": "Produto 2", "preco": 15.99},
        {"nome": "Produto 3", "preco": 19.99},
        {"nome": "Produto 4", "preco": 8.99},
    ]

    # Cabeçalho da tabela
    header = ["Nome", "Preço"]

    # Converter os dados dos produtos em uma matriz para exibir na tabela
    data = [[produto["nome"], produto["preco"]] for produto in produtos]

    # Definir o layout da janela
    layout = [
        [sg.Table(values=data, headings=header, auto_size_columns=True, justification="center")],
        [sg.Button("Fechar", size=(10, 2), key="-FECHAR-")]
    ]

    # Criar a janela de produtos cadastrados
    window = sg.Window("Produtos Cadastrados", layout)

    # Loop para ler os eventos da janela
    while True:
        event, _ = window.read()

        if event == sg.WINDOW_CLOSED or event == "-FECHAR-":
            break

    # Fechar a janela de produtos cadastrados
    window.close()

# Executar a função para exibir a janela de produtos cadastrados
exibir_produtos_cadastrados()
