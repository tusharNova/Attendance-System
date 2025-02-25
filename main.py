from PyQt5.QtWidgets import QApplication
from login.clsScreenMain import clsScreenMain
from windowMain.clsMainWindow import clsMainWindow
from windowMain.clsStudentScreen import clsStudentScreen
import sys

if __name__ == '__main__':
    app = QApplication([])

    # form = clsScreenMain()
    # form = clsMainWindow()
    form = clsStudentScreen()
    form.show()

    sys.exit(app.exec_())