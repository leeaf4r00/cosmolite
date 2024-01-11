import tkinter as tk
import subprocess


def imprimir_relatorio_moedas():
    caminho = "janela_principal\\Utilitários\\CONTADOR MOEDAS\\imprimir_relatorio_moedas.py"
    subprocess.run(["python", caminho])


def relatorio_de_vendas():
    caminho = "janela_principal\\Vendas\\Listagem de Vendas\\relatorio_de_vendas.py"
    print("Caminho:", caminho)


def relatorio_financeiro():
    caminho = "janela_principal\\controle_financeiro\\controle_financeiro.py"
    print("Caminho:", caminho)


def mostrar_botoes():
    botoes_frame.pack()


janela = tk.Tk()

botao_mostrar = tk.Button(
    janela, text="Mostrar Relatórios", command=mostrar_botoes)
botao_mostrar.pack()

botoes_frame = tk.Frame(janela)

botao1 = tk.Button(botoes_frame, text="Imprimir Relatório de Moedas",
                   command=imprimir_relatorio_moedas)
botao1.pack()

botao2 = tk.Button(botoes_frame, text="Relatório de Vendas",
                   command=relatorio_de_vendas)
botao2.pack()

botao3 = tk.Button(botoes_frame, text="Relatório Financeiro",
                   command=relatorio_financeiro)
botao3.pack()

janela.mainloop()
