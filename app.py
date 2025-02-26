import sys
from contract import *
from client import *
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
        btnContract = QPushButton("Botão 1", self)
        btnClient = QPushButton("Botão 2", self)
        btnExit = QPushButton("Botão 3", self)
        #                x    y    w    h
        btnContract.setGeometry(100, 50, 150, 150)
        btnClient.setGeometry(400, 50, 150, 150)
        btnExit.setGeometry(100, 250, 150, 150)

        btnContract.clicked.connect(self.openSecondWindow)
        btnClient.clicked.connect(self.openThirdWindow)

    def openSecondWindow(self):
        self.second_window = SecondWindow()

        main_window_position = self.pos()

        self.second_window.move(main_window_position.x() + self.width(), main_window_position.y() + self.height() - 500)

        self.second_window.show()
    
    def openThirdWindow(self):
        self.third_window = ThirdWindow()

        main_window_position = self.pos()

        self.third_window.move(main_window_position.x() + self.width(), main_window_position.y() + self.height() - 300)

        self.third_window.show()

if __name__ == "__main__":
    # creating application
    app = QApplication(sys.argv)

    # creating app window
    window = MainWindow()

    # showing all widgets (if any)
    window.show()

    # starting the app
    sys.exit(app.exec())