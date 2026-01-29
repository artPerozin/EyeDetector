import cv2
import mediapipe as mp
import numpy as np
import pygame
import time

mp_face_mesh = mp.solutions.face_mesh

# =====================
# Inicializações
# =====================
pygame_initialized = False
music_playing = False

def start_music():
    global pygame_initialized, music_playing
    if not pygame_initialized:
        pygame.mixer.init()
        pygame.mixer.music.load("alert.mp3")
        pygame_initialized = True
    if not music_playing:
        pygame.mixer.music.play(-1)
        music_playing = True

def stop_music():
    global music_playing
    if pygame_initialized and music_playing:
        pygame.mixer.music.stop()
        music_playing = False

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

# =====================
# Câmera
# =====================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Índices da íris no MediaPipe
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

# Limites de centralização
GAZE_THRESHOLD = 0.15

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    looking = False

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        def iris_ratio(iris_ids, eye_left, eye_right):
            iris_x = np.mean([landmarks[i].x for i in iris_ids])
            return (iris_x - eye_left) / (eye_right - eye_left)

        left_ratio = iris_ratio(
            LEFT_IRIS,
            landmarks[33].x,
            landmarks[133].x
        )

        right_ratio = iris_ratio(
            RIGHT_IRIS,
            landmarks[362].x,
            landmarks[263].x
        )

        gaze = (left_ratio + right_ratio) / 2

        if 0.4 < gaze < 0.6:
            looking = True

    # =====================
    # Lógica do alerta
    # =====================
    if looking:
        stop_music()
        status = "OLHANDO"
    else:
        start_music()
        status = "NAO OLHANDO"

    cv2.putText(
        frame,
        status,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0) if looking else (0, 0, 255),
        2
    )

    cv2.imshow("Gaze Detector", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
stop_music()
