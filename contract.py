from PyQt6.QtWidgets import QWidget, QLabel, QPushButton
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

        btn = QPushButton("Butao", self)
        btn.setGeometry(100, 100, 100, 100)
        btn.clicked.connect(self.teste)
    
    def teste(self):
        print("teste")
        createPDF("output.pdf")