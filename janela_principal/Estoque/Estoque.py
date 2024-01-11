import PySimpleGUI as sg
import os

# Definir o layout da janela
layout = [
    [sg.Button('Cadastrar Produtos')],
    [sg.Button('Código de Barras')],
    [sg.Button('Consultar Produtos')],
    [sg.Button('Controle do Estoque')],
    [sg.Button('Etiquetas')],
    [sg.Button('Relatório de Vendas')],
    [sg.Button('Tabela de Preços')],
]

# Criar a janela
window = sg.Window('Estoque', layout)

# Loop para interação com a janela
while True:
    event, values = window.read()
    if event is None:
        break
    elif event == 'Cadastrar Produtos':
        # Abre a janela do arquivo "Cadastrar Produtos.py"
        arquivo = os.path.join('janela principal', 'Estoque', 'Cadastrar Produtos', 'Cadastrar Produtos.py')
        if os.path.exists(arquivo):
            os.system(f'python "{arquivo}"')
        else:
            sg.popup_error('Arquivo "Cadastrar Produtos.py" não encontrado.')
    elif event == 'Código de Barras':
        # Abre a janela do arquivo "Código de Barras.py"
        arquivo = os.path.join('janela principal', 'Estoque', 'Código de Barras', 'Código de Barras.py')
        if os.path.exists(arquivo):
            os.system(f'python "{arquivo}"')
        else:
            sg.popup_error('Arquivo "Código de Barras.py" não encontrado.')
    elif event == 'Consultar Produtos':
        # Abre a janela do arquivo "Consultar Produtos.py"
        arquivo = os.path.join('janela principal', 'Estoque', 'Consultar Produtos', 'Consultar Produtos.py')
        if os.path.exists(arquivo):
            os.system(f'python "{arquivo}"')
        else:
            sg.popup_error('Arquivo "Consultar Produtos.py" não encontrado.')
    elif event == 'Controle do Estoque':
        # Abre a janela do arquivo "controle_estoque.py"
        arquivo = os.path.join('janela principal', 'Controle_estoque', 'controle_estoque.py')
        if os.path.exists(arquivo):
            os.system(f'python "{arquivo}"')
        else:
            sg.popup_error('Arquivo "controle_estoque.py" não encontrado.')
    elif event == 'Etiquetas':
        # Abre a janela do arquivo "Etiquetas.py"
        arquivo = os.path.join('janela principal', 'Estoque', 'Etiquetas', 'Etiquetas.py')
        if os.path.exists(arquivo):
            os.system(f'python "{arquivo}"')
        else:
            sg.popup_error('Arquivo "Etiquetas.py" não encontrado.')
    elif event == 'Relatório de Vendas':
        # Abre a janela do arquivo "Relatório de Vendas.py"
        arquivo = os.path.join('janela principal', 'Estoque', 'Relatório de Vendas', 'Relatório de Vendas.py')
        if os.path.exists(arquivo):
            os.system(f'python "{arquivo}"')
        else:
            sg.popup_error('Arquivo "Relatório de Vendas.py" não encontrado.')
    elif event == 'Tabela de Preços':
        # Abre a janela do arquivo "Tabela de Preços.py"
        arquivo = os.path.join('janela principal', 'Estoque', 'Tabela de Preços', 'Tabela de Preços.py')
        if os.path.exists(arquivo):
            os.system(f'python "{arquivo}"')
        else:
            sg.popup_error('Arquivo "Tabela de Preços.py" não encontrado.')

# Fechar a janela ao sair do loop
window.close()
