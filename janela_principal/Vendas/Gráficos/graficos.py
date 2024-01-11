import PySimpleGUI as sg

# Função para exibir a janela de gráficos
def exibir_janela_graficos():
    layout_graficos = [
        [sg.Button("Curva ABC", size=(20, 2), key='-CURVA_ABC-')],
        [sg.Button("Gráficos de Vendas", size=(20, 2), key='-GRAFICOS_VENDAS-')],
        [sg.Button("Análise Anual de Vendas", size=(20, 2), key='-ANALISE_ANUAL-')],
        [sg.Button("Análise Trimestral de Vendas", size=(20, 2), key='-ANALISE_TRIMESTRAL-')],
        [sg.Button("Análise de Todas as Vendas do Mês", size=(20, 2), key='-ANALISE_MENSAL-')],
        [sg.Button("Voltar", size=(20, 2))]
    ]

    window_graficos = sg.Window("Gráficos", layout_graficos, finalize=True)

    while True:
        event, _ = window_graficos.read()

        if event == sg.WINDOW_CLOSED or event == "Voltar":
            break

        if event == '-CURVA_ABC-':
            sg.popup("Exibindo Curva ABC")
        elif event == '-GRAFICOS_VENDAS-':
            sg.popup("Exibindo Gráficos de Vendas")
        elif event == '-ANALISE_ANUAL-':
            sg.popup("Exibindo Análise Anual de Vendas")
        elif event == '-ANALISE_TRIMESTRAL-':
            sg.popup("Exibindo Análise Trimestral de Vendas")
        elif event == '-ANALISE_MENSAL-':
            sg.popup("Exibindo Análise de Todas as Vendas do Mês")

    window_graficos.close()

# Função para abrir a janela principal
def abrir_janela_principal():
    sg.theme('DefaultNoMoreNagging')

    layout_principal = [
        [sg.Text("COSMOLITE - V.1.0 - Janela Principal", font=("Helvetica", 18, 'bold'), justification='center')],
        [sg.Button("Cadastro de Produtos"), sg.Button("Venda de Produtos"), sg.Button("Vendas PDV"), sg.Button("Vendas Detalhadas")],
        [sg.Button("Vendas Simplificadas"), sg.Button("Consultar Produtos"), sg.Button("Produtos Cadastrados"), sg.Button("Consultar Produtos Fiscais")],
        [sg.Button("Consultar Vendedores"), sg.Button("Relatório de Vendas"), sg.Button("Gráficos"), sg.Button("Informações Fiscais")],
        [sg.Button("Vendas"), sg.Button("Preferências"), sg.Button("Sair")],
        [sg.Text("Desenvolvido por Rafael Moreira Fernandes | Todos os Direitos Reservados.")]
    ]

    window_principal = sg.Window("Sistema Fiscal", layout_principal, finalize=True)

    while True:
        event, _ = window_principal.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == "Gráficos":
            exibir_janela_graficos()

    window_principal.close()

abrir_janela_principal()
