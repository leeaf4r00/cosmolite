#fiscal_program.py
import os
import sys
import sqlite3
import PySimpleGUI as sg
import subprocess  # Adicione esta linha para importar a biblioteca 'subprocess'
from typing import List, Tuple

# Importe a função popup diretamente do módulo PySimpleGUI
from PySimpleGUI import popup

# Define o caminho absoluto para a imagem "Cosmolite.png"
current_dir = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(current_dir, "images", "cosmolite.png")

# Define as constantes para o arquivo fiscal_program.py
DB_FILE = "users.db"
WINDOW_TITLE = "Cosmolite 1.0 Fiscal"
USERNAME_LABEL = "Nome de Usuário:"
PASSWORD_LABEL = "Senha:"
LOGIN_BUTTON = "Login"
REGISTER_BUTTON = "Cadastrar"
BACK_BUTTON = "Voltar"
EXIT_BUTTON = "Sair"
NO_USERS_MESSAGE = "Nenhum usuário cadastrado. Por favor, realize o cadastro."
INVALID_CREDENTIALS_MESSAGE = "Credenciais inválidas. Tente novamente."
FILL_FIELDS_MESSAGE = "Por favor, preencha todos os campos."
USERNAME_IN_USE_MESSAGE = "Nome de usuário já em uso. Escolha outro nome de usuário."
ERROR_TITLE = "Erro"
FIRST_TIME_ACCESS_MESSAGE = "Seja bem-vindo ao Cosmolite!\nAgora realize seu primeiro cadastro."

# Verificar se o arquivo "users.db" já existe
if not os.path.isfile(DB_FILE):
    # Criar o arquivo "users.db" e a tabela "users" se não existirem
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    conn.commit()
    conn.close()

def autenticar_usuario():
    """Autentica o usuário antes de liberar acesso às funcionalidades"""
    layout_login = [
        [sg.Image(filename=IMAGE_PATH, size=(300, 300), pad=(40, 40))],
        [sg.Text(WINDOW_TITLE, font=("Helvetica", 20), justification="center", pad=((40, 40), (0, 40)))],
        [sg.Text(USERNAME_LABEL, size=(15, 1), justification="right"), sg.Input(key="-USERNAME-", size=(30, 1), font=("Helvetica", 14))],
        [sg.Text(PASSWORD_LABEL, size=(15, 1), justification="right"), sg.Input(key="-PASSWORD-", size=(30, 1), font=("Helvetica", 14), password_char="*")],
        [sg.Button(LOGIN_BUTTON, size=(15, 1), pad=(10, 10))],
        [sg.Button(REGISTER_BUTTON, size=(15, 1), pad=(10, 10))]
    ]

    window_login = sg.Window(WINDOW_TITLE, layout_login, finalize=True)

    while True:
        event, values = window_login.read()

        if event is None:
            window_login.close()
            sys.exit()

        if event == LOGIN_BUTTON:
            username = values["-USERNAME-"]
            password = values["-PASSWORD-"]

            if not username or not password:
                popup(FILL_FIELDS_MESSAGE)
                continue

            if autenticar_usuario_db(username, password):
                window_login.close()
                abrir_janela_principal()
                return
            else:
                popup(INVALID_CREDENTIALS_MESSAGE)

        if event == REGISTER_BUTTON:
            window_login.close()
            popup(FIRST_TIME_ACCESS_MESSAGE)
            cadastrar_usuario()
            return

def autenticar_usuario_db(username: str, password: str) -> bool:
    """Verifica se as credenciais de usuário são válidas no banco de dados"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def cadastrar_usuario():
    """Realiza o cadastro do usuário"""
    layout_cadastro = [
        [sg.Image(filename=IMAGE_PATH, size=(300, 300), pad=(40, 40))],
        [sg.Text(WINDOW_TITLE, font=("Helvetica", 20), justification="center", pad=((40, 40), (0, 40)))],
        [sg.Text(USERNAME_LABEL, size=(15, 1), justification="right"), sg.Input(key="-USERNAME-", size=(30, 1), font=("Helvetica", 14))],
        [sg.Text(PASSWORD_LABEL, size=(15, 1), justification="right"), sg.Input(key="-PASSWORD-", size=(30, 1), font=("Helvetica", 14), password_char="*")],
        [sg.Text("Confirme sua senha:", size=(15, 1), justification="right"), sg.Input(key="-CONFIRM_PASSWORD-", size=(30, 1), font=("Helvetica", 14), password_char="*")],
        [sg.Button(REGISTER_BUTTON, size=(15, 1), pad=(10, 10))],
        [sg.Button(BACK_BUTTON, size=(15, 1), pad=(10, 10))]
    ]

    window_cadastro = sg.Window(WINDOW_TITLE, layout_cadastro, finalize=True)

    while True:
        event, values = window_cadastro.read()

        if event is None:
            window_cadastro.close()
            sys.exit()

        if event == REGISTER_BUTTON:
            username = values["-USERNAME-"]
            password = values["-PASSWORD-"]
            confirm_password = values["-CONFIRM_PASSWORD-"]

            if not username or not password or not confirm_password:
                popup(FILL_FIELDS_MESSAGE)
                continue

            if password != confirm_password:
                popup("As senhas digitadas não correspondem. Tente novamente.")
                continue

            if cadastrar_usuario_db(username, password):
                popup("Cadastro realizado com sucesso.")
                window_cadastro.close()
                abrir_janela_principal()
                return
            else:
                popup(USERNAME_IN_USE_MESSAGE)

        if event == BACK_BUTTON:
            window_cadastro.close()
            autenticar_usuario()
            return

def cadastrar_usuario_db(username: str, password: str) -> bool:
    """Cadastra um novo usuário no banco de dados"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    
    if result is not None:
        conn.close()
        return False
    
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return True

def abrir_janela_principal():
    """Abre a janela principal do sistema após a autenticação bem-sucedida"""
    # Define o caminho relativo para o arquivo janela_principal.py
    janela_principal_path = os.path.join(current_dir, "janela_principal", "janela_principal.py")
    subprocess.Popen([sys.executable, janela_principal_path])

# Verificar se é o primeiro cadastro
def verificar_primeiro_cadastro():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchone()
    conn.close()

    if result is None:
        popup(NO_USERS_MESSAGE)
        cadastrar_usuario()
    else:
        autenticar_usuario()

verificar_primeiro_cadastro()