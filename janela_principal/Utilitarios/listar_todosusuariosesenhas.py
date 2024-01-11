import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk


class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_table(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao criar tabela: {str(e)}")

    def get_all_users(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            conn.close()
            return users
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao obter usuários: {str(e)}")
            return []

    def add_user(self, username, password):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror(
                "Erro", f"Erro ao adicionar usuário: {str(e)}"
            )

    def update_user(self, user_id, password):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET password = ? WHERE id = ?", (
                    password, user_id)
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror(
                "Erro", f"Erro ao atualizar usuário: {str(e)}"
            )

    def delete_user(self, user_id):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror(
                "Erro", f"Erro ao excluir usuário: {str(e)}"
            )

    def get_user_by_id(self, user_id):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            conn.close()
            return user
        except sqlite3.Error as e:
            messagebox.showerror(
                "Erro", f"Erro ao obter usuário por ID: {str(e)}"
            )
            return None


class App(tk.Tk):
    def __init__(self, db_file):
        super().__init__()
        self.title("Lista de Usuários e Senhas")
        self.geometry("600x400")

        self.db = Database(db_file)
        self.db.create_table()
        self.user_list_window = UserListWindow(self, db_file)
        self.add_user_window = None
        self.edit_user_window = None

        add_button = tk.Button(
            self, text="Adicionar Usuário", command=self.open_add_user_window)
        add_button.pack(pady=10)

        editar_button = tk.Button(
            self, text="Editar Usuário", command=self.open_edit_user_window)
        editar_button.pack(pady=10)

        remover_button = tk.Button(
            self, text="Remover Usuário", command=self.user_list_window.remover_user)
        remover_button.pack(pady=10)

        listar_button = tk.Button(
            self, text="Listar Usuários e Senhas", command=self.user_list_window.listar_usuarios_senhas)
        listar_button.pack(pady=10)

        self.user_list_window.pack(pady=10)

    def open_add_user_window(self):
        self.add_user_window = AddUserWindow(
            self, self.db, self.user_list_window)
        self.add_user_window.grab_set()

    def open_edit_user_window(self):
        item = self.user_list_window.users_table.focus()
        if item:
            user_id = self.user_list_window.users_table.item(item, "values")[0]
            password = self.user_list_window.users_table.item(item, "values")[
                2]
            self.edit_user_window = EditUserWindow(
                self, self.db, self.user_list_window, user_id, password)
            self.edit_user_window.grab_set()


class UserListWindow(tk.Frame):
    def __init__(self, master, db_file):
        super().__init__(master)
        self.users_table = ttk.Treeview(
            self, columns=("ID", "Username", "Password"), show="headings"
        )
        self.users_table.heading("ID", text="ID")
        self.users_table.heading("Username", text="Usuário")
        self.users_table.heading("Password", text="Senha")
        self.users_table.pack(pady=10)

        self.master = master
        self.db = Database(db_file)
        self.display_users()

    def display_users(self):
        self.users_table.delete(*self.users_table.get_children())

        users = self.db.get_all_users()
        for user in users:
            user_id = user[0]
            username = user[1]
            password = user[2]
            self.users_table.insert(
                "", tk.END, values=(user_id, username, password))

    def remover_user(self):
        item = self.users_table.focus()
        if item:
            user_id = self.users_table.item(item, "values")[0]
            username = self.users_table.item(item, "values")[1]
            confirm = messagebox.askyesno(
                "Remover Usuário", f"Deseja remover o usuário '{username}' com o ID: '{user_id}'?"
            )
            if confirm:
                self.db.delete_user(user_id)
                self.display_users()

    def listar_usuarios_senhas(self):
        users = self.db.get_all_users()

        if not users:
            messagebox.showinfo(
                "Informação", "Não há usuários cadastrados.")
        else:
            info_message = ""
            for user in users:
                user_id = user[0]
                username = user[1]
                password = user[2]
                info_message += f"Usuário: {username}\nSenha: {password}\n\n"
            messagebox.showinfo("Usuários e Senhas", info_message)


class AddUserWindow(tk.Toplevel):
    def __init__(self, master, db, user_list_window):
        super().__init__(master)
        self.title("Adicionar Usuário")
        self.db = db
        self.user_list_window = user_list_window

        username_label = tk.Label(self, text="Usuário:")
        username_label.grid(row=0, column=0)

        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1)

        password_label = tk.Label(self, text="Senha:")
        password_label.grid(row=1, column=0)

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        confirm_password_label = tk.Label(self, text="Confirmar Senha:")
        confirm_password_label.grid(row=2, column=0)

        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.grid(row=2, column=1)

        save_button = tk.Button(self, text="Salvar", command=self.save_user)
        save_button.grid(row=3, column=0, columnspan=2)

    def save_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if username and password and confirm_password:
            if password == confirm_password:
                self.db.add_user(username, password)
                self.user_list_window.display_users()
                self.destroy()
            else:
                messagebox.showwarning(
                    "Senhas não coincidem", "A senha e a confirmação de senha não coincidem."
                )
        else:
            messagebox.showwarning(
                "Campos Vazios", "Preencha todos os campos antes de salvar."
            )


class EditUserWindow(tk.Toplevel):
    def __init__(self, master, db, user_list_window, user_id, current_password):
        super().__init__(master)
        self.title("Editar Usuário")
        self.db = db
        self.user_list_window = user_list_window
        self.user_id = user_id

        current_password_label = tk.Label(self, text="Senha Atual:")
        current_password_label.grid(row=0, column=0)

        self.current_password_entry = tk.Entry(self, show="*")
        self.current_password_entry.insert(0, current_password)
        self.current_password_entry.grid(row=0, column=1)

        new_password_label = tk.Label(self, text="Nova Senha:")
        new_password_label.grid(row=1, column=0)

        self.new_password_entry = tk.Entry(self, show="*")
        self.new_password_entry.grid(row=1, column=1)

        show_password_button = tk.Button(
            self, text="Mostrar Senha", command=self.show_password)
        show_password_button.grid(row=2, column=0, columnspan=2)

        save_button = tk.Button(self, text="Salvar", command=self.save_user)
        save_button.grid(row=3, column=0)

        delete_button = tk.Button(
            self, text="Excluir", command=self.delete_user)
        delete_button.grid(row=3, column=1)

    def show_password(self):
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()

        messagebox.showinfo(
            "Senhas", f"Senha Atual: {current_password}\nNova Senha: {new_password}")

    def save_user(self):
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()

        if current_password and new_password:
            self.db.update_user(self.user_id, new_password)
            self.user_list_window.display_users()
            self.destroy()
        else:
            messagebox.showwarning(
                "Campos Vazios", "Preencha todos os campos antes de salvar."
            )

    def delete_user(self):
        confirm = messagebox.askyesno(
            "Remover Usuário", f"Deseja remover o usuário com o ID: '{self.user_id}'?"
        )
        if confirm:
            self.db.delete_user(self.user_id)
            self.user_list_window.display_users()
            self.destroy()


if __name__ == "__main__":
    app = App("users.db")
    app.mainloop()
