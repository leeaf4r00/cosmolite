import sqlite3

DB_FILE = 'users.db'

conn = sqlite3.connect(DB_FILE)

def get_users():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    return cur.fetchall()

def add_user(username, password):
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                (username, password))
    conn.commit()

# outras funções de banco de dados