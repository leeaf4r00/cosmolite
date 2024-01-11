import PySimpleGUI as sg
from pathlib import Path

def find_relative_path(file_path: str) -> str:
    current_dir = Path.cwd()
    try:
        relative_path = Path(file_path).relative_to(current_dir)
    except ValueError:
        return "Não encontrado"
    return str(relative_path)

def delete_file(file_path: str) -> bool:
    try:
        path = Path(file_path)
        if path.exists() and path.is_file():
            path.unlink()
            return True
        return False
    except Exception as e:
        print(f"Erro ao apagar o arquivo: {e}")
        return False

class GUI:
    def __init__(self):
        sg.theme('DefaultNoMoreNagging')
        self.found_files = set()
        self.layout = [
            [sg.Text("Selecione o(s) arquivo(s) que deseja encontrar:")],
            [sg.Input(key='-FILE-', size=(40, 1)), sg.FilesBrowse()],
            [sg.Button('Procurar'), sg.Button('Apagar'), sg.Button('Limpar'), sg.Button('Sair')],
            [sg.Output(size=(60, 10))]
        ]
        self.window = sg.Window('Encontrar e Apagar Arquivo', self.layout)
        self.last_path = ""

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WINDOW_CLOSED or event == 'Sair':
                break

            file_paths = values['-FILE-'].split(';')
            for file_path in file_paths:
                relative_path = find_relative_path(file_path)

                if event == 'Procurar':
                    if relative_path not in self.found_files:
                        self.found_files.add(relative_path)
                    print(f"O arquivo '{Path(file_path).name}' está na pasta de caminho relativo: {relative_path}")

                elif event == 'Apagar':
                    if delete_file(file_path):
                        self.found_files.remove(relative_path)
                        print(f"O arquivo '{Path(file_path).name}' foi apagado.")

                elif event == 'Limpar':
                    self.found_files.clear()
                    print("Lista de arquivos encontrados foi limpa.")

                self.last_path = file_path

        self.window.close()

if __name__ == '__main__':
    gui = GUI()
    gui.run()
