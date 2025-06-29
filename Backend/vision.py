import cv2
import threading
from Backend.TextToSpeech import TextToSpeech

def start_vision():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    greeted = False

    if not cap.isOpened():
        print("❌ Could not open webcam.")
        TextToSpeech("Sorry, I could not access the webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if not greeted:
                threading.Thread(target=TextToSpeech, args=("Hello! Welcome back.",), daemon=True).start()
                greeted = True

        cv2.imshow("JARVIS Vision", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()