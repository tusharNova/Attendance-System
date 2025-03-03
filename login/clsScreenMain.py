# import os
# from datetime import datetime
# from PyQt5.QtWidgets import  QMainWindow
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtCore import QTimer
# from login.ScreenMain import Ui_MainWindow
# from windowMain.clsMainWindow import  clsMainWindow
# import cv2 ,sys
#
#
# class clsScreenMain(QMainWindow):
#     def __init__(self):
#         super(clsScreenMain ,self).__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#

import cv2
import numpy as np
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from pyexpat import ExpatError

from login.ScreenMain import Ui_MainWindow

# Load the trained face recognizer
try:
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read("face_trained.yml")
except Exception as e:
    print(f"Error loading face recognizer: {e}")
    sys.exit(1)

# Load label dictionary
try:
    label_dict = np.load("label_dict.npy", allow_pickle=True).item()
except Exception as e:
    print(f"Error loading label dictionary: {e}")
    sys.exit(1)

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


class VideoThread(QThread):
    """Thread to handle video capture and face recognition."""
    update_frame_signal = pyqtSignal(QImage)  # Signal to send frames to UI
    show_message_signal = pyqtSignal(str)  # Signal to show recognition messages

    def run(self):
        cap = cv2.VideoCapture(0)  # Open webcam
        last_recognized_name = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Face detection
            faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            for (x, y, w, h) in faces_detected:
                face_roi = gray[y:y + h, x:x + w]

                # Face recognition
                label, confidence = face_recognizer.predict(face_roi)

                if confidence < 50:
                    name = label_dict[label]
                    if name != last_recognized_name:
                        last_recognized_name = name
                        self.show_message_signal.emit(f"Image Recognized!\nPerson: {name}")
                else:
                    name = "Unknown"
                    last_recognized_name = None

                # Draw a rectangle and put a name label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Convert OpenCV frame to QImage
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Emit the signal with the new frame
            self.update_frame_signal.emit(qt_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


class clsScreenMain(QMainWindow):
    def __init__(self):
        super(clsScreenMain, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnClicked.setHidden(True)
        # Start the video thread

        self.ui.btnLogin.clicked.connect(self.showCam)


    def showCam(self):
        self.video_thread = VideoThread()
        self.video_thread.update_frame_signal.connect(self.update_video_label)
        self.video_thread.show_message_signal.connect(self.show_message)
        self.video_thread.start()


    def update_video_label(self, qt_image):
        """Update the QLabel with the video feed."""
        pixmap = QPixmap.fromImage(qt_image)
        self.ui.labelVideo.setPixmap(pixmap)  # Assuming labelVideo is the QLabel in your UI
        self.ui.labelVideo.setScaledContents(True)  # Ensure it fits properly

    def show_message(self, message):
        """Show recognition message (e.g., in a status bar or another QLabel)."""
        try:
            self.ui.statusbar.showMessage(message, 2000)  # Display for 2 seconds
        except Exception as e:
            print(e)


