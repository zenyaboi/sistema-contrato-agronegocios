from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QFormLayout, QLineEdit)

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
        layout.addRow("CNPJ:", self.txtCNPJ)

        # Endereço
        self.txtAddress = QLineEdit(self)
        layout.addRow("Endereço:", self.txtAddress)

        # Cidade
        self.txtCity = QLineEdit(self)
        layout.addRow("Cidade:", self.txtCity)

        # UF
        self.txtState = QLineEdit(self)
        layout.addRow("UF:", self.txtState)

        # CEP
        self.txtCEP = QLineEdit(self)
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
        #btnSave.clicked.connect(self.saveClient)
        layout.addRow(btnSave)

        # Definir layout
        self.setLayout(layout)