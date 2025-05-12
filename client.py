from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QLineEdit, 
                             QComboBox, QTableWidget, QHBoxLayout, QFormLayout, QTextEdit, QStackedWidget)
import sqlite3
from database import create_clients_db
import os

if not os.path.exists('clients.db'):
    print("Banco de dados 'clients.db' não encontrado. Criando...")
    create_clients_db()
else:
    print("Banco de dados 'clients.db' já existe. Verificando tabelas...")

class ThirdWindow(QWidget):
    def __init__(self):
        super().__init__()

        # setting the window size
        width = 640
        height = 480

        # setting a fixed size for the app (unable to resize)
        self.setFixedSize(width, height)

        # window title
        self.setWindowTitle("Clientes")

        # layout
        layout = QVBoxLayout()

        btnAdd = QPushButton("Adicionar Cliente")
        btnEdit = QPushButton("Editar Cliente")
        btnExit = QPushButton("Sair da Janela")

        layout.addWidget(btnAdd)
        layout.addWidget(btnEdit)
        layout.addWidget(btnExit)

        btnAdd.clicked.connect(self.addClient)
        btnEdit.clicked.connect(self.editClient)
        btnExit.clicked.connect(self.close)

        self.setLayout(layout)
    
    def addClient(self):
        # Abrir janela para adicionar cliente
        self.client_window = AddClientWindow()
        self.client_window.show()

    def editClient(self):
        # Abrir janela para editar cliente (implementar lógica)
        QMessageBox.information(self, "Editar Cliente", "Funcionalidade em desenvolvimento.")

class AddClientWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Adicionar Cliente")
        self.setFixedSize(400, 500)

        # Layout
        layout = QFormLayout()

        # Nome
        self.txtName = QLineEdit(self)
        layout.addRow("Nome:", self.txtName)

        # CNPJ
        self.txtCNPJ = QLineEdit(self)
        self.txtCNPJ.setPlaceholderText("00.000.000/0000-00")
        self.txtCNPJ.setInputMask("00.000.000/0000-00")
        layout.addRow("CNPJ:", self.txtCNPJ)

        # Endereço
        self.txtAddress = QLineEdit(self)
        layout.addRow("Endereço:", self.txtAddress)

        # IE
        self.txtIE = QLineEdit(self)
        self.txtIE.setPlaceholderText("00000000-00")
        self.txtIE.setInputMask("00000000-00")
        layout.addRow("IE:", self.txtIE)

        # Cidade
        self.txtCity = QLineEdit(self)
        layout.addRow("Cidade:", self.txtCity)

        # UF
        self.txtState = QLineEdit(self)
        self.txtState.setInputMask("AA")
        layout.addRow("UF:", self.txtState)

        # CEP
        self.txtCEP = QLineEdit(self)
        self.txtCEP.setPlaceholderText("00.000-000")
        self.txtCEP.setInputMask("00.000-000")
        layout.addRow("CEP:", self.txtCEP)

        # Banco
        self.txtBank = QLineEdit(self)
        layout.addRow("Banco:", self.txtBank)

        # Agência
        self.txtAgency = QLineEdit(self)
        layout.addRow("Agência:", self.txtAgency)

        # Conta
        self.txtAccount = QLineEdit(self)
        layout.addRow("Conta:", self.txtAccount)

        # Botão para salvar cliente
        btnSave = QPushButton("Salvar Cliente", self)
        btnSave.clicked.connect(self.saveClient)
        layout.addRow(btnSave)

        # Definir layout
        self.setLayout(layout)
    
    def saveClient(self):
        # Obter dados do formulário
        client_data = {
            "name": self.txtName.text(),
            "cnpj": self.txtCNPJ.text(),
            "address": self.txtAddress.text(),
            "ie": self.txtIe.text(),
            "city": self.txtCity.text(),
            "state": self.txtState.text(),
            "cep": self.txtCEP.text(),
            "bank": self.txtBank.text(),
            "agency": self.txtAgency.text(),
            "account": self.txtAccount.text()
        }

        # Validar campos obrigatórios
        if not client_data["name"] or not client_data["cnpj"]:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios.")
            return

        # Inserir cliente no banco de dados
        try:
            conn = sqlite3.connect('clients.db')
            cursor = conn.cursor()

            # Verificar se a tabela existe (opcional, já que a criação é garantida no início)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clients'")
            if not cursor.fetchone():
                QMessageBox.critical(self, "Erro", "A tabela 'clients' não existe no banco de dados.")
                return

            # Inserir cliente
            cursor.execute('''
            INSERT INTO clients (name, cnpj, address, ie, city, state, cep, bank, agency, account)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                client_data["name"],
                client_data["cnpj"],
                client_data["address"],
                client_data["ie"],
                client_data["city"],
                client_data["state"],
                client_data["cep"],
                client_data["bank"],
                client_data["agency"],
                client_data["account"]
            ))
            conn.commit()
            conn.close()

            # Mensagem de sucesso
            QMessageBox.information(self, "Sucesso", f"Cliente {client_data['name']} salvo com sucesso.")
            self.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar cliente: {e}")