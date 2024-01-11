import PySimpleGUI as sg
import clipboard
import logging

# Constantes para mensagens de erro
ERRO_GENERICO = "Erro genérico"
ERRO_VALUE = "Erro de ValueError"
ERRO_TYPE = "Erro de TypeError"
ERRO_CAMPO_VAZIO = "Erro de Campo Vazio"
ERRO_EAN_EM_BRANCO = "Erro de EAN em Branco"
ERRO_SQLITE = "Erro de SQLite"


class ErrorHandlers:
    @staticmethod
    def handle_generic_error(error):
        """Handles generic errors."""
        error_message = str(error)
        error_name = type(error).__name__
        sg.popup_error(f"{error_name}: {error_message}", title=ERRO_GENERICO)
        ErrorHandlers.log_error(error_message)

    @staticmethod
    def handle_value_error(error):
        """Handles ValueError."""
        error_message = f"{ERRO_VALUE}: {error}"
        sg.popup_error(error_message, title=ERRO_VALUE)
        ErrorHandlers.copy_error_to_clipboard(error_message)
        sg.popup("Erro Copiado",
                 "O código de erro foi copiado para a área de transferência.")
        ErrorHandlers.log_error(error_message)

    @staticmethod
    def handle_type_error(error):
        """Handles TypeError."""
        error_message = f"{ERRO_TYPE}: {error}"
        sg.popup_error(error_message, title=ERRO_TYPE)
        ErrorHandlers.copy_error_to_clipboard(error_message)
        sg.popup("Erro Copiado",
                 "O código de erro foi copiado para a área de transferência.")
        ErrorHandlers.log_error(error_message)

    @staticmethod
    def handle_empty_error(error):
        """Handles empty field errors."""
        error_message = f"{ERRO_CAMPO_VAZIO}: {error}"
        sg.popup_error(error_message, title=ERRO_CAMPO_VAZIO)
        ErrorHandlers.copy_error_to_clipboard(error_message)
        sg.popup("Erro Copiado",
                 "O código de erro foi copiado para a área de transferência.")
        ErrorHandlers.log_error(error_message)

    @staticmethod
    def handle_blank_ean_error(error):
        """Handles blank EAN errors."""
        error_message = f"{ERRO_EAN_EM_BRANCO}: {error}"
        sg.popup_error(error_message, title=ERRO_EAN_EM_BRANCO)
        ErrorHandlers.copy_error_to_clipboard(error_message)
        sg.popup("Erro Copiado",
                 "O código de erro foi copiado para a área de transferência.")
        ErrorHandlers.log_error(error_message)

    @staticmethod
    def copy_error_to_clipboard(error_message):
        clipboard.copy(error_message)
        print("Código de erro copiado para a área de transferência:")
        print(error_message)

    @staticmethod
    def log_error(error_message):
        try:
            # Configure the logger for writing errors to a log file
            logging.basicConfig(filename="error_log.txt", level=logging.ERROR)
            logging.error(error_message)
        except Exception as e:
            print(f"Erro ao escrever no arquivo de log: {e}")

    @staticmethod
    def get_error_codes():
        return list(ErrorHandlers.error_codes.keys())


# Dicionário de códigos de erro
ErrorHandlers.error_codes = {
    1001: ErrorHandlers.handle_value_error,
    1002: ErrorHandlers.handle_type_error,
    1003: ErrorHandlers.handle_empty_error,
    1004: ErrorHandlers.handle_blank_ean_error
}
