import tkinter as tk
from tkinter import scrolledtext, Button, messagebox

class LogWindow:
    """Classe que representa a janela de log."""

    def __init__(self, log_controller):
        self.window = None
        self.log_controller = log_controller
        self.logger = None

    def create_window(self):
        """Cria a janela de log."""
        self.window = tk.Tk()
        self.window.title("Log - Cosmolite")

        log_label = tk.Label(
            self.window, text="Relatórios e Logs", font=("Helvetica", 18, 'bold'))
        log_label.pack()

        self.text = scrolledtext.ScrolledText(
            self.window, width=80, height=20, background='white', foreground='black')
        self.text.pack()

        clear_button = Button(self.window, text="Limpar", command=self.clear_log)
        clear_button.pack()

        generate_button = Button(
            self.window, text="Gerar Relatório", command=self.generate_report)
        generate_button.pack()

        export_button = Button(
            self.window, text="Exportar Dados", command=self.export_data)
        export_button.pack()

        copy_button = Button(
            self.window, text="Copiar Log de Erros", command=self.copy_error_log)
        copy_button.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.logger = self.log_controller.logger

    def clear_log(self):
        """Limpa o log exibido na janela."""
        self.text.delete('1.0', tk.END)

    def generate_report(self):
        """Gera um relatório."""
        if self.validate_fields():
            self.log_controller.generate_report()

    def export_data(self):
        """Exporta os dados."""
        if self.validate_fields():
            self.log_controller.export_data()

    def copy_error_log(self):
        """Copia o log de erros para a área de transferência."""
        error_log = self.get_error_log()
        if error_log:
            self.window.clipboard_clear()
            self.window.clipboard_append(error_log)
            messagebox.showinfo("Log - Cosmolite", "Log de erros copiado para a área de transferência.")

    def on_close(self):
        """Lida com o fechamento da janela."""
        self.log_controller.on_window_close()
        self.window.destroy()

    def update_log(self, log_text):
        """Atualiza o log exibido na janela."""
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, log_text)

    def validate_fields(self):
        """Verifica se os campos não estão vazios."""
        if self.text.get("1.0", tk.END).strip() == "":
            self.logger.error("Os campos não podem estar vazios.")
            return False
        return True

    def get_error_log(self):
        """Obtém o log de erros."""
        log_text = self.text.get("1.0", tk.END)
        error_log = ""
        for line in log_text.split("\n"):
            if line.startswith("ERROR"):
                error_log += line + "\n"
        return error_log

    def run(self):
        """Inicia o loop principal da janela."""
        self.window.mainloop()
