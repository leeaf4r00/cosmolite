#janela_principal\Utilitários\contador_moedas_cedulas\contador_moedas.py
import PySimpleGUI as sg
import pandas as pd
from decimal import Decimal
import locale
import subprocess
import datetime
import os

# Definir o layout da janela
layout = [
    [sg.Text('Insira os valores abaixo:')],
    [sg.Text('Tipo:'), sg.Radio('Cédula', 'tipo', key='tipo_cedula', enable_events=True),
     sg.Radio('Moeda', 'tipo', key='tipo_moeda', default=True, enable_events=True)],
    [sg.Text('Valor:'), sg.Combo(['R$2', 'R$5', 'R$10', 'R$20', 'R$50', 'R$100', 'R$200', 'Outro'], key='valor_cedula',
                                 visible=False), sg.Combo(['R$0.05', 'R$0.10', 'R$0.25', 'R$0.50', 'R$1'], key='valor_moeda', visible=True)],
    [sg.Text('Quantidade:'), sg.InputText(key='quantidade')],
    [sg.Button('Adicionar'), sg.Button('Apagar')],
    [sg.Text('')],
    [sg.Text('Relatório')],
    [sg.Text('Total de moedas: R$0.00', key='total_moedas')],
    [sg.Text('Total de cédulas: R$0.00', key='total_cedulas')],
    [sg.Button('Gerar Relatório'), sg.Button('Imprimir Relatórios'), sg.Button('Fechar')],
    [sg.Multiline('', key='relatorio', size=(50, 10), font='Courier')]
]

window = sg.Window('Controle de Moedas e Cédulas', layout)

# Variáveis globais
transacoes = pd.DataFrame(columns=['Tipo', 'Valor', 'Quantidade'])

# Diretório do relatório
relatorios_dir = os.path.join('janela_principal', 'Relatorios', 'Relatorios_controle_moedas')

def criar_pastas():
    # Cria a pasta "Relatorios_controle_moedas" se ainda não existir
    os.makedirs(relatorios_dir, exist_ok=True)

    # Subpastas
    subpastas = ['CSV', 'PDF', 'HTML']
    for subpasta in subpastas:
        subpasta_dir = os.path.join(relatorios_dir, subpasta)
        os.makedirs(subpasta_dir, exist_ok=True)

def validar_valor(valor):
    if isinstance(valor, str):
        if not valor.startswith('R$'):
            sg.popup('Insira um valor válido')
            return None
        try:
            valor_str = valor.replace("R$", "").replace(",", "")
            valor_num = Decimal(locale.atof(valor_str))
        except ValueError:
            sg.popup('Insira um valor válido')
            return None
        return valor_num
    return valor


def validar_quantidade(quantidade):
    try:
        quantidade_num = int(quantidade)
        if quantidade_num <= 0:
            raise ValueError
    except ValueError:
        sg.popup('Insira uma quantidade válida')
        return None
    return quantidade_num


def adicionar_transacao(tipo, valor, quantidade):
    global transacoes
    transacoes = pd.concat([transacoes, pd.DataFrame({'Tipo': [tipo], 'Valor': [valor], 'Quantidade': [quantidade]})],
                           ignore_index=True)


def apagar_transacao():
    global transacoes
    if not transacoes.empty:
        transacoes = transacoes.iloc[:-1]


def calcular_saldo():
    saldo_moedas = Decimal(0)
    saldo_cedulas = Decimal(0)

    for _, transacao in transacoes.iterrows():
        tipo = transacao['Tipo']
        valor = transacao['Valor']
        quantidade = transacao['Quantidade']

        if tipo == 'Moeda':
            saldo_moedas += Decimal(quantidade) * validar_valor(valor)
        elif tipo == 'Cédula':
            valor_numerico = validar_valor(valor)
            saldo_cedulas += valor_numerico * Decimal(quantidade)

    # Converta para string antes de formatar
    saldo_moedas = formatar_valor(str(saldo_moedas))
    # Converta para string antes de formatar
    saldo_cedulas = formatar_valor(str(saldo_cedulas))

    return saldo_moedas, saldo_cedulas


def atualizar_selecao():
    if window['tipo_cedula'].get():
        window['valor_cedula'].update(visible=True)
        window['valor_moeda'].update(visible=False)
    else:
        window['valor_cedula'].update(visible=False)
        window['valor_moeda'].update(visible=True)


def formatar_valor(valor):
    if isinstance(valor, str):
        # Retorna o valor original se for uma string (para o total de cédulas)
        return valor
    return f'R${locale.currency(float(valor), grouping=True)}'


def atualizar_totais():
    saldo_moedas, saldo_cedulas = calcular_saldo()
    window['total_moedas'].update(
        f'Total de moedas: {saldo_moedas}')  # Remova a chamada para formatar_valor()
    window['total_cedulas'].update(
        f'Total de cédulas: {saldo_cedulas}')  # Remova a chamada para formatar_valor()


def gerar_relatorio():
    saldo_moedas, saldo_cedulas = calcular_saldo()
    relatorio = f'Total de moedas: {saldo_moedas}\nTotal de cédulas: {saldo_cedulas}\n\nDetalhes:\n'
    for _, transacao in transacoes.iterrows():
        tipo = transacao['Tipo']
        valor = transacao['Valor']
        quantidade = transacao['Quantidade']
        relatorio += f'{tipo} - {valor} - Quantidade: {quantidade}\n'
    window['relatorio'].update(relatorio)


def limpar_transacoes():
    global transacoes
    transacoes = pd.DataFrame(columns=['Tipo', 'Valor', 'Quantidade'])
    atualizar_totais()


def gerar_relatorio_csv():
    criar_pastas()
    relatorio_path = os.path.join(relatorios_dir, 'CSV', f'relatorio_{datetime.datetime.now().strftime("%Y%m%d")}.csv')
    transacoes.to_csv(relatorio_path, index=False)
    sg.popup('O arquivo CSV do relatório foi salvo e será aberto.', 'Caminho: ' + relatorio_path)
    subprocess.run(['start', relatorio_path], shell=True)


def gerar_relatorio_pdf():
    from fpdf import FPDF

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Relatório de Transações', 0, 1, 'C')

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)

    criar_pastas()
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body(f'Total de moedas: {window["total_moedas"].DisplayText}')
    pdf.chapter_body(
        f'Total de cédulas: {window["total_cedulas"].DisplayText}')
    pdf.chapter_body('Detalhes das Transações:')
    for _, transacao in transacoes.iterrows():
        tipo = transacao['Tipo']
        valor = transacao['Valor']
        quantidade = transacao['Quantidade']
        pdf.chapter_body(f'{tipo} - {valor} - Quantidade: {quantidade}')
    relatorio_path = os.path.join(relatorios_dir, 'PDF', f'relatorio_{datetime.datetime.now().strftime("%Y%m%d")}.pdf')
    pdf.output(relatorio_path)
    sg.popup('O arquivo PDF do relatório foi salvo e será aberto.', 'Caminho: ' + relatorio_path)
    subprocess.run(['start', relatorio_path], shell=True)


def gerar_relatorio_html():
    criar_pastas()
    html = f'''
    <html>
    <head>
        <title>Relatório de Transações</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1 {{
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            h2 {{
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            p {{
                margin-top: 0;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>Resumo das Transações</h1>
        <p>Total de moedas: {window["total_moedas"].get()}</p>
        <p>Total de cédulas: {window["total_cedulas"].get()}</p>
        <h2>Detalhes das Transações</h2>
        <ul>
    '''

    for _, transacao in transacoes.iterrows():
        tipo = transacao['Tipo']
        valor = transacao['Valor']
        quantidade = transacao['Quantidade']
        html += f'<li>{tipo} - {valor} - Quantidade: {quantidade}</li>\n'

    html += '''
        </ul>
    </body>
    </html>
    '''

    relatorio_path = os.path.join(relatorios_dir, 'HTML', f'relatorio_{datetime.datetime.now().strftime("%Y%m%d")}.html')
    with open(relatorio_path, 'w') as file:
        file.write(html)
    sg.popup('O arquivo HTML do relatório foi salvo e será aberto.', 'Caminho: ' + relatorio_path)
    subprocess.run(['start', relatorio_path], shell=True)


# Configurar locale para o formato de moeda do Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

while True:
    event, _ = window.read()

    if event in (None, 'Fechar'):
        break

    if event == 'tipo_cedula' or event == 'tipo_moeda':
        atualizar_selecao()

    elif event == 'Adicionar':
        tipo = 'Moeda' if window['tipo_moeda'].get() else 'Cédula'
        valor = window['valor_moeda'].get() if window['tipo_moeda'].get(
        ) else window['valor_cedula'].get()
        if valor == 'Outro':
            valor = sg.popup_get_text(
                'Insira o valor da cédula:', 'Adicionar Cédula')
            valor = validar_valor('R$' + valor)
        else:
            valor = validar_valor(valor)
        if valor is None:
            continue
        quantidade = validar_quantidade(window['quantidade'].get())
        if quantidade is None:
            continue
        adicionar_transacao(tipo, valor, quantidade)
        atualizar_totais()

    elif event == 'Gerar Relatório':
        gerar_relatorio()

    elif event == 'Apagar':
        apagar_transacao()
        atualizar_totais()

    elif event == 'Novo Caixa':
        limpar_transacoes()

    elif event == 'Imprimir Relatórios':
        file_format = sg.popup_get_text(
            'Selecione o formato do arquivo (CSV, PDF ou HTML):', 'Selecionar Formato')

        if file_format is not None:
            file_format = file_format.lower()

        if file_format == 'csv':
            gerar_relatorio_csv()
        elif file_format == 'pdf':
            gerar_relatorio_pdf()
        elif file_format == 'html':
            gerar_relatorio_html()
        elif file_format is not None:
            sg.popup('Formato inválido. Selecione CSV, PDF ou HTML.')

window.close()
