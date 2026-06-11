import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time
import threading
from collections import deque

# --- KONFIGURASI CAMERA & LAYAR ---
CAM_W = 1280
CAM_H = 720
FRAME_MARGIN = 50
FPS_BUFFER = 10

# Smoothing faktor untuk pergerakan kursor (semakin kecil semakin mulus, tapi lambat)
EMA_ALPHA = 0.40

# Threshold Jarak & Delay
CLICK_DISTANCE = 30
CLICK_DELAY = 0.4
SCROLL_DELAY = 0.15
SCREENSHOT_DELAY = 2
TOGGLE_HOLD_TIME = 1.0

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

screen_w, screen_h = pyautogui.size()

frame = None
running = True

mouse_enabled = True
resume_tracking = False

last_click = 0
last_scroll = 0
last_screenshot = 0

gesture_start_time = None

ema_x = 0
ema_y = 0

# Variabel tracking titik awal gerakan scroll
prev_scroll_x = None
prev_scroll_y = None

fps_queue = deque(maxlen=FPS_BUFFER)

# --- INISIALISASI KAMERA ---
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)
cap.set(cv2.CAP_PROP_FPS, 60)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
)

def camera_thread():
    global frame, running
    while running:
        ok, img = cap.read()
        if ok:
            frame = cv2.flip(img, 1)

threading.Thread(target=camera_thread, daemon=True).start()

def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

def fingers_up(lm):
    fingers = []
    # Ibu Jari / Thumb
    fingers.append(1 if lm[4][0] > lm[3][0] else 0)
    # Jari Telunjuk / Index
    fingers.append(1 if lm[8][1] < lm[6][1] else 0)
    # Jari Tengah / Middle
    fingers.append(1 if lm[12][1] < lm[10][1] else 0)
    # Jari Manis / Ring
    fingers.append(1 if lm[16][1] < lm[14][1] else 0)
    # Kelingking / Pinky
    fingers.append(1 if lm[20][1] < lm[18][1] else 0)
    return fingers

def ema_move(x, y):
    global ema_x, ema_y, resume_tracking

    # Perbaikan: Mengunci posisi saat pelacakan aktif kembali tanpa lompatan kursor
    if resume_tracking:
        curr_mouse_x, curr_mouse_y = pyautogui.position()
        ema_x = curr_mouse_x
        ema_y = curr_mouse_y
        resume_tracking = False

    if ema_x == 0:
        ema_x = x
        ema_y = y

    ema_x = EMA_ALPHA * x + (1 - EMA_ALPHA) * ema_x
    ema_y = EMA_ALPHA * y + (1 - EMA_ALPHA) * ema_y

    pyautogui.moveTo(int(ema_x), int(ema_y))


# --- MAIN LOOP ---
while True:
    if frame is None:
        continue

    start = time.time()
    img = frame.copy()

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Menggambar batas area pergerakan kursor (Bounding Box)
    cv2.rectangle(
        img,
        (FRAME_MARGIN, FRAME_MARGIN),
        (CAM_W - FRAME_MARGIN, CAM_H - FRAME_MARGIN),
        (255, 0, 255),
        2
    )

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

        lm_list = []
        for lm in hand.landmark:
            x = int(lm.x * CAM_W)
            y = int(lm.y * CAM_H)
            lm_list.append((x, y))

        fingers = fingers_up(lm_list)

        thumb = lm_list[4]
        index = lm_list[8]
        middle = lm_list[12]

        # Mode Kursor: Hanya Jari Telunjuk yang Tegak
        cursor_mode = (
            fingers[1] == 1 and
            fingers[2] == 0 and
            fingers[3] == 0 and
            fingers[4] == 0
        )

        if mouse_enabled and cursor_mode:
            screen_x = np.interp(index[0], (FRAME_MARGIN, CAM_W - FRAME_MARGIN), (0, screen_w))
            screen_y = np.interp(index[1], (FRAME_MARGIN, CAM_H - FRAME_MARGIN), (0, screen_h))
            ema_move(screen_x, screen_y)

        # Klik Kiri: Cubit Jari Jempol dan Jari Telunjuk
        pinch = distance(thumb, index)
        if mouse_enabled and pinch < CLICK_DISTANCE:
            current = time.time()
            if current - last_click > CLICK_DELAY:
                pyautogui.click()
                last_click = current

        # Mode Scroll: Jari Telunjuk dan Jari Tengah Tegak Bersama
        scroll_mode = (
            fingers[1] == 1 and
            fingers[2] == 1 and
            fingers[3] == 0 and
            fingers[4] == 0
        )

        if mouse_enabled and scroll_mode:
            center_x = (index[0] + middle[0]) // 2
            center_y = (index[1] + middle[1]) // 2

            # Inisialisasi awal saat baru masuk mode scroll
            if prev_scroll_x is None:
                prev_scroll_x = center_x
                prev_scroll_y = center_y

            # Akumulasi jarak pergeseran dari titik awal
            dx = center_x - prev_scroll_x
            dy = center_y - prev_scroll_y

            current = time.time()
            move_threshold = 20  # Sensitivitas gerakan scroll

            if current - last_scroll > SCROLL_DELAY:
                # Cek pergerakan dominan (Vertikal vs Horizontal)
                if abs(dy) > abs(dx):
                    # --- SCROLL VERTIKAL (ATAS / BAWAH) ---
                    if abs(dy) > move_threshold:
                        if dy < 0:
                            pyautogui.scroll(150)   # Gerakan jari KE ATAS -> Layar geser KE ATAS
                        else:
                            pyautogui.scroll(-150)  # Gerakan jari KE BAWAH -> Layar geser KE BAWAH
                        
                        last_scroll = current
                        # Update titik acuan hanya setelah berhasil melakukan scroll
                        prev_scroll_x = center_x
                        prev_scroll_y = center_y
                else:
                    # --- SCROLL HORIZONTAL (KIRI / KANAN) ---
                    if abs(dx) > move_threshold:
                        if dx < 0:
                            # Gerakan jari KE KIRI -> Layar geser KE KIRI
                            try:
                                pyautogui.hscroll(-10)
                            except:
                                # Fallback jika OS/Aplikasi tidak mendukung hscroll bawaan
                                with pyautogui.hold('shift'):
                                    pyautogui.scroll(-100)
                        else:
                            # Gerakan jari KE KANAN -> Layar geser KE KANAN
                            try:
                                pyautogui.hscroll(10)
                            except:
                                with pyautogui.hold('shift'):
                                    pyautogui.scroll(100)
                        
                        last_scroll = current
                        prev_scroll_x = center_x
                        prev_scroll_y = center_y
        else:
            # Reset titik acuan jika tangan keluar dari mode scroll
            prev_scroll_x = None
            prev_scroll_y = None

        # Gesture Screenshot: Hanya jari kelingking tegak
        if fingers == [0, 0, 0, 0, 1]:
            current = time.time()
            if current - last_screenshot > SCREENSHOT_DELAY:
                pyautogui.screenshot(f"screenshot_{int(current)}.png")
                last_screenshot = current

        # Gesture Pause: Tangan mengepal penuh
        if fingers == [0, 0, 0, 0, 0]:
            cv2.putText(
                img, "PAUSE", (500, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3
            )
            # Menandai sistem untuk mengambil koordinat mouse fisik saat ini ketika tracking kembali aktif
            resume_tracking = True 

        # Gesture Toggle ON/OFF: Jari manis dan kelingking tegak (Tahan 1 detik)
        if fingers == [0, 0, 0, 1, 1]:
            if gesture_start_time is None:
                gesture_start_time = time.time()

            hold = time.time() - gesture_start_time
            cv2.putText(
                img, f"Toggle {hold:.1f}/1.0", (420, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2
            )

            if hold >= TOGGLE_HOLD_TIME:
                mouse_enabled = not mouse_enabled
                if mouse_enabled:
                    resume_tracking = True
                gesture_start_time = None
        else:
            gesture_start_time = None

    # --- PENGHITUNG FPS & UI DISPLAY ---
    fps = int(1 / max(time.time() - start, 0.001))
    fps_queue.append(fps)
    avg_fps = int(sum(fps_queue) / len(fps_queue))

    status = "ON" if mouse_enabled else "OFF"
    color = (0, 255, 0) if mouse_enabled else (0, 0, 255)

    cv2.putText(img, f"FPS: {avg_fps}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, f"Tracking: {status}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("AI Gesture Mouse PRO V5", img)

    # Tekan 'ESC' untuk keluar dari program
    if cv2.waitKey(1) & 0xFF == 27:
        running = False
        break

cap.release()
cv2.destroyAllWindows()
hands.close()