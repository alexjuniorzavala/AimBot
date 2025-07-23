import torch
import pyautogui
import cv2
import numpy as np
from pynput.mouse import Listener
import math
import win32gui
import time
import subprocess

# Configurações
CAPTURE_SIZE_X = 530
CAPTURE_SIZE_Y = 530
X_OFFSET = -50
Y_OFFSET = 0
pyautogui.MINIMUM_DURATION = 0  # Remove o delay mínimo do pyautogui
pyautogui.PAUSE = 0  # Remove a pausa entre comandos

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
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        model.to(device)
        model.eval()
        return model
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        return None

def get_screen_center():
    bluestacks = localizar_bluestacks()
    if bluestacks:
        x1, y1, x2, y2 = bluestacks
        center_x = (x2 + x1) // 2
        center_y = (y2 + y1) // 2
    else:
        screen_width, screen_height = pyautogui.size()
        center_x = screen_width // 2
        center_y = screen_height // 2
    return center_x, center_y

def capture_center_screen():
    center_x, center_y = get_screen_center()
    x1 = center_x - Y_OFFSET
    y1 = (center_y - 277) - Y_OFFSET

    try:
        screenshot = pyautogui.screenshot(region=(x1, y1, CAPTURE_SIZE_X, CAPTURE_SIZE_Y))
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        print(f"Capturando área: x={x1}, y={y1}, tamanho={CAPTURE_SIZE_X}x{CAPTURE_SIZE_Y}")
        return frame, (x1, y1)
    except Exception as e:
        print(f"Erro na captura: {e}")
        return None, (x1, y1)

def detect_person(model, frame):
    if frame is None:
        return None, None
        
    results = model(frame, size=CAPTURE_SIZE_X)
    detections = results.pandas().xyxy[0]
    
    if not detections.empty:
        person_detections = detections[
            (detections['name'] == 'person') & 
            (detections['confidence'] > 0.4)
        ]
        
        if not person_detections.empty:
            frame_height, frame_width = frame.shape[:2]
            center_y = frame_height / 2
            
            best_detection = None
            lowest_y = float('inf')
            
            for _, det in person_detections.iterrows():
                y_center = (det['ymin'] + det['ymax']) / 2
                if y_center < lowest_y:
                    lowest_y = y_center
                    x_center = (det['xmin'] + det['xmax']) / 2
                    best_detection = (int(x_center), int(y_center))
            
            if best_detection:
                return best_detection

    return None, None

def call_ahk_swipe(start_x, start_y, end_x, end_y, steps=10):
    """
    Chama o script AHK para executar o swipe.
    Supondo que o script swipe.ahk aceite os parâmetros via linha de comando:
    start_x, start_y, end_x, end_y, steps
    """
    try:
        script_path = r"C:\caminho\para\swipe.ahk"  # ajuste o caminho conforme necessário
        command = [
            "AutoHotkey.exe", script_path,
            str(start_x),
            str(start_y),
            str(end_x),
            str(end_y),
            str(steps)
        ]
        subprocess.run(command)
    except Exception as e:
        print(f"Erro ao chamar o script AHK: {e}")

def toggle_free_look_mode():
    pyautogui.press('f1')
    time.sleep(0.06)

def move_to_target(target_x, target_y, offset_x, offset_y):
    if target_x is not None and target_y is not None:
        try:
            toggle_free_look_mode()
            time.sleep(0.06)
            
            abs_x = offset_x + target_x
            abs_y = offset_y + target_y
            
            screen_width, screen_height = pyautogui.size()
            current_x = screen_width // 2 + 200
            current_y = screen_height // 2

            delta_x = abs_x - current_x
            delta_y = abs_y - current_y

            end_x = current_x + delta_x
            end_y = current_y + delta_y

            print(f"Realizando swipe AHK para alinhar mira: de ({current_x},{current_y}) até ({end_x},{end_y})")

            call_ahk_swipe(current_x, current_y, end_x, end_y, steps=10)
            
            toggle_free_look_mode()
        except Exception as e:
            print(f"Erro ao mover: {e}")

def aim_bot():
    print("Carregando modelo YOLO...")
    model = load_model()
    if model is None:
        return

    def on_click(x, y, button, pressed):
        if button.name == 'right' and pressed:
            frame, (offset_x, offset_y) = capture_center_screen()
            target_x, target_y = detect_person(model, frame)
            move_to_target(target_x, target_y, offset_x, offset_y)

    print("\nSistema de mira automática iniciado")
    print("Detectando janela do BlueStacks...")
    if localizar_bluestacks():
        print("BlueStacks encontrado!")
    else:
        print("BlueStacks não encontrado, usando tela inteira")
    
    print("Pressione o botão esquerdo para ativar a mira")
    print("Pressione Ctrl+C para sair")
    
    with Listener(on_click=on_click) as listener:
        listener.join()

if __name__ == "__main__":
    aim_bot()