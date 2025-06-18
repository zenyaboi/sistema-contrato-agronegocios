from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QLineEdit, 
                             QComboBox, QTableWidget, QHBoxLayout, QFormLayout, QTextEdit, QStackedWidget,
                             QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt
import sqlite3
from database import create_clients_db
import os

if not os.path.exists('clients.db'):
    print("Banco de dados 'clients.db' não encontrado. Criando...")
    create_clients_db()
else:
    print("Banco de dados 'clients.db' já existe. Verificando tabelas...")

class FocusAwareLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursorPosition(0)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.setCursorPosition(0)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.hasSelectedText():
            self.setCursorPosition(0)

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
        self.client_window = AddClientWindow()
        self.client_window.show()

    def editClient(self):
        self.edit_window = EditClientSelectWindow()
        self.edit_window.show()

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
        self.txtCNPJ = FocusAwareLineEdit(self)
        self.txtCNPJ.setPlaceholderText("00.000.000/0000-00")
        self.txtCNPJ.setInputMask("00.000.000/0000-00")
        layout.addRow("CNPJ:", self.txtCNPJ)

        # Endereço
        self.txtAddress = QLineEdit(self)
        layout.addRow("Endereço:", self.txtAddress)

        # IE
        self.txtIE = FocusAwareLineEdit(self)
        self.txtIE.setPlaceholderText("00000000-00")
        self.txtIE.setInputMask("00000000-00")
        layout.addRow("IE:", self.txtIE)

        # Cidade
        self.txtCity = QLineEdit(self)
        layout.addRow("Cidade:", self.txtCity)

        # UF
        self.txtState = FocusAwareLineEdit(self)
        self.txtState.setInputMask("AA")
        layout.addRow("UF:", self.txtState)

        # CEP
        self.txtCEP = FocusAwareLineEdit(self)
        self.txtCEP.setPlaceholderText("00.000-000")
        self.txtCEP.setInputMask("00.000-000")
        layout.addRow("CEP:", self.txtCEP)

        # Banco
        self.txtBank = QLineEdit(self)
        layout.addRow("Banco:", self.txtBank)

        # Nome no Banco
        self.txtBankName = QLineEdit(self)
        layout.addRow("Nome no Banco:", self.txtBankName)

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
            "ie": self.txtIE.text(),
            "city": self.txtCity.text(),
            "state": self.txtState.text(),
            "cep": self.txtCEP.text(),
            "bank": self.txtBank.text(),
            "bank_name": self.txtBankName.text(),
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
            INSERT INTO clients (name, cnpj, address, ie, city, state, cep, bank, bankName, agency, account)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                client_data["name"],
                client_data["cnpj"],
                client_data["address"],
                client_data["ie"],
                client_data["city"],
                client_data["state"],
                client_data["cep"],
                client_data["bank"],
                client_data["bank_name"],
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

class EditClientSelectWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selecionar Cliente para Editar")
        self.setFixedSize(800, 600)
        
        layout = QVBoxLayout()
        
        # Label de instruções
        label = QLabel("Selecione o cliente que deseja editar:")
        layout.addWidget(label)
        
        # Tabela para mostrar clientes
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nome", "CNPJ", "Cidade/UF"
        ])
        
        # Ajustar largura das colunas
        self.table.setColumnWidth(0, 50)   # ID
        self.table.setColumnWidth(1, 200)  # Nome
        self.table.setColumnWidth(2, 150)  # CNPJ
        self.table.setColumnWidth(3, 150)  # Cidade/UF
        
        # Permitir seleção de apenas uma linha por vez
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.table)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        btnEdit = QPushButton("Editar Selecionado")
        btnDelete = QPushButton("Excluir Selecionado")
        btnRefresh = QPushButton("Atualizar Lista")
        btnClose = QPushButton("Fechar")
        
        btnEdit.clicked.connect(self.editSelectedClient)
        btnDelete.clicked.connect(self.deleteSelectedClient)
        btnRefresh.clicked.connect(self.loadClients)
        btnClose.clicked.connect(self.close)
        
        btn_layout.addWidget(btnEdit)
        btn_layout.addWidget(btnDelete)
        btn_layout.addWidget(btnRefresh)
        btn_layout.addWidget(btnClose)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        # Carregar clientes ao abrir
        self.loadClients()
    
    def loadClients(self):
        try:
            conn = sqlite3.connect('clients.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, cnpj, city, state
                FROM clients 
                ORDER BY id
            ''')
            
            clients = cursor.fetchall()
            conn.close()
            
            # Limpar tabela
            self.table.setRowCount(0)
            
            # Adicionar clientes à tabela
            for row, client in enumerate(clients):
                self.table.insertRow(row)
                
                # ID
                self.table.setItem(row, 0, QTableWidgetItem(str(client[0])))
                
                # Nome
                self.table.setItem(row, 1, QTableWidgetItem(client[1] or ""))
                
                # CNPJ
                cnpj_item = QTableWidgetItem(client[2] or "")
                cnpj_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 2, cnpj_item)
                
                # Cidade/UF
                cidade_uf = f"{client[3] or ''}/{client[4] or ''}"
                self.table.setItem(row, 3, QTableWidgetItem(cidade_uf))
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar clientes: {e}")
    
    def editSelectedClient(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para editar.")
            return
        
        try:
            client_id = int(self.table.item(current_row, 0).text())
            self.edit_window = EditClientFormWindow(client_id)
            self.edit_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir editor: {str(e)}")
    
    def deleteSelectedClient(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um cliente para excluir.")
            return
        
        try:
            client_id = int(self.table.item(current_row, 0).text())
            client_name = self.table.item(current_row, 1).text()
            
            # Verificar se o cliente está em algum contrato
            conn = sqlite3.connect('contracts.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM contracts WHERE seller_id = ? OR buyer_id = ?', (client_id, client_id))
            contract_count = cursor.fetchone()[0]
            conn.close()
            
            if contract_count > 0:
                QMessageBox.warning(
                    self,
                    "Não é possível excluir",
                    f"Este cliente está vinculado a {contract_count} contrato(s).\nRemova os contratos primeiro."
                )
                return
            
            # Confirmar com o usuário
            reply = QMessageBox.question(
                self, 
                "Confirmar Exclusão",
                f"Tem certeza que deseja excluir o cliente {client_name}?\nEsta ação não pode ser desfeita.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                conn = sqlite3.connect('clients.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM clients WHERE id = ?', (client_id,))
                conn.commit()
                conn.close()
                
                QMessageBox.information(self, "Sucesso", "Cliente excluído com sucesso.")
                self.loadClients()  # Atualizar a lista
        
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao excluir cliente: {str(e)}")

class EditClientFormWindow(QWidget):
    def __init__(self, client_id):
        super().__init__()
        self.client_id = client_id
        
        self.setWindowTitle("Editar Cliente")
        self.setFixedSize(400, 500)
        
        layout = QFormLayout()
        
        # Criar campos
        self.txtName = QLineEdit()
        self.txtCNPJ = FocusAwareLineEdit()
        self.txtCNPJ.setInputMask("00.000.000/0000-00")
        self.txtAddress = QLineEdit()
        self.txtIE = FocusAwareLineEdit()
        self.txtIE.setInputMask("00000000-00")
        self.txtCity = QLineEdit()
        self.txtState = FocusAwareLineEdit()
        self.txtState.setInputMask("AA")
        self.txtCEP = FocusAwareLineEdit()
        self.txtCEP.setInputMask("00.000-000")
        self.txtBank = QLineEdit()
        self.txtBankName = QLineEdit()
        self.txtAgency = QLineEdit()
        self.txtAccount = QLineEdit()
        
        # Adicionar ao layout
        layout.addRow("Nome:", self.txtName)
        layout.addRow("CNPJ:", self.txtCNPJ)
        layout.addRow("Endereço:", self.txtAddress)
        layout.addRow("IE:", self.txtIE)
        layout.addRow("Cidade:", self.txtCity)
        layout.addRow("UF:", self.txtState)
        layout.addRow("CEP:", self.txtCEP)
        layout.addRow("Banco:", self.txtBank)
        layout.addRow("Nome no Banco:", self.txtBankName)
        layout.addRow("Agência:", self.txtAgency)
        layout.addRow("Conta:", self.txtAccount)
        
        # Botões
        btnSave = QPushButton("Salvar")
        btnCancel = QPushButton("Cancelar")
        
        btnSave.clicked.connect(self.saveClient)
        btnCancel.clicked.connect(self.close)
        
        layout.addRow(btnSave)
        layout.addRow(btnCancel)
        
        self.setLayout(layout)
        self.loadClientData()
    
    def loadClientData(self):
        try:
            conn = sqlite3.connect('clients.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clients WHERE id = ?', (self.client_id,))
            client = cursor.fetchone()
            conn.close()
            
            if client:
                self.txtName.setText(client[1] or "")
                self.txtCNPJ.setText(client[2] or "")
                self.txtAddress.setText(client[3] or "")
                self.txtIE.setText(client[4] or "")
                self.txtCity.setText(client[5] or "")
                self.txtState.setText(client[6] or "")
                self.txtCEP.setText(client[7] or "")
                self.txtBank.setText(client[8] or "")
                self.txtBankName.setText(client[9] or "")
                self.txtAgency.setText(client[10] or "")
                self.txtAccount.setText(client[11] or "")
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar cliente: {e}")
    
    def saveClient(self):
        if not self.txtName.text() or not self.txtCNPJ.text():
            QMessageBox.warning(self, "Erro", "Nome e CNPJ são obrigatórios.")
            return
        
        try:
            conn = sqlite3.connect('clients.db')
            cursor = conn.cursor()
            
            cursor.execute('''
            UPDATE clients SET name=?, cnpj=?, address=?, ie=?, city=?, 
                             state=?, cep=?, bank=?, bankName=?, agency=?, account=?
            WHERE id=?
            ''', (
                self.txtName.text(),
                self.txtCNPJ.text(),
                self.txtAddress.text(),
                self.txtIE.text(),
                self.txtCity.text(),
                self.txtState.text(),
                self.txtCEP.text(),
                self.txtBank.text(),
                self.txtBankName.text(),
                self.txtAgency.text(),
                self.txtAccount.text(),
                self.client_id
            ))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Sucesso", "Cliente atualizado com sucesso!")
            self.close()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar: {e}")