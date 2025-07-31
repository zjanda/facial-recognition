import socket
import threading
import cv2
import numpy as np
import os
from face_recognition_helpers import detect_faces, encode_faces, compare_faces, load_known_faces, DEBUG

PORT = 8485
HOST = "0.0.0.0"
WIRED = os.system("ip link show eth0 | grep 'state UP'") == 0
CONNECTION_TYPE = "ethernet" if WIRED else "wifi"
CAPTURED_FRAME_NAME = "zack"
CAPTURE_FRAME_PATH = f"known_faces/{CAPTURED_FRAME_NAME}.jpg"
known_faces = load_known_faces()
# print(f"Known faces: {known_faces}")
facial_recognition = True

def receive_video(conn):
    buffer = b""
    frame_count = 0
    frame_delay = 2
    facial_recognition_delay = 10
    face_locations = None

    while True:
        data = conn.recv(4096)
        if not data:
            break

        buffer += data

        while True:
            start = buffer.find(b'\xff\xd8')
            end = buffer.find(b'\xff\xd9')

            if start != -1 and end != -1 and end > start:
                jpg = buffer[start:end+2]
                buffer = buffer[end+2:]

                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if frame is not None and frame_count % frame_delay == 0:
                    if facial_recognition and frame_count % facial_recognition_delay == 0:
                        face_locations = detect_faces(frame)
                        if face_locations:
                            if DEBUG: print(f"Faces detected: {len(face_locations)}")
                            face_encodings = encode_faces(frame, face_locations)
                            # if DEBUG: print(f"Face encodings: {face_encodings}")
                            matches_found = compare_faces(face_encodings, known_faces)
                            print(f"len matches_found: {len(matches_found)}")
                            if matches_found:
                                
                                if DEBUG: print(f"Known face found: {matches_found}")
                
                frame_count += 1
                if face_locations:
                    for (top, right, bottom, left) in face_locations:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.imshow("Pi Stream", frame)
                if cv2.waitKey(1) == ord("q"):
                    return
                elif cv2.waitKey(1) == ord("c"):
                    
                    cv2.imwrite(CAPTURE_FRAME_PATH, frame)
                    if DEBUG: print("Frame captured")
            else:
                # Discard junk data to avoid buffer bloat
                if len(buffer) > 1_000_000:
                    buffer = b""
                break


    conn.close()
    cv2.destroyAllWindows()


def send_commands(conn):
    try:
        while True:
            msg = input("Send command to Pi: ")
            if msg.lower() in ["exit", "quit"]:
                break
            conn.sendall(msg.encode("utf-8"))
    except:
        pass
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for Pi connection...")
conn, _ = server.accept()
print(f"Connected via {CONNECTION_TYPE} at port {PORT}")

t1 = threading.Thread(target=receive_video, args=(conn,))
t2 = threading.Thread(target=send_commands, args=(conn,))
t1.start()
t2.start()
t1.join()
t2.join()
