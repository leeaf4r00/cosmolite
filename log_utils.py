import sys
import logging
import os
import threading
import time
from collections import defaultdict
from logging.handlers import TimedRotatingFileHandler


class LogWindowUpdater(threading.Thread):
    """Classe que atualiza a janela de log em uma thread separada."""

    def __init__(self, log_window, log_file, should_exit_event):
        super().__init__()
        self.log_window = log_window
        self.log_file = log_file
        self.should_exit_event = should_exit_event

    def run(self):
        """Executa o loop de atualização da janela de log."""
        try:
            while not self.should_exit_event.is_set():
                with open(self.log_file, "r") as f:
                    log_lines = f.readlines()

                log_by_dates = defaultdict(list)
                for line in log_lines:
                    if line.startswith("["):
                        date = line.split("]")[0].strip("[]")
                        log_by_dates[date].append(line)
                    else:
                        log_by_dates[""].append(line)

                log_text = ""
                for date, records in log_by_dates.items():
                    if date:
                        log_text += f"[{date}]\n"
                    log_text += "".join(records) + "\n"

                self.log_window.update_log(log_text)

                time.sleep(0.1)
        except FileNotFoundError:
            time.sleep(0.1)
        except Exception as exception:
            self.log_window.logger.error(
                "Ocorreu um erro durante a atualização do log: %s", str(exception), exc_info=True)


class LogController:
    """Classe que controla o processo de logging."""

    def __init__(self):
        self.log_directory = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(self.log_directory, "log.txt")
        self.log_window = None
        self.should_exit_event = threading.Event()
        self.logger = None

    def set_log_window(self, log_window):
        """Define a janela de log."""
        self.log_window = log_window

    def start_logging(self):
        """Inicia o processo de logging."""
        self._setup_logging()

        check_and_delete_old_logs(self.log_directory)

        self.log_window.create_window()

        log_thread = LogWindowUpdater(self.log_window, self.log_file, self.should_exit_event)
        log_thread.daemon = True
        log_thread.start()

        self.log_window.run()

    def stop_logging(self):
        """Para o processo de logging."""
        self.should_exit_event.set()

    def generate_report(self):
        """Gera um relatório."""
        if self.validate_fields():
            self.logger.info("Relatório gerado")

    def export_data(self):
        """Exporta os dados."""
        if self.validate_fields():
            self.logger.info("Dados exportados")

    def on_window_close(self):
        """Callback chamado quando a janela é fechada."""
        self.stop_logging()

    def _setup_logging(self):
        """Configuração inicial do logging."""
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(sys.stdout),
                TimedRotatingFileHandler(
                    self.log_file, when="midnight", backupCount=30)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def validate_fields(self):
        """Valida os campos antes de registrar as mensagens de log."""
        if self.log_window.text.get("1.0", "end-1c").strip() == "":
            self.logger.error("Os campos não podem estar vazios.")
            return False
        return True


def check_and_delete_old_logs(log_directory: str) -> None:
    """Verifica e exclui arquivos de log antigos."""
    logs = [f for f in os.listdir(log_directory) if f.endswith('.txt')]

    current_time = time.time()
    thirty_days_ago = current_time - 30 * 24 * 60 * 60

    for log in logs:
        log_path = os.path.join(log_directory, log)
        if os.path.isfile(log_path) and os.path.getmtime(log_path) < thirty_days_ago:
            os.remove(log_path)
