import cv2
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer

# Load the trained face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("face_trained.yml")

# Load label dictionary
label_dict = np.load("label_dict.npy", allow_pickle=True).item()

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Initialize PyQt5 application
app = QApplication(sys.argv)


# Create PyQt5 Window for Messages
class MessageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition")
        self.setGeometry(100, 100, 300, 100)
        self.layout = QVBoxLayout()

        self.label = QLabel("Waiting for face recognition...", self)
        self.label.setStyleSheet("font-size: 16px; color: black;")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
        self.hide()  # Initially hide the window

    def show_message(self, message):
        """Show the message and close it after 2 seconds"""
        self.label.setText(message)
        self.show()

        # Auto-close window after 2 seconds
        QTimer.singleShot(2000, self.hide)


# Create message window instance
message_window = MessageWindow()

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Track last recognized person
last_recognized_name = None

while True:
    ret, frame = video_capture.read()

    # Flip the frame horizontally to correct the mirror effect
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # Detect faces
    faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces_detected:
        face_roi = gray[y:y + h, x:x + w]  # Extract face region

        # Predict using recognizer
        label, confidence = face_recognizer.predict(face_roi)

        if confidence < 50:  # Confidence threshold
            name = label_dict[label]

            # Show message only if the person is newly detected
            if name != last_recognized_name:
                last_recognized_name = name
                message_window.show_message(f"Image Recognized!\nPerson: {name}")

        else:
            name = "Unknown"
            last_recognized_name = None  # Reset tracking for unknown faces

        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display name of the person
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Face Recognition", frame)




    # Process PyQt5 events (for smooth UI updates)
    app.processEvents()

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
