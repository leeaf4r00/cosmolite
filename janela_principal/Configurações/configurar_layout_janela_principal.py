import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def abrir_estoque():
    print("Abrir Estoque")


def abrir_vendas():
    print("Abrir Vendas")


def abrir_cosmolite_fiscal():
    print("Abrir Cosmolite Fiscal")


def abrir_graficos():
    print("Abrir Gráficos")


def abrir_financeiro():
    print("Abrir Financeiro")


def abrir_internet():
    print("Abrir Internet")


def abrir_termos():
    print("Abrir Termos")


def abrir_utilitarios():
    print("Abrir Utilitários")


def abrir_atendimento():
    print("Abrir Atendimento")


def abrir_configuracao():
    print("Abrir Configuração")


def abrir_cadastros():
    print("Abrir Cadastros")


class BotaoArrastavel:
    def __init__(self, root, text, row, column, command):
        self.text = text
        self.command = command

        self.button = ttk.Button(root, text=self.text, command=self.command)
        self.button.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

        self.button.bind("<ButtonPress-1>", self.iniciar_arraste)
        self.button.bind("<B1-Motion>", self.arrastar)
        self.button.bind("<ButtonRelease-1>", self.finalizar_arraste)
        self.button.bind("<Button-3>", self.exibir_menu)

        self.start_x = 0
        self.start_y = 0

    def iniciar_arraste(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def arrastar(self, event):
        new_x = self.button.winfo_x() + (event.x - self.start_x)
        new_y = self.button.winfo_y() + (event.y - self.start_y)
        self.button.place(x=new_x, y=new_y)

    def finalizar_arraste(self, event):
        self.start_x = 0
        self.start_y = 0

    def exibir_menu(self, event):
        menu = tk.Menu(self.button, tearoff=0)
        menu.add_command(label="Opção 1", command=self.opcao1)
        menu.add_command(label="Opção 2", command=self.opcao2)
        menu.add_separator()
        menu.add_command(label="Opção 3", command=self.opcao3)

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def opcao1(self):
        print("Opção 1 selecionada")

    def opcao2(self):
        print("Opção 2 selecionada")

    def opcao3(self):
        print("Opção 3 selecionada")


def abrir_configuracao():
    root = tk.Tk()
    root.geometry("400x200")

    # Define a quantidade de colunas desejadas
    colunas = 4

    botao_estoque = BotaoArrastavel(root, "Estoque", 0, 0, abrir_estoque)
    botao_vendas = BotaoArrastavel(root, "Vendas", 0, 1, abrir_vendas)
    botao_cosmolite_fiscal = BotaoArrastavel(
        root, "Cosmolite Fiscal", 0, 2, abrir_cosmolite_fiscal)
    botao_graficos = BotaoArrastavel(root, "Gráficos", 0, 3, abrir_graficos)
    botao_financeiro = BotaoArrastavel(root, "Financeiro", 1, 0, abrir_financeiro)
    botao_internet = BotaoArrastavel(root, "Internet", 1, 1, abrir_internet)
    botao_termos = BotaoArrastavel(root, "Termos", 1, 2, abrir_termos)
    botao_utilitarios = BotaoArrastavel(root, "Utilitários", 1, 3, abrir_utilitarios)
    botao_atendimento = BotaoArrastavel(root, "Atendimento", 2, 0, abrir_atendimento)
    botao_configuracao = BotaoArrastavel(root, "Configuração", 2, 1, abrir_configuracao)
    botao_cadastros = BotaoArrastavel(root, "Cadastros", 2, 2, abrir_cadastros)

    # Adiciona o número de colunas desejadas com peso 1 para manter o tamanho igual
    for i in range(colunas):
        root.grid_columnconfigure(i, weight=1)

    def salvar_e_aplicar_configuracoes():
        messagebox.showinfo("Configurações", "Configurações salvas e aplicadas")

    botao_salvar_config = ttk.Button(root, text="Salvar e Aplicar Configurações",
                                     command=salvar_e_aplicar_configuracoes)
    botao_salvar_config.grid(row=3, column=0, columnspan=colunas, pady=10)

    root.mainloop()
