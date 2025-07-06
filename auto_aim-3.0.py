import torch
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
    """Localiza a janela do BlueStacks"""
    janela = win32gui.FindWindow(None, "BlueStacks")
    if janela:
        rect = win32gui.GetWindowRect(janela)
        return rect
    return None

def load_model():
    try:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True, force_reload=True)
        model.to(device)
        model.eval()
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
        
    results = model(frame, size=320)
    detections = results.pandas().xyxy[0]
    
    if not detections.empty:
        person_detections = detections[
            (detections['name'] == 'person') & 
            (detections['confidence'] > 0.5)
        ]
        
        if not person_detections.empty:
            frame_height, frame_width = frame.shape[:2]
            center_y = frame_height / 2
            
            best_detection = None
            closest_distance = float('inf')
            
            for _, det in person_detections.iterrows():
                x_center = (det['xmin'] + det['xmax']) / 2
                y_center = (det['ymin'] + det['ymax']) / 2
                distance = abs(x_center - frame_width / 2) + abs(y_center - center_y)
                
                if distance < closest_distance:
                    closest_distance = distance
                    best_detection = (int(x_center), int(y_center))
            
            if best_detection:
                return best_detection

    return None, None

def simulate_swipe_adb(start_x, start_y, end_x, end_y, duration=100):
    """Simula um movimento de deslize na tela do BlueStacks usando ADB"""
    try:
        command = f"adb shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}"
        subprocess.run(command, shell=True)
    except Exception as e:
        print(f"Erro ao realizar o swipe com ADB: {e}")

def move_to_target(target_x, target_y, offset_x, offset_y):
    if target_x is not None and target_y is not None:
        try:
            abs_x = offset_x + target_x
            abs_y = offset_y + target_y
            
            screen_width, screen_height = pyautogui.size()
            current_x = screen_width // 2 + 200
            current_y = screen_height // 2
            
            delta_x = abs_x - current_x
            delta_y = abs_y - current_y
            
            print(f"Realizando swipe para alinhar mira: delta_x={delta_x}, delta_y={delta_y}")
            simulate_swipe_adb(current_x, current_y, current_x + delta_x, current_y + delta_y)
            
        except Exception as e:
            print(f"Erro ao mover: {e}")

def aim_bot():
    print("Carregando modelo YOLO...")
    model = load_model()
    if model is None:
        return

    def process_frame():
        while True:
            frame, (offset_x, offset_y) = capture_center_screen()
            target_x, target_y = detect_person(model, frame)
            move_to_target(target_x, target_y, offset_x, offset_y)
            time.sleep(0.1)

    print("\nSistema de mira automática iniciado")
    print("Detectando janela do BlueStacks...")
    if localizar_bluestacks():
        print("BlueStacks encontrado!")
    else:
        print("BlueStacks não encontrado, usando tela inteira")
    
    thread = Thread(target=process_frame)
    thread.start()

if __name__ == "__main__":
    aim_bot()