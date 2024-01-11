import sqlite3
import os
import re
import PySimpleGUI as sg

def criar_tabela():
    # Conectando ao banco de dados
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Criando tabela de empresas (se não existir)
    c.execute('''CREATE TABLE IF NOT EXISTS empresas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, endereco TEXT, telefone TEXT, email TEXT, cnpj TEXT UNIQUE)''')

    # Criando tabela de clientes (se não existir)
    c.execute('''CREATE TABLE IF NOT EXISTS clientes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, endereco TEXT, telefone TEXT, email TEXT)''')

    # Criando tabela de fornecedores (se não existir)
    c.execute('''CREATE TABLE IF NOT EXISTS fornecedores
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, endereco TEXT, telefone TEXT, email TEXT)''')

    # Criando tabela de produtos (se não existir)
    c.execute('''CREATE TABLE IF NOT EXISTS produtos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, descricao TEXT, preco REAL)''')

    # Salvando as alterações e fechando a conexão
    conn.commit()
    conn.close()

def criar_pasta_cadastro():
    # Verificar se a pasta "Cadastro de Empresa" já existe
    if not os.path.exists("Cadastro de Empresa"):
        os.mkdir("Cadastro de Empresa")
        print("Pasta 'Cadastro de Empresa' criada com sucesso.")
    else:
        print("Pasta 'Cadastro de Empresa' já existe.")

def verificar_banco_dados():
    # Verificar se o banco de dados e as tabelas foram criados
    if not os.path.exists("database.db"):
        print("Banco de dados não encontrado.")
        return

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    tabelas_necessarias = ["empresas", "clientes", "fornecedores", "produtos"]

    for tabela in tabelas_necessarias:
        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tabela}'")
        result = c.fetchone()
        if not result:
            print(f"Tabela '{tabela}' não encontrada no banco de dados.")

    conn.close()

def cadastrar_empresa():
    # Criar layout da janela de cadastro de empresa
    layout = [
        [sg.Text('Nome:'), sg.InputText(key='nome')],
        [sg.Text('Endereço:'), sg.InputText(key='endereco')],
        [sg.Text('Telefone:'), sg.InputText(key='telefone', enable_events=True, k='-TELEFONE-')],
        [sg.Text('Email:'), sg.InputText(key='email')],
        [sg.Text('CNPJ/CPF:'), sg.InputText(key='cnpjcpf', enable_events=True, k='-CNPJCPF-')],
        [sg.Submit('Cadastrar'), sg.Cancel('Cancelar')]
    ]

    window = sg.Window('Cadastro de Empresa', layout)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Cancelar'):
            window.close()
            return

        nome = values['nome']
        endereco = values['endereco']
        telefone = values['telefone']
        email = values['email']
        cnpjcpf = values['cnpjcpf']

        # Verificar se algum campo está em branco
        if not all(values.values()):
            sg.popup('Por favor, preencha todos os campos')
            continue

        # Conectando ao banco de dados
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Verificar se o CNPJ/CPF já está cadastrado
        c.execute("SELECT * FROM empresas WHERE cnpj=?", (cnpjcpf,))
        result = c.fetchone()
        if result:
            sg.popup('Empresa com CNPJ/CPF já cadastrado')
            continue

        # Inserindo os dados da empresa na tabela
        c.execute("INSERT INTO empresas (nome, endereco, telefone, email, cnpj) VALUES (?, ?, ?, ?, ?)",
                  (nome, endereco, telefone, email, cnpjcpf))

        # Salvando as alterações e fechando a conexão
        conn.commit()
        conn.close()

        sg.popup('Empresa cadastrada com sucesso')
        window.close()
        break

def listar_empresas():
    # Conectando ao banco de dados
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Verificar se a coluna 'id' existe na tabela 'empresas'
    c.execute("PRAGMA table_info(empresas)")
    columns = c.fetchall()
    has_id_column = any(column[1] == "id" for column in columns)

    if not has_id_column:
        # Criar nova tabela com a coluna 'id' e copiar os dados da tabela existente
        c.execute("BEGIN TRANSACTION")
        c.execute("CREATE TABLE empresas_new (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, endereco TEXT, telefone TEXT, email TEXT, cnpj TEXT UNIQUE)")
        c.execute("INSERT INTO empresas_new (nome, endereco, telefone, email, cnpj) SELECT nome, endereco, telefone, email, cnpj FROM empresas")
        c.execute("DROP TABLE empresas")
        c.execute("ALTER TABLE empresas_new RENAME TO empresas")
        c.execute("COMMIT")

    # Buscar todas as empresas cadastradas
    c.execute("SELECT id, nome, endereco, telefone, email, cnpj FROM empresas")
    empresas = c.fetchall()

    # Criar layout da janela de listagem de empresas
    data = [[empresa[0], empresa[1], empresa[2], empresa[3], empresa[4], empresa[5]] for empresa in empresas]

    layout = [
        [sg.Table(values=data,
                  headings=['ID', 'Nome', 'Endereço', 'Telefone', 'Email', 'CNPJ/CPF'],
                  justification='left',
                  auto_size_columns=True,
                  display_row_numbers=True,
                  key='-TABLE-')],
        [sg.Button('Editar'), sg.Button('Excluir'), sg.Button('Fechar')]
    ]

    window = sg.Window('Listagem de Empresas', layout)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Fechar'):
            break

        if event == 'Editar':
            row_index = values['-TABLE-'][0]
            if row_index:
                empresa_id = empresas[row_index-1][0]
                editar_empresa(empresa_id)

        if event == 'Excluir':
            row_index = values['-TABLE-'][0]
            if row_index:
                empresa_id = empresas[row_index-1][0]
                excluir_empresa(empresa_id)
                # Atualizar a lista de empresas
                c.execute("SELECT id, nome, endereco, telefone, email, cnpj FROM empresas")
                empresas = c.fetchall()
                data = [[empresa[0], empresa[1], empresa[2], empresa[3], empresa[4], empresa[5]] for empresa in empresas]
                window['-TABLE-'].update(values=data)

    window.close()

def editar_empresa(empresa_id):
    # Conectando ao banco de dados
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Buscar dados da empresa pelo ID
    c.execute("SELECT * FROM empresas WHERE id=?", (empresa_id,))
    empresa = c.fetchone()

    # Fechar a conexão
    conn.close()

    # Verificar se a empresa existe
    if not empresa:
        sg.popup('Empresa não encontrada')
        return

    # Extrair os dados da empresa
    empresa_id, nome, endereco, telefone, email, cnpjcpf = empresa

    # Criar layout da janela de edição de empresa
    layout = [
        [sg.Text('Nome:'), sg.InputText(nome, key='nome')],
        [sg.Text('Endereço:'), sg.InputText(endereco, key='endereco')],
        [sg.Text('Telefone:'), sg.InputText(telefone, key='telefone', enable_events=True, k='-TELEFONE-')],
        [sg.Text('Email:'), sg.InputText(email, key='email')],
        [sg.Text('CNPJ/CPF:'), sg.InputText(cnpjcpf, key='cnpjcpf', enable_events=True, k='-CNPJCPF-')],
        [sg.Submit('Salvar'), sg.Cancel('Cancelar')]
    ]

    window = sg.Window('Edição de Empresa', layout)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Cancelar'):
            window.close()
            break

        nome = values['nome']
        endereco = values['endereco']
        telefone = values['telefone']
        email = values['email']
        cnpjcpf = values['cnpjcpf']

        # Verificar se algum campo está em branco
        if not all(values.values()):
            sg.popup('Por favor, preencha todos os campos')
            continue

        # Conectando ao banco de dados
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Verificar se o CNPJ/CPF já está cadastrado por outra empresa
        c.execute("SELECT * FROM empresas WHERE cnpj=? AND id!=?", (cnpjcpf, empresa_id))
        result = c.fetchone()
        if result:
            sg.popup('Empresa com CNPJ/CPF já cadastrado')
            continue

        # Atualizar os dados da empresa no banco de dados
        c.execute("UPDATE empresas SET nome=?, endereco=?, telefone=?, email=?, cnpj=? WHERE id=?",
                  (nome, endereco, telefone, email, cnpjcpf, empresa_id))

        # Salvando as alterações e fechando a conexão
        conn.commit()
        conn.close()

        sg.popup('Empresa atualizada com sucesso')
        window.close()
        break

def excluir_empresa(empresa_id):
    # Conectando ao banco de dados
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Excluir a empresa pelo ID
    c.execute("DELETE FROM empresas WHERE id=?", (empresa_id,))

    # Salvando as alterações e fechando a conexão
    conn.commit()
    conn.close()

    sg.popup('Empresa excluída com sucesso')

def formatar_telefone(value):
    value = re.sub(r'\D', '', value)  # Remover todos os caracteres não numéricos
    if len(value) < 11:  # Telefone com 10 dígitos (fixo)
        return f'({value[:2]}) {value[2:6]}-{value[6:]}'
    else:  # Telefone com 11 dígitos (celular)
        return f'({value[:2]}) {value[2:7]}-{value[7:]}'

def formatar_cnpjcpf(value):
    value = re.sub(r'\D', '', value)  # Remover todos os caracteres não numéricos
    if len(value) == 11:  # CPF
        return f'{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:]}'
    elif len(value) == 14:  # CNPJ
        return f'{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}'
    else:
        return value

# Criar a tabela (se ainda não existir)
criar_tabela()

# Criar a pasta "Cadastro de Empresa" (se ainda não existir)
criar_pasta_cadastro()

# Verificar o banco de dados e as tabelas
verificar_banco_dados()

# Verificar se a tabela 'empresas' está vazia
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("SELECT count(*) FROM empresas")
result = c.fetchone()
conn.close()

# Se a tabela 'empresas' estiver vazia, cadastrar uma empresa
if result[0] == 0:
    cadastrar_empresa()
else:
    layout = [
        [sg.Button('Cadastrar Empresa'), sg.Button('Listar Empresas')]
    ]

    window = sg.Window('Menu Principal', layout)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Fechar'):
            break

        if event == 'Cadastrar Empresa':
            cadastrar_empresa()
        elif event == 'Listar Empresas':
            listar_empresas()

    window.close()
