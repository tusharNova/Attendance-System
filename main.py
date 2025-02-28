from PyQt5.QtWidgets import QApplication
from login.clsScreenMain import clsScreenMain
from windowMain.clsMainWindow import clsMainWindow
from windowMain.clsStudentScreen import clsStudentScreen
from  windowMain.clsTeacherScreen import clsTeacherScreen
import sys

if __name__ == '__main__':
    app = QApplication([])

    # form = clsScreenMain()
    # form = clsMainWindow()
    form = clsStudentScreen()
    # form = clsTeacherScreen()
    form.show()


    sys.exit(app.exec_())