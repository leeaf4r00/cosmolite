import os
import subprocess
import PySimpleGUI as sg
import pyperclip
import logging

# Definir o caminho relativo para os arquivos
BASE_PATH = os.path.join(os.path.dirname(__file__), "..")
UTILITARIOS_PATH = os.path.join(BASE_PATH, "Utilitarios")
CONTADOR_MOEDAS_FILE = os.path.join(UTILITARIOS_PATH, "contador_moedas.py")
LISTADOR_ARQUIVOS_FILE = os.path.join(UTILITARIOS_PATH, "listador_arquivos.py")
LISTAR_TODOS_USUARIOS_FILE = os.path.join(
    UTILITARIOS_PATH, "listar_todosusuariosesenhas.py")

# Constantes
TITULO_JANELA_PRINCIPAL = "janela_principal"
BOTAO_CONTADOR_MOEDAS_CEDULAS = "Abrir 'contador_moedas.py'"
BOTAO_LISTAR_ARQUIVOS = "Abrir 'listador_arquivos.py'"
BOTAO_LISTAR_TODOS_USUARIOS = "Abrir 'listar_todosusuariosesenhas.py'"
BOTAO_SAIR = "Sair"
MENSAGEM_ERRO = "Erro ao abrir o arquivo."

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class ArquivoNaoEncontradoError(Exception):
    pass


class ErroAoAbrirArquivoError(Exception):
    pass


class FileOpener:
    def __init__(self, file_path):
        self.file_path = file_path

    def open_file(self, args=None):
        """
        Abre o arquivo com o programa associado.

        Parâmetros:
            args (list): Lista de argumentos para passar ao script (sys.argv).

        Raises:
            ArquivoNaoEncontradoError: Se o arquivo não for encontrado no caminho especificado.
            ErroAoAbrirArquivoError: Se ocorrer um erro ao tentar abrir o arquivo.

        """
        logging.debug("Abrindo arquivo: %s", self.file_path)
        try:
            if os.path.exists(self.file_path):
                command = ["python", self.file_path]
                if args:
                    command.extend(args)
                logging.debug("Comando subprocesso: %s", command)
                subprocess.run(command, check=True)
            else:
                raise ArquivoNaoEncontradoError(
                    f"Arquivo não encontrado: '{self.file_path}'")
        except subprocess.CalledProcessError as error:
            erro = f"{MENSAGEM_ERRO} '{self.file_path}'\nErro: {error}"
            pyperclip.copy(erro)
            raise ErroAoAbrirArquivoError(erro) from error


class App:
    def __init__(self):
        self.layout_principal = [
            [sg.Text(TITULO_JANELA_PRINCIPAL, font=("Helvetica", 20))],
            [sg.Button(BOTAO_CONTADOR_MOEDAS_CEDULAS)],
            [sg.Button(BOTAO_LISTAR_ARQUIVOS)],
            [sg.Button(BOTAO_LISTAR_TODOS_USUARIOS)],
            [sg.Button(BOTAO_SAIR)]
        ]
        self.janela_principal = sg.Window(
            TITULO_JANELA_PRINCIPAL, self.layout_principal, finalize=True)

    def executar(self):
        while True:
            evento, _ = self.janela_principal.read()

            if evento == sg.WIN_CLOSED or evento == BOTAO_SAIR:
                break
            elif evento == BOTAO_CONTADOR_MOEDAS_CEDULAS:
                try:
                    file_opener = FileOpener(CONTADOR_MOEDAS_FILE)
                    file_opener.open_file()
                except ArquivoNaoEncontradoError as error:
                    sg.popup_error(
                        str(error), keep_on_top=True, line_width=100)
                except ErroAoAbrirArquivoError as error:
                    sg.popup_error(
                        str(error), keep_on_top=True, line_width=100)
                    sg.popup_ok(
                        "O erro foi copiado para a área de transferência.", title="Erro")
            elif evento == BOTAO_LISTAR_ARQUIVOS:
                try:
                    file_opener = FileOpener(LISTADOR_ARQUIVOS_FILE)
                    file_opener.open_file()
                except ArquivoNaoEncontradoError as error:
                    sg.popup_error(
                        str(error), keep_on_top=True, line_width=100)
                except ErroAoAbrirArquivoError as error:
                    sg.popup_error(
                        str(error), keep_on_top=True, line_width=100)
                    sg.popup_ok(
                        "O erro foi copiado para a área de transferência.", title="Erro")
            elif evento == BOTAO_LISTAR_TODOS_USUARIOS:
                try:
                    file_opener = FileOpener(LISTAR_TODOS_USUARIOS_FILE)
                    # Pass arguments if needed (e.g., ["--verbose", "arg1", "arg2"])
                    file_opener.open_file(args=["arg1", "arg2"])
                except ArquivoNaoEncontradoError as error:
                    sg.popup_error(
                        str(error), keep_on_top=True, line_width=100)
                except ErroAoAbrirArquivoError as error:
                    sg.popup_error(
                        str(error), keep_on_top=True, line_width=100)
                    sg.popup_ok(
                        "O erro foi copiado para a área de transferência.", title="Erro")

        self.janela_principal.close()


if __name__ == "__main__":
    app = App()
    app.executar()
