import os
import subprocess
import random
import PySimpleGUI as sg
import requests
import webbrowser
import clipboard
import sys
import asyncio
import aiohttp
import cachetools
import csv
import json
import locale
import operator
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime
from typing import Dict, List, Optional

sg.theme('DarkBlue14')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["ROOT_DIR"] = ROOT_DIR

janela_principal_dir = os.path.join(os.environ["ROOT_DIR"], "janela_principal")

if janela_principal_dir not in sys.path:
    sys.path.append(janela_principal_dir)

API_DIR = os.path.join(ROOT_DIR, "api")
HISTORICO_DIR = os.path.join(ROOT_DIR, "historico")
HISTORICO_FILE = os.path.join(HISTORICO_DIR, "historico_data.txt")
VENDAS_DIR = os.path.join(ROOT_DIR, "vendas")
TERMS_DIR = os.path.join(ROOT_DIR, "termos")
CONTROLE_ESTOQUE_DIR = os.path.join(
    janela_principal_dir, "Vendas", "database_cadastro_produtos.py")

sg.theme('DarkBlue14')

pagina_atual = 1
itens_por_pagina = 5

layout = [
    [sg.Text("Escolha o tipo de pesquisa:"), sg.Radio("Código de barras", "RADIO1", default=True, key="-EAN-"),
     sg.Radio("Descrição", "RADIO1", key="-DESC-")],
    [sg.Text("Insira o código EAN ou descrição do produto:"), sg.Input(
        key="-SEARCH-"), sg.Button("Buscar", bind_return_key=True)],
    [sg.Multiline("", size=(100, 8), key="-RETORNO-",
                  font=("Helvetica", 10), auto_size_text=True)],
    [sg.Text("Histórico:")],
    [sg.Listbox([], size=(100, 10), key="-HISTORICO-",
                font=("Helvetica", 10), enable_events=True, auto_size_text=True)],
    [sg.Text("Token da API Cosmos:"), sg.Text("", size=(30, 1), key="-TOKEN-"),
     sg.Button("Trocar Token Cosmos", key="-CHANGE-TOKEN-")],
    [sg.Text("Software Licenciado e Desenvolvido por Rafael Moreira Fernandes | Todos Direitos Reservados ©", font=(
        "Helvetica", 10, "underline"), text_color="white", background_color="red")],
    [sg.Button("Instagram", font=("Helvetica", 10, "underline"), button_color=("white", "purple"), key="-INSTAGRAM-"),
     sg.Button("Whatsapp", font=("Helvetica", 10, "underline"),
               button_color=("white", "green"), key="-WHATSAPP-"),
     sg.Button("Copiar resultado", font=("Helvetica", 10), key="-COPY-"),
     sg.Button("Relatórios Fiscais", font=(
         "Helvetica", 10), key="-RELATORIOS-FISCAIS-"),
     sg.Button("Cadastro de Produto", font=("Helvetica", 10), key="-CADASTRO-")],
    [sg.Text("Tenha controle total de seu negócio e acessando as informações de qualquer lugar e a qualquer hora.")],
    [sg.Button("TERMOS DE USO", font=(
        "Helvetica", 10, "underline"), key="-TERMS-")],
    [sg.Button("Sair", font=("Helvetica", 10), button_color=("white", "red"))],
    [sg.Button("Favoritar Produto", font=("Helvetica", 10), key="-FAVORITAR-"),
     sg.Button("Reconsultar Produto", font=("Helvetica", 10), key="-RECONSULTAR-")]
]

window = sg.Window("Consulta de Produto", layout, size=(
    1000, 700), resizable=True, finalize=True)

API_URL = 'https://api.cosmos.bluesoft.com.br/gtins/'
API_HEADERS = {
    'X-Cosmos-Token': 'UJTBhybMZx96n33FzUfp2w',
    'User-Agent': 'API Request'
}

historico = []
cache = cachetools.LRUCache(maxsize=100)
token = 'UJTBhybMZx96n33FzUfp2w'

def feedback_mensagem(mensagem):
    window["-RETORNO-"].update(mensagem)
    window.refresh()

def check_create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def load_historico():
    global historico
    try:
        with open(HISTORICO_FILE, 'r') as f:
            historico_data = [line.strip() for line in f.readlines()]
            historico = [eval(d) for d in historico_data]
            historico.sort(key=operator.itemgetter(
                "data_consulta"), reverse=True)
            for produto in historico:
                cache[produto["gtin"]] = produto
    except FileNotFoundError:
        pass

def salvar_consulta(produto):
    produto["data_consulta"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historico.append(produto)
    historico.sort(key=operator.itemgetter("data_consulta"), reverse=True)
    save_historico()
    update_historico_display()

def save_historico():
    with open(HISTORICO_FILE, 'w') as f:
        for d in historico:
            f.write(str(d) + '\n')

class Produto:
    def __init__(self, gtin, description, ncm, price, quantity, avg_price, brand_name, gpc_code, gpc_description, gross_weight, height, length, max_price, net_weight, thumbnail, width, data_consulta):
        self.gtin = gtin
        self.description = description
        self.ncm = ncm
        self.price = price
        self.quantity = quantity
        self.avg_price = avg_price
        self.brand_name = brand_name
        self.gpc_code = gpc_code
        self.gpc_description = gpc_description
        self.gross_weight = gross_weight
        self.height = height
        self.length = length
        self.max_price = max_price
        self.net_weight = net_weight
        self.thumbnail = thumbnail
        self.width = width
        self.data_consulta = data_consulta

    def __str__(self):
        return f"Produto: {self.description}, Código EAN: {self.gtin}"

async def fetch_produto(gtin):
    produto = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{API_URL}{gtin}.json', headers=API_HEADERS) as response:
                response.raise_for_status()
                produto = await response.json()
    except aiohttp.ClientError as e:
        feedback_mensagem(f'Erro ao consultar o produto: {str(e)}')
    return produto

def consultar_produto(gtin):
    produto = None
    feedback_mensagem("Realizando consulta...")
    if gtin in cache:
        produto = cache[gtin]
        feedback_mensagem("Produto encontrado no cache.")
    else:
        produto_data = fetch_produto(gtin)
        if produto_data:
            produto = Produto(
                gtin=gtin,
                description=produto_data.get('description'),
                ncm=produto_data.get('ncm'),
                price=produto_data.get('price'),
                quantity=produto_data.get('quantity'),
                avg_price=produto_data.get('avg_price'),
                brand_name=produto_data.get('brand_name'),
                gpc_code=produto_data.get('gpc_code'),
                gpc_description=produto_data.get('gpc_description'),
                gross_weight=produto_data.get('gross_weight'),
                height=produto_data.get('height'),
                length=produto_data.get('length'),
                max_price=produto_data.get('max_price'),
                net_weight=produto_data.get('net_weight'),
                thumbnail=produto_data.get('thumbnail'),
                width=produto_data.get('width'),
                data_consulta=produto_data.get('consulta_data'))
            cache[gtin] = produto
            salvar_consulta(produto)
    return produto

def buscar_produto(search_term, search_type):
    feedback_mensagem("Iniciando consulta...")
    if search_type == "Código de barras":
        return consultar_produto(search_term)
    elif search_type == "Descrição":
        return next((p for p in historico if p.get('description') == search_term), None)
    return None

def format_produto(produto):
    if not produto:
        return "Produto não encontrado na API."
    data_consulta = datetime.strptime(
        produto.data_consulta, "%Y-%m-%d %H:%M:%S")
    formatted_date = data_consulta.strftime("%d/%m/%Y %H:%M:%S")
    return f"Produto: {produto.description}\nCódigo EAN: {produto.gtin}\nNCM: {produto.ncm}\nPreço: R${produto.price}\nQuantidade: {produto.quantity}\nPreço Médio: R${produto.avg_price}\nMarca: {produto.brand_name}\nGPC Code: {produto.gpc_code}\nGPC Descrição: {produto.gpc_description}\nPeso Bruto: {produto.gross_weight} kg\nAltura: {produto.height} cm\nComprimento: {produto.length} cm\nPreço Máximo Sugerido: R${produto.max_price}\nPeso Líquido: {produto.net_weight} kg\nData da Consulta: {formatted_date}"

def update_historico_display():
    window["-HISTORICO-"].update(values=[str(p) for p in historico])

def reset_gui():
    window["-RETORNO-"].update("")
    window["-SEARCH-"].update("")
    window["-HISTORICO-"].update("")
    window["-TOKEN-"].update(token)
    feedback_mensagem("")

def open_terms():
    terms_path = os.path.join(TERMS_DIR, "termos_uso.txt")
    if os.path.exists(terms_path):
        webbrowser.open(terms_path)
    else:
        feedback_mensagem("Arquivo de termos de uso não encontrado.")

def change_token_cosmos():
    new_token = sg.popup_get_text("Insira o novo Token Cosmos:")
    if new_token:
        global token
        token = new_token
        window["-TOKEN-"].update(token)
        feedback_mensagem("Token Cosmos atualizado.")
    else:
        feedback_mensagem("Token Cosmos não foi atualizado.")

def open_instagram():
    webbrowser.open("https://www.instagram.com/rafael.m.fernandes/")

def open_whatsapp():
    webbrowser.open("https://wa.me/5521981163000")

def copy_to_clipboard(text):
    clipboard.copy(text)
    feedback_mensagem("Resultado copiado para a área de transferência.")

def exit_application():
    save_historico()
    window.close()

def show_reports():
    os.system("python relatorios_fiscais.py")

def favorite_product(gtin):
    if gtin in cache:
        feedback_mensagem("Produto adicionado aos favoritos.")
        favorite_file = os.path.join(ROOT_DIR, "favoritos.txt")
        with open(favorite_file, 'a') as f:
            f.write(gtin + '\n')
    else:
        feedback_mensagem(
            "O produto não foi encontrado e não pode ser adicionado aos favoritos.")

def handle_event(event, values):
    global pagina_atual
    global token
    if event == sg.WIN_CLOSED:
        exit_application()
    elif event == "-INSTAGRAM-":
        open_instagram()
    elif event == "-WHATSAPP-":
        open_whatsapp()
    elif event == "-TERMS-":
        open_terms()
    elif event == "-CHANGE-TOKEN-":
        change_token_cosmos()
    elif event == "-COPY-":
        copy_to_clipboard(values["-RETORNO-"])
    elif event == "-RELATORIOS-FISCAIS-":
        show_reports()
    elif event == "-CADASTRO-":
        os.system(
            f'python {CONTROLE_ESTOQUE_DIR}')
    elif event == "-FAVORITAR-":
        gtin = values["-SEARCH-"]
        favorite_product(gtin)
    elif event == "-RECONSULTAR-":
        reset_gui()
    elif event == "Buscar":
        search_term = values["-SEARCH-"].strip()
        search_type = "-EAN-" if values["-EAN-"] else "-DESC-"
        produto = buscar_produto(search_term, search_type)

        if not produto:
            feedback_mensagem("Produto não encontrado na API.")
        else:
            result = format_produto(produto)
            feedback_mensagem(result)

def main():
    check_create_folder(API_DIR)
    check_create_folder(HISTORICO_DIR)
    check_create_folder(VENDAS_DIR)
    check_create_folder(TERMS_DIR)
    load_historico()
    window["-TOKEN-"].update(token)
    while True:
        event, values = window.read()
        handle_event(event, values)

if __name__ == '__main__':
    main()
