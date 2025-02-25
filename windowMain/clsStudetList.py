from PyQt5.QtWidgets import  QMainWindow
from windowMain.studetList import Ui_MainWindow
class clsStudetList(QMainWindow):
    def __init__(self):
        super(clsStudetList ,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)