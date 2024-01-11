# interface_grafica.py
import PySimpleGUI as sg

# Constantes para textos exibidos
WELCOME_MESSAGE = "Bem-vindo ao Cosmolite"
FIRST_ACCESS_MESSAGE = "Digite sua Chave de segurança para o primeiro acesso"
LOGIN_MESSAGE = "Faça o login"
LOGIN_BUTTON_TEXT = "Login"
SECURITY_BUTTON_TEXT = "Digite sua Chave de segurança"
EXIT_BUTTON_TEXT = "Sair"

def show_tela_seguranca_open_popup():
    sg.popup("Janela de tela_seguranca já está aberta!")

def show_tela_seguranca_error_popup(error):
    sg.popup(f"Erro ao abrir o arquivo tela_seguranca.py: {error}")

def show_janela_principal_error_popup(error):
    sg.popup(f"Erro ao abrir janela_principal: {error}")

def create_shortcut():
    # Lógica para criar o atalho para tela_seguranca.py
    # Restante do código permanece igual...
    pass

def open_login_window():
    layout = [
        [sg.Text(LOGIN_MESSAGE, font=("Helvetica", 16))],
        [sg.Input(key="-USERNAME-", size=(30, 2), font=("Helvetica", 14))],
        [sg.Input(key="-PASSWORD-", size=(30, 2),
                  font=("Helvetica", 14), password_char="*")],
        [sg.Button("Confirmar", size=(30, 2), font=("Helvetica", 14)), sg.Button(
            EXIT_BUTTON_TEXT, size=(30, 2), font=("Helvetica", 14))]
    ]

    window = sg.Window(
        "Cosmolite - Login",
        layout,
        element_justification="center",
        margins=(100, 100)
    )

    while True:
        event, values = window.read()

        if event is None or event == EXIT_BUTTON_TEXT:
            break

        if event == "Confirmar":
            username = values["-USERNAME-"]
            password = values["-PASSWORD-"]

            window.close()
            return username, password

    window.close()
    return None, None
