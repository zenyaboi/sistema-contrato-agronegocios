from PyQt6.QtWidgets import QWidget, QLabel, QPushButton

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

        btnAdd = QPushButton("Adicionar Cliente", self)
        btnAdd.setGeometry(100, 50, 150, 150)

        btnEdit = QPushButton("Editar Cliente", self)
        btnEdit.setGeometry(400, 50, 150, 150)

        btnExit = QPushButton("Sair da Janela", self)
        btnExit.setGeometry(100, 250, 150, 150)
        btnExit.clicked.connect(self.exitWindow)
    
    def exitWindow(self):
        self.close()