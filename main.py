import gui

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

app = QApplication(sys.argv)

font = QFont("Calibri", 12)
font.setStyleHint(QFont.Monospace)
app.setFont(font)

window = gui.MainMenu()
window.show()
app.exec()