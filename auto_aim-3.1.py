from ultralytics import YOLO
import pyautogui
import cv2
import numpy as np
import subprocess
import win32gui
import time
from threading import Thread

# Configurações
CAPTURE_SIZE_X = 320
CAPTURE_SIZE_Y = 240
X_ORIGIN = 702
Y_ORIGIN = 200
pyautogui.MINIMUM_DURATION = 0
pyautogui.PAUSE = 0

def localizar_bluestacks():
    janela = win32gui.FindWindow(None, "BlueStacks")
    if janela:
        rect = win32gui.GetWindowRect(janela)
        return rect
    return None

def load_model():
    try:
        model = YOLO("yolov8s.pt")  # Usa YOLOv8s
        return model
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        return None

def capture_center_screen():
    try:
        screenshot = pyautogui.screenshot(region=(X_ORIGIN, Y_ORIGIN, CAPTURE_SIZE_X, CAPTURE_SIZE_Y))
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return frame, (X_ORIGIN, Y_ORIGIN)
    except Exception as e:
        print(f"Erro na captura: {e}")
        return None, (X_ORIGIN, Y_ORIGIN)

def detect_person(model, frame):
    if frame is None:
        return None, None

    results = model.predict(frame, imgsz=320)[0]
    boxes = results.boxes.xyxy.cpu().numpy()
    classes = results.boxes.cls.cpu().numpy()
    confidences = results.boxes.conf.cpu().numpy()

    if boxes is not None and len(boxes) > 0:
        best_box = None
        closest_dist = float("inf")
        center_x = frame.shape[1] / 2
        center_y = frame.shape[0] / 2

        for box, cls, conf in zip(boxes, classes, confidences):
            if int(cls) == 0 and conf > 0.5:  # 'person' = class 0
                x_center = (box[0] + box[2]) / 2
                y_center = (box[1] + box[3]) / 2
                dist = abs(x_center - center_x) + abs(y_center - center_y)
                if dist < closest_dist:
                    closest_dist = dist
                    best_box = (int(x_center), int(y_center))

        if best_box:
            return best_box

    return None, None

def enviar_para_ahk(x, y):
    try:
        with open("target.txt", "w") as f:
            f.write(f"{x},{y}")
        subprocess.run(["swipe_executor.exe"])  # nome do seu executável AHK
    except Exception as e:
        print(f"Erro ao chamar o AHK: {e}")

def move_to_target(target_x, target_y, offset_x, offset_y):
    if target_x is not None and target_y is not None:
        abs_x = offset_x + target_x
        abs_y = offset_y + target_y
        print(f"[📡] Enviando coordenadas para swipe: ({abs_x}, {abs_y})")
        enviar_para_ahk(abs_x, abs_y)

def aim_bot():
    print("Carregando modelo YOLOv8s...")
    model = load_model()
    if model is None:
        return

    def process_frame():
        while True:
            frame, (offset_x, offset_y) = capture_center_screen()
            target_x, target_y = detect_person(model, frame)
            move_to_target(target_x, target_y, offset_x, offset_y)
            time.sleep(3000)

    print("Sistema de mira automática iniciado")
    if localizar_bluestacks():
        print("✅ BlueStacks detectado.")
    else:
        print("⚠️ BlueStacks não detectado.")

    Thread(target=process_frame).start()

if __name__ == "__main__":
    aim_bot()
