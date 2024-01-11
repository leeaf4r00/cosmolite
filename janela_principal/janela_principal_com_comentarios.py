# janela_principal\janela_principal.py
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

# Constants
LOGIN_TITLE = "Cosmolite 1.0 Fiscal - Login"
MAIN_TITLE = "Sistema Fiscal - COSMOLITE - V.1.0 - Janela Principal"
WINDOW_SIZE = (550, 450)
LOGIN_IMAGE_PATH = os.path.join("cosmolite", "images", "cosmolite.png")
DB_PATH = "users.db"


class JanelaPrincipal:
    def __init__(self, first_run=True):
        """
        Inicializa a classe JanelaPrincipal.

        Args:
            first_run (bool, optional): Indica se é a primeira execução do programa. Defaults to True.
        """
        # Conexão com o banco de dados
        self.conn = sqlite3.connect("users.db")
        self.window = None
        self.first_run = first_run

    def run(self):
        """
        Inicia a execução da interface gráfica.
        """
        # Imprimir o valor de LOGIN_IMAGE_PATH
        print("Caminho da imagem de login:", LOGIN_IMAGE_PATH)

        try:
            if self.first_run:
                self.login()
            else:
                self.abrir_janela_principal()
        except Exception as ex:
            # Se ocorrer um erro, exibe uma janela de erro com o traceback
            tb = traceback.format_exc()
            self.show_error("Ocorreu um erro inesperado:", str(ex), tb)
            # Copia o traceback para a área de transferência
            pyperclip.copy(tb)

    def login(self):
        """
        Exibe a janela de login.
        """
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
        """
        Realiza a autenticação do usuário com o nome de usuário e senha fornecidos.

        Args:
            username (str): Nome de usuário.
            password (str): Senha.

        Raises:
            ValueError: Se as credenciais forem inválidas ou não forem preenchidas corretamente.
        """
        if not username or not password:
            raise ValueError("Por favor, preencha todos os campos.")

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()

        if not result:
            raise ValueError("Credenciais inválidas. Tente novamente.")

    def register(self):
        """
        Exibe a janela de cadastro de novo usuário.
        """
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
        """
        Realiza o cadastro de um novo usuário com o nome de usuário e senha fornecidos.

        Args:
            username (str): Nome de usuário.
            password (str): Senha.

        Raises:
            ValueError: Se o nome de usuário já estiver em uso ou se algum campo não for preenchido corretamente.
        """
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
        """
        Abre a janela principal do sistema.
        """
        username = self.get_connected_username()
        users_count = self.get_connected_users_count()

        layout_principal = self.criar_layout(username, users_count)

        self.window = sg.Window(MAIN_TITLE, layout_principal, finalize=True)

        # Atualizar a data exibida
        self.window["-DATE-"].update(self.get_current_date())

        while True:
            event, _ = self.window.read()

            if event is None:
                break

            # Executar a função correspondente ao botão pressionado
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

            # Atualizar a data exibida
            self.window["-DATE-"].update(self.get_current_date())

        self.window.close()

    def criar_layout(self, username, users_count):
        """
        Cria o layout da janela principal.

        Args:
            username (str): Nome de usuário conectado.
            users_count (int): Número de usuários conectados.

        Returns:
            list: Layout da janela principal.
        """
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
        """
        Obtém o nome de usuário conectado.

        Returns:
            str: Nome de usuário conectado.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT username FROM users")
        result = cursor.fetchone()
        return result[0] if result else "Desconhecido"

    def get_connected_users_count(self):
        """
        Obtém o número de usuários conectados.

        Returns:
            int: Número de usuários conectados.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        return result[0]

    def perform_exit(self):
        """
        Função para confirmar a saída e realizar o backup.
        """
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
        """
        Realiza o backup do banco de dados.
        """
        shutil.copyfile("users.db", "backup.db")
        sg.popup("Backup realizado com sucesso.")

    def get_current_date(self):
        """
        Obtém a data atual.

        Returns:
            str: Data atual no formato "dd/mm/yyyy".
        """
        return datetime.now().strftime("%d/%m/%Y")

    def abrir_estoque(self):
        """
        Abre a janela do módulo Estoque.
        """
        self.open_subwindow("Estoque", os.path.join(
            "janela_principal", "Estoque", "estoque.py"))

    def abrir_vendas(self):
        """
        Abre a janela do módulo Vendas.
        """
        self.open_subwindow("Vendas", os.path.join(
            "janela_principal", "Vendas", "vendas.py"))

    def abrir_cosmolite_fiscal(self):
        """
        Abre a janela do módulo Cosmolite Fiscal.
        """
        self.open_subwindow("Cosmolite Fiscal", os.path.join(
            "janela_principal", "Cosmolite_Fiscal", "CosmoliteFiscal.py"))

    def abrir_graficos(self):
        """
        Abre a janela do módulo Gráficos.
        """
        self.open_subwindow("Gráficos", os.path.join(
            "janela_principal", "Gráficos", "graficos.py"))

    def abrir_financeiro(self):
        """
        Abre a janela do módulo Financeiro.
        """
        self.open_subwindow("Financeiro", os.path.join(
            "janela_principal", "Financeiro", "financeiro.py"))

    def abrir_internet(self):
        """
        Abre a janela do módulo Internet.
        """
        self.open_subwindow("Internet", os.path.join(
            "janela_principal", "Internet", "internet.py"))

    def abrir_termos(self):
        """
        Abre a janela do módulo Termos.
        """
        self.open_subwindow("Termos", os.path.join(
            "janela_principal", "Termos", "termos.py"))

    def abrir_utilitarios(self):
        """
        Abre a janela do módulo Utilitários.
        """
        self.open_subwindow("Utilitários", os.path.join(
            "janela_principal", "Utilitários", "utilitarios.py"))

    def abrir_atendimento(self):
        """
        Abre a janela do módulo Atendimento.
        """
        self.open_subwindow("Atendimento", os.path.join(
            "janela_principal", "Atendimento", "atendimento.py"))

    def abrir_relatorios(self):
        """
        Abre a janela do módulo Relatórios.
        """
        self.open_subwindow("Relatórios", os.path.join(
            "janela_principal", "Relatórios", "Relatorios_controle_moedas", "relatorios.py"))

    def abrir_configuracoes(self):
        """
        Abre a janela do módulo Configurações.
        """
        self.open_subwindow("Configurações", os.path.join(
            "janela_principal", "Configurações", "configuracoes.py"))

    def abrir_cadastros(self):
        """
        Abre a janela do módulo Cadastros.
        """
        self.open_subwindow("Cadastros", os.path.join(
            "janela_principal", "Cadastros", "cadastros.py"))

    def open_subwindow(self, title, path):
        """
        Abre uma sub-janela com base no caminho do arquivo fornecido.

        Args:
            title (str): Título da sub-janela.
            path (str): Caminho do arquivo a ser executado.
        """
        subprocess.Popen(['python', path])

    def show_error(self, title, message, traceback_text=None):
        """
        Exibe uma janela de erro com o título, a mensagem e o traceback fornecidos.

        Args:
            title (str): Título da janela de erro.
            message (str): Mensagem de erro.
            traceback_text (str, optional): Texto do traceback. Defaults to None.
        """
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
                # Copia o traceback para a área de transferência
                pyperclip.copy(traceback_text)
                break

        window_error.close()

    def copiar_para_area_de_transferencia(self, texto):
        """
        Copia o texto fornecido para a área de transferência.

        Args:
            texto (str): Texto a ser copiado para a área de transferência.
        """
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(texto)
        root.update()  # agora o texto permanecerá na área de transferência após o fechamento da janela
        root.destroy()


if __name__ == "__main__":
    janela_principal = JanelaPrincipal()
    janela_principal.run()
