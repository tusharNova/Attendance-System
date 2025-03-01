import cv2
import numpy as np
import os


face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


dataset_path = "dataset/"

# Prepare data and labels
labels = []
faces = []
label_dict = {}  # Store name-label mapping

person_id = 0
for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path , person_name)
    if os.path.isdir(person_folder):
        label_dict[person_id] = person_name
        for image_file in os.listdir(person_folder):
            image_path =os.path.join(person_folder , image_file)
            img = cv2.imread(image_path , cv2.IMREAD_GRAYSCALE)
            face =face_cascade.detectMultiScale(img , scaleFactor=1.1 , minNeighbors=5)


            for (x ,y ,w ,h ) in face:
                faces.append(img[y:y+h , x:x+w])
                labels.append(person_id)
    person_id +=1

face_recognizer.train(faces, np.array(labels))

face_recognizer.save("face_trained.yml")
np.save("label_dict.npy", label_dict)

print("Training Complete! Model saved.")