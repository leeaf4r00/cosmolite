import PySimpleGUI as sg

sg.theme('DarkBlue14')

def open_vendas_simplificadas(clientes_cadastrados):
    """
    Abre a janela de vendas Simplificadas.

    Args:
        clientes_cadastrados (list): Lista dos clientes cadastrados.
    """
    layout = [
        [sg.Text('Vendas Simplificadas', font=('Helvetica', 20), justification='center')],
        [sg.Text('Selecione o Cliente:', font=('Helvetica', 14))],
        [sg.Combo(clientes_cadastrados, size=(30, 1), key='-CLIENTE-', readonly=True)],
        [sg.Button('Cadastrar Clientes', key='-CADASTRAR-', font=('Helvetica', 12), size=(15, 1))],
        [sg.Button('Vender', key='-VENDER-', font=('Helvetica', 12), size=(10, 1))],
        [sg.Button('Fechar', font=('Helvetica', 12), size=(10, 1))]
    ]

    window = sg.Window('Vendas Simplificadas', layout)

    while True:
        event, values = window.read()

        if event is None or event == 'Fechar':
            break

        if event == '-CADASTRAR-':
            cadastrar_cliente()

        if event == '-VENDER-':
            cliente_selecionado = values['-CLIENTE-']
            realizar_venda(cliente_selecionado)

    window.close()

def cadastrar_cliente():
    """
    Abre a janela de cadastro de clientes.
    """
    sg.popup('Janela de Cadastro de Clientes')

def realizar_venda(cliente):
    """
    Realiza a venda para o cliente selecionado.

    Args:
        cliente (str): O cliente selecionado.
    """
    sg.popup(f'Venda realizada para o cliente: {cliente}')

if __name__ == '__main__':
    clientes_cadastrados = ['Cliente 1', 'Cliente 2', 'Cliente 3']
    open_vendas_simplificadas(clientes_cadastrados)
