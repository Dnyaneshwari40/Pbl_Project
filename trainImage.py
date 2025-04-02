import cv2
import os
import numpy as np

def TrainImage(haarcascade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier(haarcascade_path)

    faces = []
    ids = []

    student_folders = os.listdir(trainimage_path)

    for student in student_folders:
        student_path = os.path.join(trainimage_path, student)

        if os.path.isdir(student_path):
            image_files = [os.path.join(student_path, f) for f in os.listdir(student_path) if f.endswith(".jpg")]

            for img_path in image_files:
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                id_ = int(student)
                faces.append(img)
                ids.append(id_)

    recognizer.train(faces, np.array(ids))
    recognizer.save(trainimagelabel_path)

    message.configure(text="Training Completed!")
    text_to_speech("Training Completed!")
