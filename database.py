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

    # Verificar se a tabela já existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'")
    if not cursor.fetchone():
        # Criar tabela de clientes
        cursor.execute('''
        CREATE TABLE clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cnpj TEXT NOT NULL,
            address TEXT,
            ie TEXT,
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

    if not table_exists(cursor, 'contracts'):
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
            delivPlace TEXT,
            stateDelivPlace TEXT,
            -- SB/CO fields
            umidade_maxima TEXT,
            impureza_maxima TEXT,
            ardidos_avariados TEXT,
            -- WH fields
            falling_number TEXT,
            pl_minimo TEXT,
            ph TEXT,
            w_minimo TEXT,
            triguilho TEXT,
            -- Additional dynamic fields
            additional_fields TEXT,
            FOREIGN KEY (seller_id) REFERENCES clients (id),
            FOREIGN KEY (buyer_id) REFERENCES clients (id)
        )
        ''')
        print("Tabela 'contracts' criada com sucesso.")
    else:
        columns_to_add = [
            ('umidade_maxima', 'TEXT'),
            ('impureza_maxima', 'TEXT'),
            ('ardidos_avariados', 'TEXT'),
            ('falling_number', 'TEXT'),
            ('pl_minimo', 'TEXT'),
            ('ph', 'TEXT'),
            ('w_minimo', 'TEXT'),
            ('triguilho', 'TEXT'),
            ('additional_fields', 'TEXT')
        ]
        
        for column, col_type in columns_to_add:
            cursor.execute(f"PRAGMA table_info(contracts)")
            columns = [info[1] for info in cursor.fetchall()]
            if column not in columns:
                cursor.execute(f"ALTER TABLE contracts ADD COLUMN {column} {col_type}")
                print(f"Coluna '{column}' adicionada à tabela 'contracts'.")

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