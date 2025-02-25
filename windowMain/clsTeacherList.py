from PyQt5.QtWidgets import  QMainWindow
from windowMain.TeacherList import Ui_MainWindow

class clsTeacherList(QMainWindow):
    def __init__(self):
        super(clsTeacherList ,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)