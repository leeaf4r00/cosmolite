import os
import sys
import subprocess
from datetime import datetime
import sqlite3
import shutil
import PySimpleGUI as sg
import traceback
import pyperclip
import tkinter as tk

# Constantes
LOGIN_TITLE = "Cosmolite 1.0 Fiscal - Login"
MAIN_TITLE = "Sistema Fiscal - COSMOLITE - V.1.0 - Janela Principal"
WINDOW_SIZE = (550, 450)
LOGIN_IMAGE_PATH = os.path.join("cosmolite", "images", "cosmolite.png")
DB_PATH = "users.db"


class JanelaPrincipal:
    def __init__(self, first_run=True):
        self.conn = sqlite3.connect("users.db")
        self.window = None
        self.first_run = first_run

    def run(self):
        print("Caminho da imagem de login:", LOGIN_IMAGE_PATH)

        try:
            if self.first_run:
                self.login()
            else:
                self.abrir_janela_principal()
        except Exception as ex:
            tb = traceback.format_exc()
            self.show_error("Ocorreu um erro inesperado:", str(ex), tb)
            pyperclip.copy(tb)

    def login(self):
        layout_login = [
            [sg.Image(filename=os.path.join("images", "cosmolite.png"),
                      size=(300, 300), pad=(40, 40))],
            [sg.Text("Cosmolite 1.0 Fiscal", font=("Helvetica", 20),
                     justification="center", pad=((40, 40), (0, 40)))],
            [sg.Text("Nome de Usuário:", size=(15, 1), justification="right"), sg.Input(
                key="-USERNAME-", size=(30, 1), font=("Helvetica", 14))],
            [sg.Text("Senha:", size=(15, 1), justification="right"), sg.Input(
                key="-PASSWORD-", size=(30, 1), font=("Helvetica", 14), password_char="*")],
            [sg.Button("Login", size=(15, 1), pad=(10, 10))],
            [sg.Button("Cadastrar", size=(15, 1), pad=(10, 10))]
        ]

        window_login = sg.Window(LOGIN_TITLE, layout_login, finalize=True)

        while True:
            event, values = window_login.read()

            if event is None:
                window_login.close()
                sys.exit()

            if event == "Login":
                try:
                    self.perform_login(
                        values["-USERNAME-"], values["-PASSWORD-"])
                    window_login.close()
                    self.abrir_janela_principal()
                    break
                except ValueError as ve:
                    self.show_error("Erro de Login:", str(ve))

            if event == "Cadastrar":
                window_login.close()
                self.register()
                break

    def perform_login(self, username, password):
        if not username or not password:
            raise ValueError("Por favor, preencha todos os campos.")

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()

        if not result:
            raise ValueError("Credenciais inválidas. Tente novamente.")

    def register(self):
        layout_cadastro = [
            [sg.Image(filename=os.path.join("images", "cosmolite.png"),
                      size=(300, 300), pad=(40, 40))],
            [sg.Text("Cosmolite 1.0 Fiscal", font=("Helvetica", 20),
                     justification="center", pad=((40, 40), (0, 40)))],
            [sg.Text("Nome de Usuário:", size=(15, 1), justification="right"), sg.Input(
                key="-USERNAME-", size=(30, 1), font=("Helvetica", 14))],
            [sg.Text("Senha:", size=(15, 1), justification="right"), sg.Input(
                key="-PASSWORD-", size=(30, 1), font=("Helvetica", 14), password_char="*")],
            [sg.Button("Cadastrar", size=(15, 1), pad=(10, 10))],
            [sg.Button("Voltar", size=(15, 1), pad=(10, 10))]
        ]

        window_cadastro = sg.Window(
            LOGIN_TITLE, layout_cadastro, finalize=True)

        while True:
            event, values = window_cadastro.read()

            if event is None:
                window_cadastro.close()
                sys.exit()

            if event == "Cadastrar":
                try:
                    self.perform_register(
                        values["-USERNAME-"], values["-PASSWORD-"])
                    sg.popup("Cadastro realizado com sucesso.")
                    window_cadastro.close()
                    self.login()
                    break
                except ValueError as ve:
                    self.show_error("Erro de Cadastro:", str(ve))

            if event == "Voltar":
                window_cadastro.close()
                self.login()
                break

    def perform_register(self, username, password):
        if not username or not password:
            raise ValueError("Por favor, preencha todos os campos.")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

        if result:
            raise ValueError(
                "Nome de usuário já em uso. Escolha outro nome de usuário.")

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def abrir_janela_principal(self):
        username = self.get_connected_username()
        users_count = self.get_connected_users_count()

        layout_principal = self.criar_layout(username, users_count)

        self.window = sg.Window(MAIN_TITLE, layout_principal, finalize=True)
        self.window["-DATE-"].update(self.get_current_date())

        while True:
            event, _ = self.window.read()

            if event is None:
                break

            button_actions = {
                "Estoque": self.abrir_estoque,
                "Vendas": self.abrir_vendas,
                "Cosmolite Fiscal": self.abrir_cosmolite_fiscal,
                "Gráficos": self.abrir_graficos,
                "Financeiro": self.abrir_financeiro,
                "Internet": self.abrir_internet,
                "Termos": self.abrir_termos,
                "Utilitários": self.abrir_utilitarios,
                "Atendimento": self.abrir_atendimento,
                "Relatórios": self.abrir_relatorios,
                "Configurações": self.abrir_configuracoes,
                "Sair": self.perform_exit,
                "Cadastros": self.abrir_cadastros,
            }

            if event in button_actions:
                button_actions[event]()

            self.window["-DATE-"].update(self.get_current_date())

        self.window.close()

    def criar_layout(self, username, users_count):
        layout_principal = [
            [sg.Text("COSMOLITE - V.1.0 - Janela Principal", font=("Helvetica",
                                                                   18, 'bold'), justification='center', key='-TITLE-')],
            [sg.Button("Estoque"), sg.Button("Vendas"), sg.Button(
                "Cosmolite Fiscal"), sg.Button("Gráficos"), sg.Button("Financeiro")],
            [sg.Button("Internet"), sg.Button("Termos"), sg.Button("Utilitários"), sg.Button("Atendimento"), sg.Button("Relatórios"),
             sg.Button("Configurações"), sg.Button("Cadastros")],
            [sg.Text(f"Usuário: {username} - Número de Usuários: {users_count} - Data: ", key='-STATUS-', size=(None, 1)),
             sg.Text("", key="-DATE-", size=(20, 1))],
            [sg.Button("Sair", button_color=("white", "red"))],
            [sg.Text(
                "Desenvolvido por Rafael Moreira Fernandes | Todos os Direitos Reservados.")]
        ]

        return layout_principal

    def get_connected_username(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT username FROM users")
        result = cursor.fetchone()
        return result[0] if result else "Desconhecido"

    def get_connected_users_count(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        return result[0]

    def perform_exit(self):
        layout_confirm_exit = [
            [sg.Text("Deseja realizar o backup antes de sair?")],
            [sg.Button("Sair"), sg.Button("Realizar Backup")]
        ]

        window_confirm_exit = sg.Window(
            "Confirmação de Saída", layout_confirm_exit, finalize=True)

        while True:
            event, _ = window_confirm_exit.read()

            if event is None:
                break

            if event == "Sair":
                window_confirm_exit.close()
                sg.popup("Saindo do sistema...")
                sys.exit()
            elif event == "Realizar Backup":
                self.realizar_backup()
                sg.popup("Backup Realizado com Sucesso!")
                break

        window_confirm_exit.close()

    def realizar_backup(self):
        shutil.copyfile("users.db", "backup.db")
        sg.popup("Backup realizado com sucesso.")

    def get_current_date(self):
        return datetime.now().strftime("%d/%m/%Y")

    def abrir_estoque(self):
        self.open_subwindow("Estoque", os.path.join(
            "janela_principal", "Estoque", "estoque.py"))

    def abrir_vendas(self):
        self.open_subwindow("Vendas", os.path.join(
            "janela_principal", "Vendas", "vendas.py"))

    def abrir_cosmolite_fiscal(self):
        self.open_subwindow("Cosmolite Fiscal", os.path.join(
            "janela_principal", "Cosmolite_Fiscal", "CosmoliteFiscal.py"))

    def abrir_graficos(self):
        self.open_subwindow("Gráficos", os.path.join(
            "janela_principal", "Gráficos", "graficos.py"))

    def abrir_financeiro(self):
        self.open_subwindow("Financeiro", os.path.join(
            "janela_principal", "Financeiro", "financeiro.py"))

    def abrir_internet(self):
        self.open_subwindow("Internet", os.path.join(
            "janela_principal", "Internet", "internet.py"))

    def abrir_termos(self):
        self.open_subwindow("Termos", os.path.join(
            "janela_principal", "Termos", "termos.py"))

    def abrir_utilitarios(self):
        self.open_subwindow("Utilitários", os.path.join(
            "janela_principal", "Utilitários", "utilitarios.py"))

    def abrir_atendimento(self):
        self.open_subwindow("Atendimento", os.path.join(
            "janela_principal", "Atendimento", "atendimento.py"))

    def abrir_relatorios(self):
        self.open_subwindow("Relatórios", os.path.join(
            "janela_principal", "Relatórios", "Relatorios_controle_moedas", "relatorios.py"))

    def abrir_configuracoes(self):
        self.open_subwindow("Configurações", os.path.join(
            "janela_principal", "Configurações", "configuracoes.py"))

    def abrir_cadastros(self):
        self.open_subwindow("Cadastros", os.path.join(
            "janela_principal", "Cadastros", "cadastros.py"))

    def open_subwindow(self, title, path):
        subprocess.Popen(['python', path])

    def show_error(self, title, message, traceback_text=None):
        layout_error = [
            [sg.Text(title, font=("Helvetica", 14), justification="center")],
            [sg.Text(message)],
            [sg.Multiline(default_text=traceback_text,
                          size=(80, 15), key='-TRACEBACK-')],
            [sg.Button("OK")]
        ]

        window_error = sg.Window("Erro", layout_error, finalize=True)

        while True:
            event, values = window_error.read()

            if event == "OK" or event is None:
                traceback_text = values['-TRACEBACK-']
                pyperclip.copy(traceback_text)
                break

        window_error.close()

    def copiar_para_area_de_transferencia(self, texto):
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(texto)
        root.update()
        root.destroy()


if __name__ == "__main__":
    janela_principal = JanelaPrincipal()
    janela_principal.run()
