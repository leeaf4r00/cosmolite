import PySimpleGUI as sg
import pandas as pd
import os
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime
import csv

class RelatorioFinanceiroCsv:
    """Classe responsável por ler um arquivo CSV de relatório financeiro e realizar exportações."""

    def __init__(self):
        self.caminho_relatorios = "janela_principal/Relatorios/Relatorios_controle_financeiro"
        self.criar_pastas()

    def criar_pastas(self):
        """Cria as pastas necessárias para os relatórios, se não existirem."""
        if not os.path.exists(self.caminho_relatorios):
            os.makedirs(self.caminho_relatorios)

    def exportar_excel(self, data):
        """Exporta os dados para um arquivo Excel."""
        self.criar_pastas()
        df = pd.DataFrame(data)
        nome_arquivo = f"{self.caminho_relatorios}/controlefinanceiro_{self.get_data_atual()}.xlsx"
        df.to_excel(nome_arquivo, index=False)
        print(f"Dados exportados para o arquivo Excel: {nome_arquivo}")

    def exportar_html(self, data):
        """Exporta os dados para um arquivo HTML."""
        self.criar_pastas()
        df = pd.DataFrame(data)
        nome_arquivo = f"{self.caminho_relatorios}/controlefinanceiro_{self.get_data_atual()}.html"
        df.to_html(nome_arquivo, index=False)
        print(f"Dados exportados para o arquivo HTML: {nome_arquivo}")

    def exportar_pdf(self, data):
        """Exporta os dados para um arquivo PDF."""
        self.criar_pastas()
        df = pd.DataFrame(data)
        nome_arquivo = f"{self.caminho_relatorios}/controlefinanceiro_{self.get_data_atual()}.pdf"

        html = df.to_html(index=False)

        def convert_html_to_pdf(html, output_path):
            with open(output_path, "wb") as output_file:
                pisa_status = pisa.CreatePDF(html, dest=output_file)
            return pisa_status.err

        convert_html_to_pdf(html, nome_arquivo)
        print(f"Dados exportados para o arquivo PDF: {nome_arquivo}")

    def exportar_csv(self, data):
        """Exporta os dados para um arquivo CSV."""
        self.criar_pastas()
        df = pd.DataFrame(data)
        nome_arquivo = f"{self.caminho_relatorios}/controlefinanceiro_{self.get_data_atual()}.csv"
        df.to_csv(nome_arquivo, index=False)
        print(f"Dados exportados para o arquivo CSV: {nome_arquivo}")

    def get_data_atual(self):
        """Retorna a data e hora atual no formato 'DDMMYYYY_HHMM'."""
        data_atual = datetime.now().strftime("%d%m%Y_%H%M")
        return data_atual

    def ler_arquivo_csv(self, nome_arquivo):
        """Lê o arquivo CSV de relatório financeiro e retorna os dados como um dicionário."""
        try:
            with open(nome_arquivo, "r", newline="") as file:
                reader = csv.DictReader(file)
                data = {}
                for row in reader:
                    section = row.get("Seção")
                    if section in data:
                        data[section].append(row)
                    else:
                        data[section] = [row]
                return data
        except FileNotFoundError:
            sg.popup_error("Arquivo CSV não encontrado.")
            return None
        except csv.Error:
            sg.popup_error("Erro ao ler o arquivo CSV.")
            return None

relatorio = RelatorioFinanceiroCsv()

layout = [
    [sg.Text("Selecione o arquivo CSV: "), sg.Input(), sg.FileBrowse(key="-FILE-")],
    [sg.Text("Selecione o tipo de exportação:"),
     sg.Combo(["Excel", "HTML", "PDF", "CSV"], default_value="Excel", key="-EXPORT-TYPE-")],
    [sg.Button('Exportar')]
]

window = sg.Window('Controle Financeiro', layout)

while True:
    event, values = window.read()
    if event is None:
        break
    elif event == 'Exportar':
        nome_arquivo = values["-FILE-"]
        export_type = values["-EXPORT-TYPE-"]
        dados = relatorio.ler_arquivo_csv(nome_arquivo)
        if dados is not None:
            if export_type == "Excel":
                relatorio.exportar_excel(dados)
            elif export_type == "HTML":
                relatorio.exportar_html(dados)
            elif export_type == "PDF":
                relatorio.exportar_pdf(dados)
            elif export_type == "CSV":
                relatorio.exportar_csv(dados)

window.close()
