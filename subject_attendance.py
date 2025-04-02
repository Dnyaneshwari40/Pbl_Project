import cv2
import os
import numpy as np
import pandas as pd
import datetime
import csv

def subjectChoose(text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    if not os.path.exists("TrainingImageLabel/Trainner.yml"):
        text_to_speech("Training model not found! Please train the model first.")
        return

    recognizer.read("TrainingImageLabel/Trainner.yml")
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        text_to_speech("Error: Could not access webcam!")
        return

    font = cv2.FONT_HERSHEY_SIMPLEX
    attendance_set = set()

    # Load student details
    student_details_path = "StudentDetails/studentdetails.csv"
    if not os.path.exists(student_details_path):
        text_to_speech("Student details file missing!")
        return
    
    student_details = pd.read_csv(student_details_path, header=None)
    student_dict = {str(row[0]): row[1] for _, row in student_details.iterrows()}

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            id_, conf = recognizer.predict(gray[y:y + h, x:x + w])

            if conf < 60:  # Adjust confidence threshold
                name = student_dict.get(str(id_), "Unknown")
                attendance_set.add((id_, name, str(datetime.datetime.now())))

                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y - 10), font, 0.8, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (x, y - 10), font, 0.8, (0, 0, 255), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

    # Save attendance
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    attendance_file = f"Attendance/Attendance_{today_date}.csv"

    with open(attendance_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Enrollment", "Name", "Time"])
        writer.writerows(attendance_set)

    text_to_speech("Attendance marked successfully!")
