# banco_dados.py

import sqlite3

DB_FILE = "produtos.db"

def connect():
  conn = sqlite3.connect(DB_FILE)
  return conn

def init_db():
  conn = connect()
  # cria tabelas etc
  conn.close()

def insert_historico(produto):
  conn = connect()
  cursor = conn.cursor()
  cursor.execute("INSERT INTO historico VALUES (?)", (produto,))
  conn.commit()
  conn.close()

def get_historico():
  conn = connect()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM historico")
  data = cursor.fetchall()
  conn.close()
  return data