import cv2
import os
from PyQt5.QtCore import QTimer
# from PyQt5.QtCore.QUrl import query
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import  QMainWindow ,QMessageBox
from windowMain.StudentScreen import Ui_MainWindow
from DB.clsDb import clsDb

class clsStudentScreen(QMainWindow):
    def __init__(self):
        super(clsStudentScreen ,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.current_frame = None
        self.gender = None
        self.imgName = ""
        self.start_camera()
        self.db = clsDb()
        self.imgCnt = 0

        self.ui.btnClikedImg.clicked.connect(self.captureStudentImage)
        self.ui.btnAddStd.clicked.connect(self.addStudent)

        self.ui.btnSave.setHidden(1)
        print(self.imgCnt)





    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            self.current_frame = frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.ui.labelVideo.setPixmap(QPixmap.fromImage(image))

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.ui.labelVideo.clear

    def captureStudentImage(self):
        print(self.imgCnt)
        if self.current_frame is not None and self.ui.txtName.text():
            folder = 'dataset/' + self.ui.txtName.text()
            os.makedirs(folder, exist_ok=True)

            if self.imgCnt < 5:
                filename = os.path.join(folder, f"img{self.imgCnt}.jpg")
                cv2.imwrite(filename, self.current_frame)
                QMessageBox.information(self, "Success", f"Image saved and minimum 5 images number of is {self.imgCnt}")
                self.imgCnt += 1
                self.hidebtn()
            else:

                QMessageBox.information(self, "Information", f"No need for more images")
        else:
            QMessageBox.warning(self, "Error", "Please enter student name and capture a valid image!")

    def addStudent(self):

        name = self.ui.txtName.text()
        branch = self.ui.cmbBranch.currentText()
        sem = self.ui.cmbSem.currentText()
        rollNo = self.ui.txtRoll.text()
        email = self.ui.txtEmail.text()
        self.imgName = "txxx"
        if self.ui.radMale.isChecked():
            self.gender = "Male"
        elif self.ui.radFemale.isChecked():
            self.gender = "Female"
        else:
            self.gender = "Other"
        if self.imgCnt == 5:

            query = "insert into StudentTable VALUES(null , '"+name+"', '"+branch+"' , '"+sem+"' , "+rollNo+" ,'"+email+"' ,'"+self.gender+"' ,'"+self.imgName+"' )"
            print(query)
            done = self.db.runSql(query)

            if done:
                QMessageBox.information(self, "Success", f"Student Add Success.")
            else:
                QMessageBox.warning(self, "Error", "Please enter student name!")


        else:
            QMessageBox.warning(self, "Error", "Clicked Minimum 5 images of student!")

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()
