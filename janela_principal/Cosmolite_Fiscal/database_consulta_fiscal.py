# janela_principal\Cosmolite_Fiscal\database.py
import os
import sqlite3
import json
from datetime import datetime

# Define o diretório raiz do script
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define o caminho para o arquivo do banco de dados SQLite
DB_PATH = os.path.join(ROOT_DIR, "database_consulta_fiscal.db")

# Define as constantes para os nomes dos campos na tabela historico
FIELD_GTIN = "gtin"
FIELD_DESCRIPTION = "description"
FIELD_CREATED_AT = "created_at"
FIELD_UPDATED_AT = "updated_at"

# Define a query SQL para inserir um produto na tabela historico
INSERT_PRODUTO_QUERY = """
    INSERT INTO historico (gtin, description, produto_json, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?)
"""

# Define a query SQL para atualizar um produto na tabela historico
UPDATE_PRODUTO_QUERY = """
    UPDATE historico SET {fields_values}, updated_at=? WHERE gtin=?
"""

# Define a query SQL para excluir um produto da tabela historico
DELETE_PRODUTO_QUERY = """
    DELETE FROM historico WHERE gtin=?
"""

# Define a query SQL para selecionar produtos com filtros e ordenação
SELECT_PRODUTOS_QUERY = """
    SELECT produto_json FROM historico
    WHERE {where_condition}
    ORDER BY {order_by}
"""


class Produto:
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return json.dumps(self.data)

    @classmethod
    def from_json(cls, json_data):
        data = json.loads(json_data)
        return cls(data)


class DatabaseError(Exception):
    pass


class ProdutoDAO:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_database()

    def _create_database(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute(
                    """
                    CREATE TABLE IF NOT EXISTS historico (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        gtin TEXT NOT NULL,
                        description TEXT,
                        produto_json TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
        except sqlite3.Error as ex:
            raise DatabaseError(f"Erro ao criar o banco de dados: {ex}")

    def save_produto(self, produto_data, fields_to_update=None):
        validate_produto_data(produto_data)
        produto_json = json.dumps(produto_data)
        fields_values = ", ".join(
            f"{field}=?" for field in fields_to_update) if fields_to_update else "produto_json=?"

        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                current_timestamp = datetime.now().isoformat()

                # Verifica se o produto já existe no banco pelo GTIN
                c.execute("SELECT * FROM historico WHERE gtin=?",
                          (produto_data[FIELD_GTIN],))
                row = c.fetchone()

                if row:
                    # Produto já existe, então atualiza os campos específicos
                    c.execute(UPDATE_PRODUTO_QUERY.format(
                        fields_values=fields_values), (
                        *produto_data.values(),
                        current_timestamp,
                        produto_data[FIELD_GTIN]
                    ))
                else:
                    # Produto não existe, então insere como um novo
                    c.execute(INSERT_PRODUTO_QUERY, (
                        *produto_data.values(),
                        current_timestamp,
                        current_timestamp
                    ))

        except (sqlite3.IntegrityError, sqlite3.OperationalError) as ex:
            raise DatabaseError(
                f"Erro ao salvar produto no banco de dados: {ex}")

    def delete_produto(self, gtin):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute(DELETE_PRODUTO_QUERY, (gtin,))
        except sqlite3.OperationalError as ex:
            raise DatabaseError(
                f"Erro ao excluir produto no banco de dados: {ex}")

    def load_produtos(self, filters=None, order_by="id DESC"):
        where_condition = " AND ".join(filters) if filters else "1"
        select_query = SELECT_PRODUTOS_QUERY.format(
            where_condition=where_condition,
            order_by=order_by
        )

        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute(select_query)
                rows = c.fetchall()

            return [Produto.from_json(row[0]) for row in rows] if rows else []
        except sqlite3.OperationalError as ex:
            raise DatabaseError(
                f"Erro ao carregar produtos do banco de dados: {ex}")

    def get_produtos_by_field(self, field, value):
        validate_field_name(field)
        return self.load_produtos(filters=[f"{field}=?", (value,)])

    def get_produto(self, gtin):
        produtos = self.get_produtos_by_field(FIELD_GTIN, gtin)
        return produtos[0] if produtos else None


def create_database():
    try:
        dao = ProdutoDAO(DB_PATH)
    except DatabaseError as ex:
        print(f"Erro ao criar o banco de dados: {ex}")
    else:
        print("Banco de dados criado com sucesso!")


def validate_field_name(field):
    if field not in [FIELD_GTIN, FIELD_DESCRIPTION]:
        raise ValueError(
            "Campo de filtro inválido. Utilize 'gtin' ou 'description'.")


def validate_produto_data(produto_data):
    if not isinstance(produto_data, dict):
        raise ValueError("produto_data deve ser um dicionário.")
    if FIELD_GTIN not in produto_data:
        raise ValueError("gtin é um campo obrigatório em produto_data.")
    if not isinstance(produto_data[FIELD_GTIN], str):
        raise ValueError("gtin deve ser uma string.")
    if FIELD_DESCRIPTION in produto_data and not isinstance(produto_data[FIELD_DESCRIPTION], str):
        raise ValueError("description deve ser uma string, se fornecido.")


# Executar a criação da tabela apenas quando o módulo é executado diretamente
if __name__ == "__main__":
    create_database()
