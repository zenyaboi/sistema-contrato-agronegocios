import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # setting the window size
        width = 640
        height = 480

        # setting a fixed size for the app (unable to resize)
        self.setFixedSize(width, height)

        # window title
        self.setWindowTitle("Sistema de Contrato")

        # creating main buttons
        btn = QPushButton("Botão 1", self)
        btn2 = QPushButton("Botão 2", self)
        btn3 = QPushButton("Botão 3", self)
        #                x    y    w    h
        btn.setGeometry(100, 50, 150, 150)
        btn2.setGeometry(400, 50, 150, 150)
        btn3.setGeometry(100, 250, 150, 150)

        btn.clicked.connect(self.funcTeste)

    def funcTeste(self):
        print("teste")

if __name__ == "__main__":
    # creating application
    app = QApplication(sys.argv)

    # creating app window
    window = MainWindow()

    # showing all widgets (if any)
    window.show()

    # starting the app
    sys.exit(app.exec())