import pyautogui
import cv2
import numpy as np
import time
from ultralytics import YOLO
import win32gui

# Carrega o modelo YOLOv8n
model = YOLO('yolov8n.pt')

def localizar_bluestacks():
    """Localiza a janela do BlueStacks"""
    janela = win32gui.FindWindow(None, "BlueStacks")
    if janela:
        rect = win32gui.GetWindowRect(janela)
        return rect
    return None

def capture_bluestacks_screen():
    bluestacks = localizar_bluestacks()
    if bluestacks:
        x1, y1, x2, y2 = bluestacks
        width = x2 - x1
        height = y2 - y1
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return frame, (x1, y1)
    else:
        print("BlueStacks não encontrado.")
        return None, (0, 0)

def detect_and_swipe(model):
    frame, (offset_x, offset_y) = capture_bluestacks_screen()
    if frame is None:
        return

    results = model(frame)
    detections = results[0].boxes  # Acessa as caixas de detecção do primeiro resultado

    if detections is not None and len(detections) > 0:
        for det in detections:
            if det.cls == 0 and det.conf > 0.4:  # cls == 0 para 'person'
                x_center = (det.xmin + det.xmax) / 2
                y_center = (det.ymin + det.ymax) / 2
                print(f"Detecção encontrada: x={x_center}, y={y_center}")

                # Simula um deslize na tela
                simulate_swipe(offset_x + x_center, offset_y + y_center)

def simulate_swipe(x, y, duration=0.1, sensitivity=5.0):
    """Simula um movimento de deslize na tela do BlueStacks"""
    try:
        import win32api
        import win32con
        
        # Converte as coordenadas para o formato do win32api
        x = int(x)
        y = int(y)
        
        # Posiciona o mouse no ponto inicial
        win32api.SetCursorPos((x, y))
        
        # Pressiona o botão esquerdo do mouse
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        
        # Ajusta a sensibilidade
        steps = int(10 / sensitivity)  # Menos passos para maior sensibilidade
        sleep_time = duration / steps
        
        for i in range(steps + 1):
            t = i / steps
            curr_x = int(x + 100 * t)  # Exemplo de movimento horizontal
            curr_y = int(y)
            win32api.SetCursorPos((curr_x, curr_y))
            time.sleep(sleep_time)
        
        # Solta o botão do mouse
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        
    except Exception as e:
        print(f"Erro ao realizar o swipe: {e}")

if __name__ == "__main__":
    while True:
        detect_and_swipe(model)
        time.sleep(1)  # Intervalo entre as detecções
