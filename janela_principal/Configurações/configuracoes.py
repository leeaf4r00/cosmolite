import os
import PySimpleGUI as sg

def criar_pasta_configuracoes():
    if not os.path.exists("Configurações"):
        os.makedirs("Configurações")

def criar_arquivos_configuracoes():
    configuracoes = [
        "Geral",
        "Estoque",
        "Etiquetas",
        "Contas a Receber",
        "Cobrança Bancária",
        "Tabela de preços",
        "Orçamentos",
        "Rede",
        "Ponto de venda",
        "Comprovante de venda",
        "Senhas de usuários",
        "Códigos de Barras",
        "Pedidos de Compras",
        "Nota Fiscal",
        "Internet",
        "Cartão de Crédito",
        "Tipos de Clientes",
        "Atendimentos",
        "Funcionários",
        "Módulos",
        "Temas"
    ]

    for configuracao in configuracoes:
        with open(f"Configurações/{configuracao}.txt", "w") as file:
            file.write(f"Arquivo de configuração para {configuracao}")

def verificar_arquivos_configuracoes():
    configuracoes = [
        "Geral",
        "Estoque",
        "Etiquetas",
        "Contas a Receber",
        "Cobrança Bancária",
        "Tabela de preços",
        "Orçamentos",
        "Rede",
        "Ponto de venda",
        "Comprovante de venda",
        "Senhas de usuários",
        "Códigos de Barras",
        "Pedidos de Compras",
        "Nota Fiscal",
        "Internet",
        "Cartão de Crédito",
        "Tipos de Clientes",
        "Atendimentos",
        "Funcionários",
        "Módulos",
        "Temas"
    ]

    for configuracao in configuracoes:
        if not os.path.exists(f"Configurações/{configuracao}.txt"):
            return False

    return True

def abrir_janela_configuracoes():
    criar_pasta_configuracoes()
    if not verificar_arquivos_configuracoes():
        criar_arquivos_configuracoes()

    if __name__ == "__main__":
        sg.popup("Arquivos de configuração criados com sucesso!")

# Lista de configurações
configuracoes = [
    "Geral",
    "Estoque",
    "Etiquetas",
    "Contas a Receber",
    "Cobrança Bancária",
    "Tabela de preços",
    "Orçamentos",
    "Rede",
    "Ponto de venda",
    "Comprovante de venda",
    "Senhas de usuários",
    "Códigos de Barras",
    "Pedidos de Compras",
    "Nota Fiscal",
    "Internet",
    "Cartão de Crédito",
    "Tipos de Clientes",
    "Atendimentos",
    "Funcionários",
    "Módulos",
    "Temas"
]

# Criação dos botões do layout
botoes_configuracoes = [[sg.Button(button, size=(15, 1))] for button in configuracoes]

# Layout da janela de configurações
layout_configuracoes = [
    [sg.Text("Configurações", font=("Helvetica", 18, 'bold'))],
    [sg.Text("Selecione uma configuração:", font=("Helvetica", 12))],
] + botoes_configuracoes  # Adiciona os botões ao layout

window_configuracoes = sg.Window("Configurações", layout_configuracoes, finalize=True)

while True:
    event, values = window_configuracoes.read()

    if event is None:
        break

    if event in configuracoes:
        # Lógica para ação ao clicar em um botão de configuração
        sg.popup(f"Botão '{event}' pressionado.")

window_configuracoes.close()
