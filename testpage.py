import sys
import cv2
import os
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer


class StudentRegistration(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration")
        self.setGeometry(100, 100, 640, 520)

        # Widgets
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.id_label = QLabel("Student ID:")
        self.id_input = QLineEdit()
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(640, 480)

        self.start_button = QPushButton("Start Camera")
        self.capture_button = QPushButton("Capture Image")
        self.stop_button = QPushButton("Stop Camera")
        self.register_button = QPushButton("Register Student")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.video_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.capture_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

        # Connections
        self.start_button.clicked.connect(self.start_camera)
        self.capture_button.clicked.connect(self.capture_image)
        self.stop_button.clicked.connect(self.stop_camera)
        self.register_button.clicked.connect(self.register_student)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.current_frame = None

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
            self.video_label.setPixmap(QPixmap.fromImage(image))

    def capture_image(self):
        if self.current_frame is not None and self.id_input.text():
            folder = 'students'
            os.makedirs(folder, exist_ok=True)
            filename = os.path.join(folder, f"{self.id_input.text()}.jpg")
            cv2.imwrite(filename, cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR))
            QMessageBox.information(self, "Success", f"Image saved as {filename}")
        else:
            QMessageBox.warning(self, "Error", "Please enter Student ID and capture a valid image!")

    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.video_label.clear()

    def register_student(self):
        name = self.name_input.text()
        student_id = self.id_input.text()
        if name and student_id:
            QMessageBox.information(self, "Success", f"Student {name} with ID {student_id} registered successfully!")
        else:
            QMessageBox.warning(self, "Error", "Please fill in all details!")

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentRegistration()
    window.show()
    sys.exit(app.exec_())
