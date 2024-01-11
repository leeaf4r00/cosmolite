# config.py

import os
import PySimpleGUI as sg

# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho para pasta de dados
DATA_DIR = os.path.join(BASE_DIR, "dados") 

# Caminho para arquivo de histórico
HISTORICO_FILE = os.path.join(DATA_DIR, "historico.txt")

# URL da API 
API_URL = "https://api.cosmos.bluesoft.com.br/gtins/"

# Headers padrão da API
API_HEADERS = {
    "User-Agent": "MeuApp/1.0"
}

# Token da API
api_token = "SEU_TOKEN_AQUI" 

# Tema PySimpleGUI
THEME = "DarkBlue14"

# Função para trocar o token
def change_token():

  layout = [
    [sg.Text("Token atual: "), sg.Text(api_token, key="-TOKEN-")],
    [sg.Text("Novo token:"), sg.Input(key="-NEW-TOKEN-")],
    [sg.Button("Trocar"), sg.Button("Cancelar")]
  ]

  window = sg.Window("Trocar Token", layout)
  
  while True:
    event, values = window.read()

    if event == "Trocar":
      new_token = values["-NEW-TOKEN-"]
      if new_token:
        api_token = new_token
        sg.popup("Token alterado com sucesso!")
        break
      else: 
        sg.popup_error("Token inválido")

    if event == "Cancelar" or event == sg.WIN_CLOSED:
      break

  window.close()