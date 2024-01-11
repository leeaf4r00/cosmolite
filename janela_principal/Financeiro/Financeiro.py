import PySimpleGUI as sg
import subprocess

def abrir_controle_de_moedas():
    subprocess.Popen(['python', 'janela_principal/Utilitários/CONTADOR MOEDAS/contador_moedas.py'])

def abrir_controle_saidas():
    subprocess.Popen(['python', 'janela_principal/Financeiro/controle_saidas.py'])

def abrir_contas():
    subprocess.Popen(['python', 'janela_principal/Financeiro/contas.py'])

def abrir_controle_financeiro():
    subprocess.Popen(['python', 'janela_principal/controle_financeiro/relatorios_financeiro.py'])

# Layout dos botões
layout = [
    [sg.Button('Controle de Moedas', size=(20, 2))],
    [sg.Button('Controle de Saídas', size=(20, 2))],
    [sg.Button('Contas', size=(20, 2))],
    [sg.Button('Controle Financeiro', size=(20, 2))]
]

# Cria a janela com o layout
window = sg.Window('Botões Financeiros', layout)

# Loop para tratar os eventos da janela
while True:
    event, values = window.read()
    if event is None:
        break
    elif event == 'Controle de Moedas':
        abrir_controle_de_moedas()
    elif event == 'Controle de Saídas':
        abrir_controle_saidas()
    elif event == 'Contas':
        abrir_contas()
    elif event == 'Controle Financeiro':
        abrir_controle_financeiro()

# Fecha a janela ao sair do loop
window.close()
