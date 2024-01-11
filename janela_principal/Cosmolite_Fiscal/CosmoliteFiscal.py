import PySimpleGUI as sg
import subprocess
import os


def exibir_opcoes():
    # Define the layout of the window
    layout = [
        [sg.Button("Consultar Produtos Fiscais")],
        [sg.Button("Informações Fiscais")]
    ]

    # Create the window
    window = sg.Window('Cosmolite Fiscal', layout)

    # Loop for interacting with the window
    while True:
        event, values = window.read()
        if event is None:
            break
        elif event == 'Consultar Produtos Fiscais':
            # Call the function in "consultar_produtos_fiscais.py" using subprocess.run()
            arquivo = os.path.join(
                'janela_principal', 'Cosmolite_Fiscal', 'consultar_produtos_fiscais.py')
            subprocess.run(["python", arquivo])
        elif event == 'Informações Fiscais':
            # Put your desired code to open the "Informações Fiscais" window here
            print('Opening Informações Fiscais')

    # Close the window when exiting the loop
    window.close()


# Call the function to display the options of Cosmolite Fiscal
exibir_opcoes()
