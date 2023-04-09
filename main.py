import gui

import sys

from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

window = gui.MainMenu()
window.show()
app.exec()