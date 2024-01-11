# utils.py
import os
import shutil
import PIL.Image
import PySimpleGUI as sg
import pyperclip
import tkinter as tk


def verificar_criar_pasta(caminho_pasta: str) -> None:
    """
    Verifica se a pasta existe e a cria, se necessário.

    Args:
        caminho_pasta (str): Caminho da pasta a ser verificada/criada.
    """
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)


def redimensionar_imagem(nome_arquivo: str, largura_alvo: int, altura_alvo: int) -> str:
    """
    Redimensiona uma imagem para a largura e altura desejadas.

    Args:
        nome_arquivo (str): Caminho do arquivo de imagem.
        largura_alvo (int): Largura desejada da imagem redimensionada.
        altura_alvo (int): Altura desejada da imagem redimensionada.

    Returns:
        str: Caminho do arquivo da imagem redimensionada.
    """
    if not isinstance(largura_alvo, int) or not isinstance(altura_alvo, int):
        raise TypeError("largura_alvo e altura_alvo devem ser inteiros.")

    imagem = PIL.Image.open(nome_arquivo)
    imagem_redimensionada = imagem.resize((largura_alvo, altura_alvo))

    nome_arquivo_redimensionado = os.path.join(
        "images",
        f"redimensionada_{os.path.basename(nome_arquivo)}"
    )
    imagem_redimensionada.save(nome_arquivo_redimensionado)

    return nome_arquivo_redimensionado


def criar_atalho(arquivo_origem, pasta_destino):
    """
    Cria um atalho para o arquivo arquivo_origem na pasta pasta_destino.

    Args:
        arquivo_origem (str): Caminho do arquivo para criar um atalho.
        pasta_destino (str): Caminho da pasta onde o atalho será criado.

    Returns:
        str: Caminho do atalho criado.
    """
    nome_arquivo_origem = os.path.basename(arquivo_origem)
    atalho_destino = os.path.join(
        pasta_destino, f"atalho_{nome_arquivo_origem}")

    try:
        shutil.copy(arquivo_origem, atalho_destino)
        return atalho_destino
    except Exception as e:
        raise RuntimeError(f"Erro ao criar o atalho: {e}")


def copiar_para_area_de_transferencia(texto):
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


def show_error(title, message, traceback_text=None):
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


def realizar_backup():
    """
    Realiza o backup do banco de dados.
    """
    shutil.copyfile("users.db", "backup.db")
    sg.popup("Backup realizado com sucesso.")


def open_login_window():
    # Lógica para abrir a janela de login aqui
    # Por exemplo, exibir uma janela com campos de usuário e senha e retornar as credenciais inseridas pelo usuário
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha: ")
    return username, password


def show_janela_principal_error_popup(error_message):
    # Lógica para mostrar uma janela popup com o erro da janela principal
    print(f"Erro na janela principal: {error_message}")
