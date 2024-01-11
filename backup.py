import PySimpleGUI as sg
import sqlite3
import shutil

sg.set_options(font=("Helvetica", 12))

# Conexão com o banco de dados
conn = sqlite3.connect("users.db")

# Função para realizar o backup
def realizar_backup():
    shutil.copyfile("users.db", "backup.db")
    sg.popup("Backup realizado com sucesso.")

# Função para ler o arquivo de backup
def ler_backup():
    try:
        conn_backup = sqlite3.connect("backup.db")
        cursor = conn_backup.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        for row in data:
            print(row)
        conn_backup.close()
    except sqlite3.Error as e:
        sg.popup("Erro ao ler o arquivo de backup:", str(e))

# Função para abrir a janela principal
def abrir_janela_principal():
    layout_principal = [
        [sg.Button("Realizar Backup"), sg.Button("Ler Backup")],
        [sg.Text("Desenvolvido por Rafael Moreira Fernandes | Todos os Direitos Reservados.", font=("Helvetica", 12), justification='center', size=(40, 1), key='-FOOTER-', relief=sg.RELIEF_SUNKEN)],
    ]

    window_principal = sg.Window("Backup", layout_principal, finalize=True)

    while True:
        event, values = window_principal.read()

        if event == sg.WINDOW_CLOSED:
            break

        # Executar a função correspondente ao botão pressionado
        if event == "Realizar Backup":
            realizar_backup()
        elif event == "Ler Backup":
            ler_backup()

    window_principal.close()

# Fechamento da conexão com o banco de dados
try:
    abrir_janela_principal()
finally:
    conn.close()
