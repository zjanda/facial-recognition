import time
import face_recognition
import cv2
import os
import pickle
from face_recognition_helpers import load_known_faces, save_encodings, ENCODINGS_DIR


known_face_encodings, known_face_names = load_known_faces()
save_encodings(known_face_encodings, known_face_names)


