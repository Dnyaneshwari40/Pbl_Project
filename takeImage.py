import cv2
import os
import csv

def TakeImage(enrollment, name, haarcascade_path, trainimage_path, message, err_screen, text_to_speech):
    if enrollment == "" or name == "":
        err_screen()
        text_to_speech("Enrollment and Name required!")
        return

    # Create student folder if not exists
    student_folder = os.path.join(trainimage_path, enrollment)
    if not os.path.exists(student_folder):
        os.makedirs(student_folder)

    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(haarcascade_path)
    count = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = frame[y:y + h, x:x + w]
            img_path = os.path.join(student_folder, f"{name}_{count}.jpg")
            cv2.imwrite(img_path, face_img)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Capturing Face", frame)

        if cv2.waitKey(100) & 0xFF == ord("q") or count >= 10:
            break

    cam.release()
    cv2.destroyAllWindows()

    # Save details in CSV
    csv_path = "StudentDetails/studentdetails.csv"
    with open(csv_path, "a") as f:
        writer = csv.writer(f)
        writer.writerow([enrollment, name])

    message.configure(text=f"Images Saved for {name}")
    text_to_speech(f"Images saved for {name}")
