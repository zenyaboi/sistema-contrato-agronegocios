from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from pdf import createPDF

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # setting the window size
        width = 640
        height = 480

        # setting a fixed size for the app (unable to resize)
        self.setFixedSize(width, height)

        # window title
        self.setWindowTitle("Contratos")

        # layout
        layout = QVBoxLayout()
        
        '''
        btnCreate = QPushButton("Criar Contrato", self)
        btnCreate.setGeometry(100, 50, 150, 150)

        btnEdit = QPushButton("Editar Contrato", self)
        btnEdit.setGeometry(400, 50, 150, 150)

        btnExit = QPushButton("Sair da Janela", self)
        btnExit.setGeometry(100, 250, 150, 150)
        btnExit.clicked.connect(self.exitWindow)
        '''
        btnCreate = QPushButton("Criar Contrato")
        btnEdit = QPushButton("Editar Contrato")
        btnExit = QPushButton("Sair da Janela")

        layout.addWidget(btnCreate)
        layout.addWidget(btnEdit)
        layout.addWidget(btnExit)

        btnCreate.clicked.connect(self.createContract)
        btnEdit.clicked.connect(self.editContract)
        btnExit.clicked.connect(self.close)

        self.setLayout(layout)
    
    def createContract(self):
        self.contract_window = ContractWindow()
        self.contract_window.show()

    def editContract(self):
        QMessageBox.information(self, "Editar Contrato", "Funcionalidade em desenvolvimento.")

class ContractWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Criar Contrato")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        self.setLayout(layout)