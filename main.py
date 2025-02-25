from PyQt5.QtWidgets import QApplication
from login.clsScreenMain import clsScreenMain
from windowMain.clsMainWindow import clsMainWindow
import sys

if __name__ == '__main__':
    app = QApplication([])

    form = clsScreenMain()
    # form = clsMainWindow()
    form.show()

    sys.exit(app.exec_())