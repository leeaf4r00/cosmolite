# api_client.py

import requests
import os
import sqlite3

class ApiClient:
    def __init__(self, token):
        self.API_URL = 'https://api.cosmos.bluesoft.com.br/gtins/'
        self.API_HEADERS = {
            'X-Cosmos-Token': token,
            'User-Agent': 'API Request'
        }

    def consultar_produto(self, gtin):
        try:
            r = requests.get(f'{self.API_URL}{gtin}.json', headers=self.API_HEADERS)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            return f'Erro ao consultar o produto: {str(e)}'

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                produto TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def insert_historico(self, data, produto):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO historico (data, produto) VALUES (?, ?)', (data, produto))

        conn.commit()
        conn.close()

    def get_historico(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT data, produto FROM historico ORDER BY id DESC LIMIT 10')
        historico = cursor.fetchall()

        conn.close()
        return historico
