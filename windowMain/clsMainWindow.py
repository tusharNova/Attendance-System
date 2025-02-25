from PyQt5.QtWidgets import  QMainWindow
from windowMain.MainWindow import Ui_MainWindow
from windowMain.clsStudentScreen import clsStudentScreen
from windowMain.clsStudetList import clsStudetList
from  windowMain.clsTeacherList import clsTeacherList
from windowMain.clsTeacherScreen import  clsTeacherScreen
class clsMainWindow(QMainWindow):
    def __init__(self):
        super(clsMainWindow ,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.loginF = None
        self.form = None

        self.ui.actionCreate_Teacher.triggered.connect(self.TeacherScreen)
        self.ui.actionCreate_Student.triggered.connect(self.StudentScreen)
        self.ui.actionList_of_Teacher.triggered.connect(self.TeacherList)
        self.ui.actionList_of_Student.triggered.connect(self.StudentList)

    def TeacherScreen(self):
        # self.ui.mdiArea.closeActiveSubWindow()
        # self.form = clsTeacherScreen()
        # center = self.ui.mdiArea.viewport().rect().center()
        # f = self.ui.mdiArea.addSubWindow(self.form)
        # f.setVisible(True)
        self.form = None
        self.form = clsTeacherScreen()
        self.form.show()

    def StudentScreen(self):
        self.form = None
        self.form = clsStudentScreen()
        self.form.show()

    def TeacherList(self):
        self.form = None
        self.form = clsTeacherList()
        self.form.show()

    def StudentList(self):
        self.form = None
        self.form = clsStudetList()
        self.form.show()




