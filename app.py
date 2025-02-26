import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

def funcTeste():
    print("teste")

# creating application
app = QApplication(sys.argv)

# creating app window
window = QWidget()

# setting the window size
width = 640
height = 480

# setting a fixed size for the app (unable to resize)
window.setFixedSize(width, height)

# window title
window.setWindowTitle("Sistema de Contrato")

# creating main buttons
btn = QPushButton("Botão 1", window)
btn2 = QPushButton("Botão 2", window)
btn3 = QPushButton("Botão 3", window)
#                x    y    w    h
btn.setGeometry(100, 50, 150, 150)
btn2.setGeometry(400, 50, 150, 150)
btn3.setGeometry(100, 250, 150, 150)

btn.clicked.connect(funcTeste)

# showing all widgets (if any)
window.show()

# starting the app
sys.exit(app.exec())