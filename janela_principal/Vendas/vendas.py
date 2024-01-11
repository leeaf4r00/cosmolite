import PySimpleGUI as sg
import subprocess


def abrir_ponto_de_venda():
    opcoes = ['PDV', 'Detalhado', 'Simplificadas']
    layout = [
        [sg.Text('Qual ponto de venda você vai utilizar?')],
        [sg.Combo(opcoes, default_value=opcoes[0], size=(20, 1),
                  key='-PONTO_VENDA-', enable_events=True)],
        [sg.Button('OK')]
    ]
    window = sg.Window('Ponto de Venda', layout)

    while True:
        event, values = window.read()
        if event == '-PONTO_VENDA-' or event == 'OK':
            escolha = values['-PONTO_VENDA-']
            if escolha == 'PDV':
                subprocess.Popen(["python", "vendas/pdv.py"])
            elif escolha == 'Detalhado':
                subprocess.Popen(["python", "vendas/vendas_detalhadas.py"])
            elif escolha == 'Simplificadas':
                subprocess.Popen(["python", "vendas/vendas_simplificadas.py"])
            break
        if event is None or not window:
            break

    window.close()


# ... defina as outras funções de abertura de janela de acordo com as opções


def exibir_opcoes(tema):
    # Definir o tema
    sg.theme(tema)

    # Definir o layout da janela
    layout = [
        [sg.Text('Selecione uma opção:', font=(
            'Helvetica', 14), justification='center')],
        [sg.Button("Ponto de Venda", size=(20, 2))],
        [sg.Button("Listagem de Vendas", size=(20, 2))],
        [sg.Button("Orçamentos", size=(20, 2))],
        [sg.Button("Devolução", size=(20, 2))],
        [sg.Button("Cadastrar Produto", size=(20, 2))],
        [sg.Button("Gráficos", size=(20, 2))],
        [sg.Button("Comissão de Vendedores", size=(20, 2))],
        [sg.Button("Consignação", size=(20, 2))],
        [sg.Button("NFe PDF - Exportar e Salvar as notas fiscais emitidas e salvar Nota Fiscal Eletronica em PDF", size=(20, 2))],
        [sg.Button("NFE XML - Exportar arquivos XML", size=(20, 2))],
        [sg.Button("Relatório de Vendas", size=(20, 2))]
    ]

    # Criar a janela
    window = sg.Window('Vendas', layout)

    # Mapeie os eventos para as respectivas funções
    event_mapping = {
        'Ponto de Venda': abrir_ponto_de_venda,
        # ... mapeie os outros eventos para as respectivas funções
    }

    # Loop para interação com a janela
    while True:
        event, values = window.read()
        if event is None:
            break
        if event in event_mapping:
            event_mapping[event]()

    # Fechar a janela ao sair do loop
    window.close()


# Chamar a função para exibir as opções de vendas
tema = 'DarkBlue14'  # Defina o tema padrão
exibir_opcoes(tema)
