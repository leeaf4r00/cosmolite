import os
import subprocess
import datetime
import PySimpleGUI as sg
import pandas as pd
from fpdf import FPDF

sg.theme('DefaultNoMoreNagging')

relatorios_dir = 'janela_principal/Relatorios/relatorios_controle_fiscais'

layout = [
    [sg.Button('Verificar Transações do Dia Atual')],
    [sg.Button('Verificar Arquivos de Relatório')],
    [sg.Button('Imprimir Relatório em PDF')],
    [sg.Button('Fechar')]
]

window = sg.Window('Imprimir Relatório de Transações', layout)

def criar_pastas():
    if not os.path.exists(relatorios_dir):
        os.makedirs(relatorios_dir)
        os.makedirs(os.path.join(relatorios_dir, 'CSV'))
        os.makedirs(os.path.join(relatorios_dir, 'PDF'))
        os.makedirs(os.path.join(relatorios_dir, 'HTML'))

def gerar_relatorio_csv():
    criar_pastas()
    relatorio_path = os.path.join(relatorios_dir, 'CSV', f'relatorio_{datetime.datetime.now().strftime("%Y%m%d")}.csv')
    transacoes = pd.DataFrame()  # Substitua pelo seu DataFrame de transações
    transacoes.to_csv(relatorio_path, index=False)
    sg.popup('O arquivo CSV do relatório foi salvo e será aberto.', 'Caminho: ' + relatorio_path)
    subprocess.run(['start', relatorio_path], shell=True)

def gerar_relatorio_pdf():
    criar_pastas()

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

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body(f'Total de moedas: {window["total_moedas"].DisplayText}')
    pdf.chapter_body(f'Total de cédulas: {window["total_cedulas"].DisplayText}')
    pdf.chapter_body('Detalhes das Transações:')
    transacoes = pd.DataFrame()  # Substitua pelo seu DataFrame de transações
    for _, transacao in transacoes.iterrows():
        tipo = transacao['Tipo']
        valor = transacao['Valor']
        quantidade = transacao['Quantidade']
        pdf.chapter_body(f'{tipo} - {valor} - Quantidade: {quantidade}')
    relatorio_path = os.path.join(relatorios_dir, 'PDF', f'relatorio_{datetime.datetime.now().strftime("%Y%m%d")}.pdf')
    pdf.output(relatorio_path)
    sg.popup('O arquivo PDF do relatório foi salvo e será aberto.', 'Caminho: ' + relatorio_path)
    subprocess.run(['start', relatorio_path], shell=True)

while True:
    event, _ = window.read()

    if event in (None, 'Fechar'):
        break

    elif event == 'Imprimir Relatório em PDF':
        gerar_relatorio_pdf()

window.close()
