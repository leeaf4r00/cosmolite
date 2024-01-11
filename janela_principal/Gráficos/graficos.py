import PySimpleGUI as sg
import subprocess


def open_file(file_name):
    subprocess.Popen(['python', file_name])


# Definição do layout da janela principal
layout = [
    [sg.Button('Análise Anual de Vendas', size=(20, 2), key='btn_anual')],
    [sg.Button('Análise Trimestral de Vendas',
               size=(20, 2), key='btn_trimestral')],
    [sg.Button('Análise de Todas as Vendas do Mês',
               size=(20, 2), key='btn_todas')],
    [sg.Button('Curva ABC', size=(20, 2), key='btn_curva')],
    [sg.Button('Gráfico de Vendas', size=(20, 2), key='btn_grafico')]
]

# Criação da janela principal
window = sg.Window('Gráficos', layout,
                   element_justification='center', finalize=True)

# Loop para capturar eventos da janela principal
while True:
    event, _ = window.read()
    if event is None:
        break
    elif event == 'btn_anual':
        open_file('Análise Anual de Vendas.py')
    elif event == 'btn_trimestral':
        open_file('Análise Trimestral de Vendas.py')
    elif event == 'btn_todas':
        open_file('Análise de Todas as Vendas do Mês.py')
    elif event == 'btn_curva':
        open_file('Curva ABC.py')
    elif event == 'btn_grafico':
        open_file('Gráfico de Vendas.py')

    # Criação da janela para exibir o arquivo correspondente
    layout_file = [
        [sg.Text(f'Exibindo: {event}')],
        [sg.Button('Fechar')]
    ]

    window_file = sg.Window(
        event, layout_file, element_justification='center', finalize=True)

    # Loop para capturar eventos da janela do arquivo correspondente
    while True:
        event_file, _ = window_file.read()
        if event_file is None or event_file == 'Fechar':
            break

    # Fechamento da janela do arquivo correspondente
    window_file.close()

# Fechamento da janela principal
window.close()
