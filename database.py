import sqlite3
import os
import json

def table_exists(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cursor.fetchone() is not None

def create_clients_db():
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    if not table_exists(cursor, 'clients'):
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
            bankName TEXT,
            agency TEXT,
            account TEXT
        )
        ''')
        print("Tabela 'clients' criada com sucesso.")
    else:
        cursor.execute("PRAGMA table_info(clients)")
        current_columns = cursor.fetchall()
        existing_columns = [column[1] for column in current_columns]
        
        expected_order = ['id', 'name', 'cnpj', 'address', 'ie', 'city', 'state', 'cep', 'bank', 'bankName', 'agency', 'account']
        
        bankname_exists = 'bankName' in existing_columns
        needs_recreation = False
        
        if not bankname_exists:
            print("Coluna 'bankName' não existe. Será adicionada na posição correta.")
            needs_recreation = True
        else:
            bankname_position = -1
            for i, column in enumerate(current_columns):
                if column[1] == 'bankName':
                    bankname_position = i
                    break
            
            expected_bankname_position = expected_order.index('bankName')
            
            if bankname_position != expected_bankname_position:
                print(f"Coluna 'bankName' está na posição {bankname_position}, mas deveria estar na posição {expected_bankname_position}.")
                needs_recreation = True
            else:
                print("Tabela 'clients' já está com a estrutura correta.")
        
        if needs_recreation:
            print("Recriando tabela 'clients' com ordem correta das colunas...")
            
            cursor.execute("SELECT * FROM clients")
            existing_data = cursor.fetchall()
            
            cursor.execute("ALTER TABLE clients RENAME TO clients_backup")
            
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
                bankName TEXT,
                agency TEXT,
                account TEXT
            )
            ''')
            
            old_column_names = [col[1] for col in current_columns]
            
            column_mapping = []
            for new_col in expected_order:
                if new_col in old_column_names:
                    column_mapping.append(old_column_names.index(new_col))
                else:
                    column_mapping.append(None)
            
            for row in existing_data:
                new_row = []
                for col_index in column_mapping:
                    if col_index is not None:
                        new_row.append(row[col_index])
                    else:
                        new_row.append(None)
                
                placeholders = ','.join(['?' for _ in new_row])
                cursor.execute(f"INSERT INTO clients VALUES ({placeholders})", new_row)
            
            cursor.execute("DROP TABLE clients_backup")
            print("Tabela 'clients' recriada com sucesso na ordem correta.")

    conn.commit()
    conn.close()

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
            commission TEXT,
            umidade_maxima TEXT,
            impureza_maxima TEXT,
            ardidos_avariados TEXT,
            falling_number TEXT,
            pl_minimo TEXT,
            ph TEXT,
            w_minimo TEXT,
            triguilho TEXT,
            additional_fields TEXT,
            FOREIGN KEY (seller_id) REFERENCES clients (id),
            FOREIGN KEY (buyer_id) REFERENCES clients (id)
        )
        ''')
        print("Tabela 'contracts' criada com sucesso.")
    else:
        # Verificar e adicionar colunas ausentes
        cursor.execute("PRAGMA table_info(contracts)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        columns_to_add = [
            ('additional_fields', 'TEXT'), ('commission', 'TEXT')
        ]
        
        for column, col_type in columns_to_add:
            if column not in existing_columns:
                cursor.execute(f"ALTER TABLE contracts ADD COLUMN {column} {col_type}")
                print(f"Coluna '{column}' adicionada à tabela 'contracts'.")

    conn.commit()
    conn.close()

# Inicialização dos bancos de dados
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