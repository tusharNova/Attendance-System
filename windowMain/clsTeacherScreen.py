from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import  QMainWindow
from windowMain.TeacherScreen import Ui_MainWindow
import cv2
class clsTeacherScreen(QMainWindow):
    def __init__(self):
        super(clsTeacherScreen ,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.ui.btnClikedImg.clicked.connect(self.start_camera)
        self.ui.btnSave.clicked.connect(self.stop_camera)

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.ui.labelVideo.setPixmap(QPixmap.fromImage(image))

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.ui.labelVideo.clear()

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()
