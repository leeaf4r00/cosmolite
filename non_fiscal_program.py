import PySimpleGUI as sg
import subprocess
import sys
import time
from datetime import datetime
import sqlite3
import threading
import os

sg.set_options(font=("Helvetica", 12))

# Definindo o tema
sg.theme("LightGrey1")

# Conexão com o banco de dados
conn = sqlite3.connect("users.db")


def open_window(window_name):
    subprocess.call([sys.executable, f"{window_name}.py"])


def show_popup(message):
    sg.popup(message)


def get_user_info():
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    result = cursor.fetchone()
    return result[0] if result else "Desconhecido"


def get_connected_users_count():
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    result = cursor.fetchone()
    return result[0]


def get_current_date():
    now = datetime.now()
    return now.strftime("%d/%m/%Y")


def login():
    layout_login = [
        [sg.Text("Cosmolite V-1.0", font=(
            "Helvetica", 20), justification="center")],
        [sg.Text("Nome de Usuário:"), sg.Input(key="-USERNAME-")],
        [sg.Text("Senha:"), sg.Input(key="-PASSWORD-", password_char="*")],
        [sg.Button("Login"), sg.Button("Cadastrar")]
    ]

    window_login = sg.Window("Cosmolite V-1.0",
                             layout_login, finalize=True)
    window_login['-USERNAME-'].expand(expand_x=True)

    while True:
        event, values = window_login.read()

        if event is None:
            window_login.close()
            sys.exit()

        if event == "Login":
            username = values["-USERNAME-"]
            password = values["-PASSWORD-"]

            if not username or not password:
                show_popup("Por favor, preencha todos os campos.")
                continue

            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?", (username, password))
            result = cursor.fetchone()

            if result:
                window_login.close()
                open_window("janela_principal_nao_fiscal")
                return

            show_popup("Credenciais inválidas. Tente novamente.")

        if event == "Cadastrar":
            window_login.close()
            register()
            break


def register():
    layout_cadastro = [
        [sg.Text("Cosmolite 1.0", font=(
            "Helvetica", 20), justification="center")],
        [sg.Text("Nome de Usuário:"), sg.Input(key="-USERNAME-")],
        [sg.Text("Senha:"), sg.Input(key="-PASSWORD-", password_char="*")],
        [sg.Button("Cadastrar"), sg.Button("Voltar")]
    ]

    window_cadastro = sg.Window(
        "Cosmolite 1.0", layout_cadastro, finalize=True)
    window_cadastro['-USERNAME-'].expand(expand_x=True)

    while True:
        event, values = window_cadastro.read()

        if event is None:
            window_cadastro.close()
            sys.exit()

        if event == "Cadastrar":
            username = values["-USERNAME-"]
            password = values["-PASSWORD-"]

            if not username or not password:
                show_popup("Por favor, preencha todos os campos.")
                continue

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            result = cursor.fetchone()

            if result:
                show_popup("Nome de usuário já em uso. Escolha outro nome de usuário.")
            else:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                show_popup("Cadastro realizado com sucesso.")
                window_cadastro.close()
                login()
                return

        if event == "Voltar":
            window_cadastro.close()
            login()
            return


def resize_image(filename, target_width, target_height):
    import PIL.Image

    image = PIL.Image.open(filename)
    resized_image = image.resize((target_width, target_height))
    resized_filename = os.path.join("C:\\Users\\RR ATACADISTA\\Documents\\COSMOLITE\\images", f"resized_{os.path.basename(filename)}")

    # Verificar se o diretório de destino existe, caso contrário, criá-lo
    os.makedirs(os.path.dirname(resized_filename), exist_ok=True)

    resized_image.save(resized_filename)
    return resized_filename

# Função para abrir a janela principal
def open_main_window():
    resized_image_filename = resize_image(os.path.join(
        "images", "cosmolite.png"), 200, 200)
    loading_image_filename = os.path.join(
        "images", "Loading.gif")

    layout_main = [
        [sg.Column(
            [
                [sg.Text("Cosmolite 1.0", font=(
                    "Helvetica", 20), justification="center")],
                [sg.Image(resized_image_filename)],
                [sg.Text("Seja Bem Vindo! Primeiro faça seu cadastro e depois faça seu login.\nCosmolite seu Sistema de Automação Comercial",
                         font=("Helvetica", 12), justification="center", size=(400, 2), key="-INFO-")],
                [sg.Button("Login", size=(10, 1), key="-LOGIN-"),
                 sg.Button("Cadastrar", size=(10, 1), key="-CADASTRAR-")],
                [sg.Text("Desenvolvido por Rafael Moreira Fernandes - Todos os Direitos Reservados.©",
                         font=("Helvetica", 10), justification="center")],
                [sg.Text(f"Data: {get_current_date()}", font=("Helvetica", 10), justification="center", key="-DATE-")]
            ],
            element_justification="center"
        )]
    ]

    window_main = sg.Window("Cosmolite V-1.0",
                            layout_main, finalize=True, size=(550, 450), use_ttk_buttons=True)

    while True:
        event, values = window_main.read()

        if event is None:
            window_main.close()
            sys.exit()

        if event == "-LOGIN-":
            window_main.close()
            login()
            break

        if event == "-CADASTRAR-":
            window_main.close()
            register()
            break


if __name__ == "__main__":
    open_main_window()
