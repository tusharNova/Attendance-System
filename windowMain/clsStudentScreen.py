import cv2
import os
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import  QMainWindow ,QMessageBox
from windowMain.StudentScreen import Ui_MainWindow


class clsStudentScreen(QMainWindow):
    def __init__(self):
        super(clsStudentScreen ,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.current_frame = None
        self.start_camera()

        self.ui.btnClikedImg.clicked.connect(self.captureStudentImage)

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
            self.ui.labelVideo.clear()

    def captureStudentImage(self):
        # print("done")
        if self.current_frame is not None and self.ui.txtName.text():
            folder = 'students'
            os.makedirs(folder, exist_ok=True)
            filename = os.path.join(folder, f"{self.ui.txtName.text()}.jpg")
            # cv2.imwrite(filename, cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR))
            cv2.imwrite(filename, self.current_frame)
            QMessageBox.information(self, "Success", f"Image saved as {filename}")
        else:
            QMessageBox.warning(self, "Error", "Please enter student name and capture a valid image!")

    def addStudent(self):
        pass

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()
