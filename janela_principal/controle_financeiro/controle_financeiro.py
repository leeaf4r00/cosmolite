from datetime import datetime
import csv
import os
import pandas as pd


class DadosInvalidosError(Exception):
    """Exceção levantada quando os dados são inválidos."""

    pass


class ArquivoNaoEncontradoError(Exception):
    """Exceção levantada quando o arquivo não é encontrado."""

    pass


class ErroLeituraCSVError(Exception):
    """Exceção levantada quando ocorre um erro na leitura do arquivo CSV."""

    pass


class RelatorioFinanceiro:
    """Classe responsável por ler um arquivo CSV de relatório financeiro e realizar exportações."""

    def __init__(self):
        self.caminho_relatorios = "Relatorios/Relatorios_controle_financeiro"
        self.criar_pastas()
        self.dados = None

    def criar_pastas(self):
        """Cria as pastas necessárias para os relatórios, se não existirem."""
        if not os.path.exists(self.caminho_relatorios):
            os.makedirs(self.caminho_relatorios)

    def exportar_excel(self, data, nome_arquivo):
        """Exporta os dados para um arquivo Excel."""
        self.criar_pastas()
        df = pd.DataFrame(data)
        df.to_excel(nome_arquivo, index=False)
        print(f"Dados exportados para o arquivo Excel: {nome_arquivo}")

    def exportar_html(self, data, nome_arquivo):
        """Exporta os dados para um arquivo HTML."""
        self.criar_pastas()
        df = pd.DataFrame(data)
        df.to_html(nome_arquivo, index=False)
        print(f"Dados exportados para o arquivo HTML: {nome_arquivo}")

    def exportar_pdf(self, data, nome_arquivo):
        """Exporta os dados para um arquivo PDF."""
        self.criar_pastas()
        df = pd.DataFrame(data)

        html = df.to_html(index=False)

        def convert_html_to_pdf(html, output_path):
            with open(output_path, "wb") as output_file:
                pisa_status = pisa.CreatePDF(html, dest=output_file)
            return pisa_status.err

        convert_html_to_pdf(html, nome_arquivo)
        print(f"Dados exportados para o arquivo PDF: {nome_arquivo}")

    def exportar_csv(self, data, nome_arquivo):
        """Exporta os dados para um arquivo CSV."""
        self.criar_pastas()
        df = pd.DataFrame(data)
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
            raise ArquivoNaoEncontradoError("Arquivo CSV não encontrado.")
        except csv.Error:
            raise ErroLeituraCSVError("Erro ao ler o arquivo CSV.")

    def validar_dados(self, data):
        """Realiza validações nos dados antes da exportação."""
        if not data:
            raise DadosInvalidosError("Dados inválidos: nenhum dado encontrado.")
        # Realize outras validações conforme necessário

    def exportar_dados(self, export_type, nome_arquivo=None):
        """Exporta os dados para o formato especificado."""
        try:
            self.validar_dados(self.dados)

            if nome_arquivo is None:
                nome_arquivo = f"{self.caminho_relatorios}/{self.get_data_atual()}.{export_type.lower()}"

            if export_type == "Excel":
                self.exportar_excel(self.dados, nome_arquivo)
            elif export_type == "HTML":
                self.exportar_html(self.dados, nome_arquivo)
            elif export_type == "PDF":
                self.exportar_pdf(self.dados, nome_arquivo)
            elif export_type == "CSV":
                self.exportar_csv(self.dados, nome_arquivo)

            print("Exportação concluída.")
        except DadosInvalidosError as e:
            print(f"Erro ao exportar os dados: {str(e)}")
        except ArquivoNaoEncontradoError as e:
            print(f"Erro ao ler o arquivo CSV: {str(e)}")
        except ErroLeituraCSVError as e:
            print(f"Erro ao ler o arquivo CSV: {str(e)}")


if __name__ == "__main__":
    relatorio = RelatorioFinanceiro()
    relatorio.dados = relatorio.ler_arquivo_csv("dados.csv")
    relatorio.exportar_dados("CSV")
