import os
import webbrowser
import json
import subprocess
import PySimpleGUI as sg
import themes
from typing import List, Tuple

# Constantes
KEYS_FILE = "keys.json"
IMAGES_DIR = "images"
ERROR_FILE_NOT_FOUND = "Arquivo de chaves não encontrado!"
ERROR_INVALID_KEY = "Chave de segurança inválida!"


class TelaSegurancaApp:
    """Aplicativo da Tela de Segurança"""

    def __init__(self):
        """Inicializa a janela e configurações"""
        if os.name == "nt":
            default_theme = themes.THEMES["Padrão"]
        else:
            default_theme = themes.THEMES["Azul Escuro"]
        sg.theme(default_theme)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.keys_file = os.path.join(current_dir, KEYS_FILE)
        self.images_dir = os.path.join(current_dir, IMAGES_DIR)

        self.layout = [
            [sg.Image(
                filename=os.path.join(self.images_dir, "cosmolite.png"),
                size=(300, 300),
                key="-IMAGE-",
                background_color="#f0f0f0",
                pad=(0, 20),
            )],
            [
                sg.Column([
                    [sg.Text("COSMOLITE 1.0", font=("Helvetica", 20),
                             justification="center", pad=((40, 40), (0, 40)))],
                    [sg.Text("Seja bem-vindo! Vamos iniciar seu primeiro acesso!",
                             font=("Helvetica", 16), justification="center")],
                    [sg.Text("Chave de Segurança", size=(15, 1),
                             justification="center")],
                    [sg.Input(key="-security_key-", size=(30, 1), font=("Helvetica", 14),
                              password_char="*")],
                    [sg.Button("Confirmar", size=(15, 1), pad=(10, 10),
                               button_color=(sg.GREENS[0], sg.GREENS[1]), key="-CONFIRM-")],
                    [sg.Text("Sistema Cosmolite Versão 1.0",
                             font=("Helvetica", 10), justification="center", pad=(10, 0))],
                    [sg.Text("Software Licenciado e Desenvolvido por Rafael Moreira Fernandes | Todos Direitos Reservados ©.",
                             font=("Helvetica", 10), justification="center", pad=(10, 0))],
                    [sg.Text("Caso você não tenha uma chave de segurança, adquira uma!",
                             font=("Helvetica", 10), justification="center", pad=(10, 0), text_color="blue", enable_events=True, key="-LINK-")],
                    [sg.Button("Abrir WhatsApp", font=("Helvetica", 10), size=(
                        18, 1), pad=(10, 0), key="-WHATSAPP-", button_color=(sg.GREENS[0], sg.GREENS[1]))],
                ], element_justification="center")
            ],
        ]

        self.window = None

    def create_window(self):
        """Cria a janela"""
        self.window = sg.Window(
            "Tela de Segurança", self.layout, element_justification="center", finalize=True
        )

    def load_keys_data(self) -> List[dict]:
        """Carrega os dados das chaves a partir do arquivo JSON"""
        if not os.path.exists(self.keys_file):
            sg.popup_error(ERROR_FILE_NOT_FOUND)
            return []

        with open(self.keys_file, encoding="utf-8") as keys_file:
            keys_data = json.load(keys_file)

        keys = keys_data.get("keys", [])
        return keys

    def validate_security_key(self, security_key: str, keys: List[dict]) -> Tuple[str, List[str]]:
        """Valida a chave de segurança"""
        for key in keys:
            if key.get("key") == security_key:
                return key.get("type"), key.get("files")

        raise KeyError(ERROR_INVALID_KEY)

    def handle_confirm_event(self, values):
        """Lida com o evento de confirmação"""
        security_key = values["-security_key-"]
        keys = self.load_keys_data()

        for key in keys:
            if key.get("key") == security_key:
                return key.get("type"), key.get("files")

        if not security_key:
            sg.popup_error("Digite uma chave de segurança!")
        else:
            sg.popup_error("Chave de Segurança Inválida! Adquira uma!")

        return None, None

    def handle_login_event(self, keys):
        """Lida com o evento de login"""
        # Implemente a lógica para lidar com o evento de login aqui
        # Certifique-se de retornar o tipo de programa e os arquivos corretos
        program_type = "cadastro"
        program_files = ["arquivo1.py", "arquivo2.py"]
        return program_type, program_files

    def handle_confirm_button(self, values):
        """Lida com o evento de clique no botão 'Confirmar'"""
        program_type, program_files = self.handle_confirm_event(values)

        if program_type and program_files:
            for file in program_files:
                if not os.path.isfile(file):
                    sg.popup_error(f"Arquivo '{file}' não encontrado!")
                    return
            subprocess.run(["python"] + program_files, check=True)

    def handle_whatsapp_button(self):
        """Lida com o evento de clique no botão 'Abrir WhatsApp'"""
        webbrowser.open_new_tab("https://wa.me/message/556WDBERNK3MM1")

    def run(self):
        """Executa o aplicativo"""
        self.create_window()

        while True:
            event, values = self.window.read()

            if event is None:
                break

            if event == "-LINK-":
                webbrowser.open_new_tab("https://www.example.com")

            if event == "-CONFIRM-":
                self.handle_confirm_button(values)

            if event == "-WHATSAPP-":
                self.handle_whatsapp_button()

        self.window.close()


def main():
    """Função principal"""
    app = TelaSegurancaApp()
    app.run()


if __name__ == "__main__":
    main()
