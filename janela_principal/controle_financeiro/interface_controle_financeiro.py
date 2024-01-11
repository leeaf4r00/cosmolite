import PySimpleGUI as sg
from relatorio_financeiro import RelatorioFinanceiro

class InterfaceControleFinanceiro:
    def __init__(self):
        self.relatorio = RelatorioFinanceiro()
        self.layout = [
            [sg.Text("Selecione o arquivo CSV: "), sg.Input(), sg.FileBrowse(key="-FILE-")],
            [sg.Text("Selecione o tipo de exportação:"),
             sg.Combo(["Excel", "HTML", "PDF", "CSV"], default_value="Excel", key="-EXPORT-TYPE-")],
            [sg.Text("Digite o nome do arquivo de saída: "), sg.InputText(key="-OUTPUT-")],
            [sg.Button('Exportar')]
        ]
        self.window = sg.Window('Controle Financeiro', self.layout)

    def run(self):
        while True:
            event, values = self.window.read()
            if event is None:
                break
            elif event == 'Exportar':
                nome_arquivo = values["-FILE-"]
                export_type = values["-EXPORT-TYPE-"]
                output_name = values["-OUTPUT-"]
                self.relatorio.ler_arquivo_csv(nome_arquivo)
                self.relatorio.exportar_dados(export_type, output_name)
        self.window.close()

if __name__ == "__main__":
    interface = InterfaceControleFinanceiro()
    interface.run()
