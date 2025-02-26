import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

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

# showing all widgets (if any)
window.show()

# starting the app
sys.exit(app.exec())