import PySimpleGUI as sg

# Definir os temas disponíveis
THEMES = {
    "Padrão": "DefaultNoMoreNagging",
    "Azul Escuro": "DarkBlue3",
    "Cinza": "SystemDefault",
    "Verde": "GreenMono",
    "Roxo": "Purple",
}

# Definir o layout do rodapé
footer_layout = [
    [sg.Text("Sistema CosmoLite versão 1.0",
             font=("Helvetica", 10), pad=(10, 0))],
    [sg.Text("Desenvolvido por Rafael Moreira Fernandes, Rurópolis - PA",
             font=("Helvetica", 10), pad=(10, 10))]
]

# Definir o layout padrão da janela
default_layout = [
    [sg.Column(footer_layout, element_justification="left")]
]

# Criar a janela principal
main_layout = [
    [sg.Menu([['Preferências', ['Alterar Tema']]])],
    [sg.Text("Janela Principal", font=("Helvetica", 16),
             justification="center", pad=(10, 10))],
    [sg.Button("Abrir Janela de Preferências",
               key="-PREFERENCES-", size=(30, 2))],
    [sg.Button("Fechar", key="-CLOSE-", size=(10, 2))]
]
main_window = sg.Window("Sistema Principal", main_layout)

# Função para alterar o tema
def alterar_tema(selected_theme, window):
    sg.theme(THEMES[selected_theme])
    window.read(timeout=0)  # Atualizar a janela

# Loop para ler os eventos da janela principal
while True:
    event, values = main_window.read()

    if event == sg.WINDOW_CLOSED or event == "-CLOSE-":
        break

    if event == "-PREFERENCES-":
        theme_layout = [
            [sg.Text("Selecione um tema:", font=("Helvetica", 14), pad=(10, 10))],
            [sg.Listbox(list(THEMES.keys()), size=(
                30, len(THEMES)), key="-THEME_LIST-")],
            [sg.Button("OK"), sg.Button("Cancelar")]
        ]
        theme_window = sg.Window("Selecionar Tema", theme_layout)

        while True:
            event, values = theme_window.read()

            if event == sg.WINDOW_CLOSED or event == "Cancelar":
                break

            if event == "OK":
                selected_theme = values["-THEME_LIST-"][0]
                alterar_tema(selected_theme, main_window)
                theme_window.close()
                break

main_window.close()
