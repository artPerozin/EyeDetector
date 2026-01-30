import cv2
import mediapipe as mp
import numpy as np
import pygame

# ==========================
# MediaPipe Face Mesh
# ==========================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

# ==========================
# ÁUDIO (pygame)
# ==========================
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

# ==========================
# VÍDEO DE ALERTA (PIP)
# ==========================
VIDEO_PATH = "alert.mp4"
VIDEO_WIDTH = 320
VIDEO_HEIGHT = 180
VIDEO_MARGIN = 20

video_cap = None
video_playing = False

def start_video():
    global video_cap, video_playing
    if not video_playing:
        video_cap = cv2.VideoCapture(VIDEO_PATH)
        video_playing = True

def stop_video():
    global video_cap, video_playing
    if video_playing:
        video_cap.release()
        video_playing = False

# ==========================
# CÂMERA
# ==========================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# ==========================
# LANDMARKS IMPORTANTES
# ==========================
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

LEFT_EYE = (33, 133)
RIGHT_EYE = (362, 263)

# ==========================
# FUNÇÃO DE DEBUG VISUAL
# ==========================
def draw_eye_debug(frame, landmarks, iris_ids, eye_left_id, eye_right_id, color):
    h, w, _ = frame.shape

    iris_x = int(np.mean([landmarks[i].x for i in iris_ids]) * w)
    iris_y = int(np.mean([landmarks[i].y for i in iris_ids]) * h)

    eye_left_x = int(landmarks[eye_left_id].x * w)
    eye_right_x = int(landmarks[eye_right_id].x * w)
    eye_y = int(landmarks[eye_left_id].y * h)

    eye_center_x = int((eye_left_x + eye_right_x) / 2)

    cv2.circle(frame, (iris_x, iris_y), 4, color, -1)
    cv2.circle(frame, (eye_center_x, eye_y), 4, (255, 255, 0), -1)

    cv2.line(
        frame,
        (eye_center_x, eye_y),
        (iris_x, iris_y),
        color,
        2
    )

    return (iris_x - eye_center_x) / (eye_right_x - eye_left_x)

# ==========================
# LOOP PRINCIPAL
# ==========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)
    looking = False
    gaze = 0.0

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        left_gaze = draw_eye_debug(
            frame, landmarks, LEFT_IRIS, *LEFT_EYE, (0, 255, 0)
        )

        right_gaze = draw_eye_debug(
            frame, landmarks, RIGHT_IRIS, *RIGHT_EYE, (0, 255, 0)
        )

        gaze = (left_gaze + right_gaze) / 2
        looking = -0.15 < gaze < 0.15

    # ==========================
    # LÓGICA DO ALERTA
    # ==========================
    if looking:
        stop_music()
        stop_video()
        status = "OLHANDO"
    else:
        start_music()
        start_video()
        status = "NAO OLHANDO"

    # ==========================
    # OVERLAY NA CÂMERA
    # ==========================
    cv2.putText(
        frame,
        status,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0) if looking else (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        f"GAZE: {gaze:.2f}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # ==========================
    # VÍDEO PIP NO CANTO
    # ==========================
    if video_playing and video_cap:
        ret_v, video_frame = video_cap.read()

        if not ret_v:
            video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret_v, video_frame = video_cap.read()

        if ret_v:
            video_frame = cv2.resize(video_frame, (VIDEO_WIDTH, VIDEO_HEIGHT))

            h, w, _ = frame.shape
            x1 = w - VIDEO_WIDTH - VIDEO_MARGIN
            y1 = VIDEO_MARGIN
            x2 = w - VIDEO_MARGIN
            y2 = VIDEO_HEIGHT + VIDEO_MARGIN

            frame[y1:y2, x1:x2] = video_frame

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                2
            )

    cv2.imshow("Gaze Detector", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ==========================
# FINALIZAÇÃO
# ==========================
cap.release()
if video_cap:
    video_cap.release()

cv2.destroyAllWindows()
stop_music()