import os
from datetime import datetime
from PyQt5.QtWidgets import  QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from login.ScreenMain import Ui_MainWindow
from windowMain.clsMainWindow import  clsMainWindow
import cv2 ,sys


class clsScreenMain(QMainWindow):
    def __init__(self):
        super(clsScreenMain ,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.mainf = None
        self.ui.btnClicked.clicked.connect(self.capture_image)
        self.ui.btnLogin.clicked.connect(self.stop_camera)
        self.ui.btnAdminControl.clicked.connect(self.showAdminControl)
        self.start_camera()
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
            self.current_frame = frame

    def capture_image(self):
        try:
            if hasattr(self, 'current_frame'):
                folder = 'captured_images'
                os.makedirs(folder, exist_ok=True)
                filename = os.path.join(folder, f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                cv2.imwrite(filename, cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR))
                print(f"Image saved to {filename}")
        except Exception as e:
            print(e)

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.ui.labelVideo.clear()

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()

    def showAdminControl(self):
        self.mainf = clsMainWindow()
        self.mainf.show()
        self.close()
