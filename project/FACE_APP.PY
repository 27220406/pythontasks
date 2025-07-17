import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# LBPH recognizer with tuned parameters
recognizer = cv2.face.LBPHFaceRecognizer_create(
    radius=1,
    neighbors=8,
    grid_x=8,
    grid_y=8,
    threshold=100.0
)

# Paths
dataset_path = "dataset"
trainer_path = "trainer.yml"
labels_file = "labels.txt"

os.makedirs(dataset_path, exist_ok=True)

# ------------ Collect Face Data ------------
def collect_faces():
    name = name_var.get().strip()
    if not name:
        messagebox.showerror("Error", "Please enter a name!")
        return

    person_folder = os.path.join(dataset_path, name)
    os.makedirs(person_folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open webcam")
        return

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))
            face_img = cv2.equalizeHist(face_img)

            count += 1
            cv2.imwrite(os.path.join(person_folder, f"{count}.jpg"), face_img)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.putText(frame, f"Capturing {count}/30", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Collecting Faces", frame)

        if cv2.waitKey(1) & 0xFF == 27 or count >= 30:
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Done", f"Collected face data for '{name}'!")

    train_model()

# ------------ Train Model ------------
def train_model():
    faces = []
    labels = []
    label_map = {}
    current_id = 0

    for person_name in os.listdir(dataset_path):
        person_folder = os.path.join(dataset_path, person_name)
        if not os.path.isdir(person_folder):
            continue

        label_map[current_id] = person_name
        for img_name in os.listdir(person_folder):
            img_path = os.path.join(person_folder, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                img = cv2.resize(img, (200, 200))
                img = cv2.equalizeHist(img)
                faces.append(img)
                labels.append(current_id)
        current_id += 1

    if not faces:
        messagebox.showerror("Error", "No face data found to train!")
        return

    recognizer.train(faces, np.array(labels))
    recognizer.save(trainer_path)

    with open(labels_file, "w") as f:
        for label, name in label_map.items():
            f.write(f"{label}:{name}\n")

# ------------ Recognize Faces ------------
def recognize_faces():
    if not os.path.exists(trainer_path) or not os.path.exists(labels_file):
        messagebox.showerror("Error", "No trained data found! Please collect face first.")
        return

    recognizer.read(trainer_path)

    label_map = {}
    with open(labels_file, "r") as f:
        for line in f:
            label, name = line.strip().split(":")
            label_map[int(label)] = name

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open webcam")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200, 200))
            roi = cv2.equalizeHist(roi)

            label, confidence = recognizer.predict(roi)
            if confidence < 70:
                name = label_map.get(label, "Unknown").upper()
            else:
                name = "UNKNOWN"

            text = f"{name} ({int(confidence)})"
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, text, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ------------ GUI Setup ------------
root = tk.Tk()
root.title("Face Recognition App")
root.geometry("400x300")
root.configure(bg="#f4f4f4")

tk.Label(root, text="Enter Name for Face Data:", font=("Arial", 12), bg="#f4f4f4").pack(pady=10)
name_var = tk.StringVar()
tk.Entry(root, textvariable=name_var, font=("Arial", 12), width=30).pack()

tk.Button(root, text="📷 Collect Face", command=collect_faces,
          font=("Arial", 12), bg="#4CAF50", fg="white", width=20).pack(pady=15)

tk.Button(root, text="🔍 Recognize Face", command=recognize_faces,
          font=("Arial", 12), bg="#2196F3", fg="white", width=20).pack(pady=5)

tk.Label(root, text="Press ESC to exit webcam view", font=("Arial", 10), fg="gray", bg="#f4f4f4").pack(pady=20)

root.mainloop()