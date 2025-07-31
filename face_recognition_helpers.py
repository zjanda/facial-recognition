import time
import cv2
import face_recognition
import os
import pickle
import numpy as np

ENCODINGS_DIR = "face_encodings"
KNOWN_FACES_DIR = "known_faces"
DEBUG = True

def detect_faces(frame):
    return face_recognition.face_locations(frame)

def encode_faces(frame, face_locations):
    return face_recognition.face_encodings(frame, face_locations)

def compare_faces(face_encodings, known_faces, tolerance=0.6):
    known_encodings, known_names = known_faces
    matches = []
    for encoding in face_encodings:
        results = face_recognition.compare_faces(known_encodings, encoding, tolerance)
        for match, name in zip(results, known_names):
            if match:
                matches.append(name)
    return matches

def load_known_faces():
    known_encodings = []
    known_names = []
    for person_name in os.listdir(KNOWN_FACES_DIR):
        person_dir = os.path.join(KNOWN_FACES_DIR, person_name)
        if os.path.isdir(person_dir):
            for filename in os.listdir(person_dir):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    image_path = os.path.join(person_dir, filename)
                    image = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        known_encodings.append(encodings[0])
                        known_names.append(person_name)
    return known_encodings, known_names

def save_encodings(known_face_encodings, known_face_names):
    os.makedirs(ENCODINGS_DIR, exist_ok=True)
    
    name_counts = {}
    for name, encoding in zip(known_face_names, known_face_encodings):
        if name not in name_counts:
            name_counts[name] = 1
        else:
            name_counts[name] += 1
        person_dir = os.path.join(ENCODINGS_DIR, name)
        os.makedirs(person_dir, exist_ok=True)
        encoding_file_path = os.path.join(person_dir, f"{name}_encoding_{name_counts[name]}.pkl")
        with open(encoding_file_path, "wb") as f:
            pickle.dump(encoding, f)