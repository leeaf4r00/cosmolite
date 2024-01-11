import PySimpleGUI as sg
import psutil
import sqlite3
import subprocess
import os
import sys
import logging
import traceback
import pyperclip
import importlib

# Adicionar o caminho relativo do diretório 'janela_principal' ao sys.path
current_path = os.path.dirname(os.path.abspath(__file__))
janela_principal_path = os.path.join(current_path, 'janela_principal')
sys.path.append(janela_principal_path)

# Constantes
TELA_SEGURANCA_FILE = "cosmolite/tela_seguranca.py"
LOG_FILE = "log.py"
WELCOME_MESSAGE = "Bem-vindo ao Cosmolite"
FIRST_ACCESS_MESSAGE = "Digite sua Chave de segurança para o primeiro acesso"
LOGIN_MESSAGE = "Faça o login"
LOGIN_BUTTON_TEXT = "Login"
SECURITY_BUTTON_TEXT = "Digite sua Chave de segurança"
EXIT_BUTTON_TEXT = "Sair"
IMAGE_PATH = os.path.join(current_path, "images", "cosmolite.png")

# Verifica se o programa de log já está em execução
for proc in psutil.process_iter():
    try:
        if proc.name().lower() == "python" and LOG_FILE in proc.cmdline():
            proc.terminate()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass


def show_error_popup(error_message):
    """
    Mostra um popup com a mensagem de erro.
    """
    sg.popup_error("Ocorreu um erro!", error_message, keep_on_top=True)


def copy_error_to_clipboard():
    """
    Captura o último traceback e tenta copiar para o clipboard.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_message = traceback.format_exception(
        exc_type, exc_value, exc_traceback)
    error_text = "".join(error_message)
    try:
        pyperclip.copy(error_text)
        print("Erro copiado para o clipboard.")
    except pyperclip.PyperclipException as e:
        print(f"Erro ao copiar o erro para o clipboard: {e}")


def create_shortcut():
    # Abre o arquivo tela_seguranca.py se ainda não estiver sendo executado.
    if is_tela_seguranca_running():
        sg.popup("Janela de tela_seguranca já está aberta!")
        return False

    try:
        subprocess.Popen(["python", TELA_SEGURANCA_FILE])
        return True
    except subprocess.CalledProcessError as error:
        sg.popup_error(f"Erro ao abrir o arquivo tela_seguranca.py: {error}")
        return False
    except Exception as e:
        sg.popup_error(
            f"Erro desconhecido ao abrir o arquivo tela_seguranca.py: {e}")
        return False


def is_tela_seguranca_running():
    # Verifica se o arquivo tela_seguranca.py está sendo executado.
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == "python" and TELA_SEGURANCA_FILE in proc.cmdline():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def open_cosmolite_window():
    # Abre a janela do Cosmolite.
    database_file = "users.db"
    is_first = is_first_run(database_file)

    if is_first:
        layout = [
            [sg.Text(FIRST_ACCESS_MESSAGE, font=("Helvetica", 16))],
            [sg.Image(filename=IMAGE_PATH)],
            [sg.Button(SECURITY_BUTTON_TEXT, size=(
                30, 2), font=("Helvetica", 14))],
            [sg.Button(EXIT_BUTTON_TEXT, size=(30, 2), font=("Helvetica", 14))]
        ]
    else:
        layout = [
            [sg.Text(WELCOME_MESSAGE, font=("Helvetica", 16))],
            [sg.Image(filename=IMAGE_PATH)],
            [sg.Button(LOGIN_BUTTON_TEXT, size=(
                30, 2), font=("Helvetica", 14))],
            [sg.Button(EXIT_BUTTON_TEXT, size=(30, 2), font=("Helvetica", 14))]
        ]

    window = sg.Window(
        "Cosmolite",
        layout,
        element_justification="center",
        margins=(100, 100)
    )

    while True:
        event, _ = window.read()

        if event is None or event == EXIT_BUTTON_TEXT:
            break

        if event == SECURITY_BUTTON_TEXT and is_first:
            create_shortcut()
            break

        if event == LOGIN_BUTTON_TEXT and not is_first:
            open_login_window()
            break

    window.close()

    if not is_tela_seguranca_running():
        sys.exit()

    program_type = read_program_type()
    if program_type == "cadastro":
        run_cadastro(program_type)


def open_login_window():
    # Abre a janela de login.
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

            if validate_login(username, password):
                sg.popup("Login bem-sucedido!")
                open_janela_principal()
                break
            else:
                sg.popup("Login inválido!")

    window.close()


def validate_login(username, password):
    # Valida as credenciais de login no banco de dados.
    database_file = "users.db"
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and user[2] == password:
        return True

    conn.close()
    return False


def open_janela_principal():
    # Abre a janela principal.
    try:
        janela_principal = importlib.import_module(
            "janela_principal.janela_principal")
        janela = janela_principal.JanelaPrincipal(first_run=False)
        janela.run()
    except ImportError as error:
        sg.popup(f"Erro ao abrir janela_principal: {error}")


def run_cadastro(program_type):
    # Executa a função de cadastro.
    open_janela_principal()


def is_first_run(database_file):
    # Verifica se é a primeira execução do programa.
    if not os.path.isfile(database_file):
        return True

    database = sqlite3.connect(database_file)
    cursor = database.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    database.close()

    return user_count == 0


def read_program_type():
    # Lê o tipo de programa registrado no banco de dados.
    database_file = "users.db"

    if is_first_run(database_file):
        return "cadastro"

    # Lógica para ler o tipo de programa registrado no banco de dados
    # Substitua esse trecho pelo seu código de leitura do banco de dados
    return "fiscal"  # Exemplo de retorno


def hide_console_window():
    # Esconde a janela do console.
    try:
        import win32console
        import win32gui

        console_hwnd = win32console.GetConsoleWindow()
        win32gui.ShowWindow(console_hwnd, 0)
    except ImportError:
        pass


def setup_logger():
    """
    Configura o logger para registrar os erros em um arquivo de log.
    """
    logger = logging.getLogger("cosmolite_logger")
    logger.setLevel(logging.ERROR)

    # Cria um manipulador para escrever os logs em um arquivo
    log_file = "error_log.txt"
    file_handler = logging.FileHandler(log_file)

    # Formatação do log
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def main():
    hide_console_window()

    # Configura o logger
    logger = setup_logger()

    while True:
        try:
            if is_first_run("users.db"):
                # Primeira execução do programa
                if not create_shortcut():
                    show_error_popup("Erro ao criar o atalho.")
                    return

            # Abrir a janela do Cosmolite
            open_cosmolite_window()
        except Exception as e:
            # Captura o traceback do erro
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_message = traceback.format_exception(
                exc_type, exc_value, exc_traceback)
            error_text = "".join(error_message)

            # Registra o erro no arquivo de log
            logger.error(error_text)

            # Exibe o erro em um popup
            show_error_popup(error_text)

            # Tenta copiar o erro para o clipboard
            copy_error_to_clipboard()

            # Rethrow the exception to show the error message on the console (if available)
            raise
        finally:
            # Certifique-se de que o programa é encerrado corretamente
            if not is_tela_seguranca_running():
                return


if __name__ == "__main__":
    main()
