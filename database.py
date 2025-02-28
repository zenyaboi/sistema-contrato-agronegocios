import sqlite3
import os

# Verificar se uma tabela já existe no banco de dados
def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cursor.fetchone() is not None

# Criar banco de dados para clientes
def create_clients_db():
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    # Verificar se a tabela de clientes já existe
    if not table_exists(cursor, 'clients'):
        # Criar tabela de clientes
        cursor.execute('''
        CREATE TABLE clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cnpj TEXT NOT NULL,
            address TEXT,
            city TEXT,
            state TEXT,
            cep TEXT,
            bank TEXT,
            agency TEXT,
            account TEXT
        )
        ''')
        print("Tabela 'clients' criada com sucesso.")
    else:
        print("Tabela 'clients' já existe.")

    conn.commit()
    conn.close()

# Criar banco de dados para contratos
def create_contracts_db():
    conn = sqlite3.connect('contracts.db')
    cursor = conn.cursor()

    # Verificar se a tabela de contratos já existe
    if not table_exists(cursor, 'contracts'):
        # Criar tabela de contratos
        cursor.execute('''
        CREATE TABLE contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_number TEXT NOT NULL,
            contract_type TEXT NOT NULL,
            contract_date TEXT NOT NULL,
            seller_id INTEGER,
            buyer_id INTEGER,
            product TEXT,
            harvest TEXT,
            quantity TEXT,
            price TEXT,
            payment TEXT,
            weight_quality TEXT,
            delivery TEXT,
            observations TEXT,
            FOREIGN KEY (seller_id) REFERENCES clients (id),
            FOREIGN KEY (buyer_id) REFERENCES clients (id)
        )
        ''')
        print("Tabela 'contracts' criada com sucesso.")
    else:
        print("Tabela 'contracts' já existe.")

    conn.commit()
    conn.close()

# Verificar se os arquivos dos bancos de dados já existem
if not os.path.exists('clients.db'):
    print("Banco de dados 'clients.db' não encontrado. Criando...")
    create_clients_db()
else:
    print("Banco de dados 'clients.db' já existe. Verificando tabelas...")
    create_clients_db()

if not os.path.exists('contracts.db'):
    print("Banco de dados 'contracts.db' não encontrado. Criando...")
    create_contracts_db()
else:
    print("Banco de dados 'contracts.db' já existe. Verificando tabelas...")
    create_contracts_db()