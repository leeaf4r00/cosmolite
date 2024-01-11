# botoes_janela_principal.py

import tkinter as tk
from tkinter import ttk

# Constantes 
COLUNAS = 4  
LINHAS = 3

# Botões mapeados para funções 
BOTOES = {
  "Estoque": abrir_estoque,
  "Vendas": abrir_vendas,
  # etc...
}

class BotaoArrastavel():

  def __init__(self, root, texto, linha, coluna, comando):
    # Inicialização e configuração
    
  # Restante dos métodos...

def configurar_grid(root):
  # Cria as linhas e colunas
  for i in range(COLUNAS):
    root.grid_columnconfigure(i, weight=1)  

  for i in range(LINHAS):
    root.grid_rowconfigure(i, weight=1)

def criar_botoes(root):
  for linha in range(LINHAS):
    for coluna in range(COLUNAS):
      texto = list(BOTOES.keys())[linha*COLUNAS + coluna] 
      comando = BOTOES[texto]
      botao = BotaoArrastavel(root, texto, linha, coluna, comando)

def main():
  root = tk.Tk()
  configurar_grid(root)
  criar_botoes(root)

  root.mainloop()

if __name__ == "__main__":
  main()