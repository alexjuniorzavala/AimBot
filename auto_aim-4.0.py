import cv2
import ctypes
import time
from ultralytics import YOLO
import mss  # Adicionado
import numpy as np  # Adicionado
from pynput.mouse import Listener, Button

# ===== CONFIGURAÇÕES DE MIRA E JANELA =====
CENTRO_MIRA = (681, 382)
SENSIBILIDADE = 1 # Ajustável
DELAY_ENTRE_CLICKS = 0.5
imgsz=160

# ===== ZONA MORTA (ignora alvos já muito próximos da mira) =====
ZONA_MORTA = [(487, 336), (695, 336), (695, 617), (410, 617)]

def dentro_zona_morta(x, y):
    x1, y1 = ZONA_MORTA[0]
    x2, y2 = ZONA_MORTA[2]
    if x1 <= x <= x2 and y1 <= y <= y2:
        print("Ignorando zona morta")
    return x1 <= x <= x2 and y1 <= y <= y2

# ===== CAPTURA DE TELA (REGIÃO CENTRAL DO JOGO) USANDO MSS =====
monitor = {"top": 239, "left": 430, "width": 480, "height": 420}
sct = mss.mss()

def get_screenshot():
    try:
        print("Fazendo o print")
        print("Rodando linha 32 : sct_img = sct.grab(monitor)")
        with mss.mss() as sct:  # Crie o objeto dentro da função
            sct_img = sct.grab(monitor)
        print("Rodando linha 34 : img = np.array(sct_img)")
        img = np.array(sct_img)
        print("Rodando linha 36 : img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)")
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img
    except Exception as e:
        print(f"Erro ao capturar tela: {e}")
        return None

# ===== YOLO DETECTOR =====
model = YOLO("Free_Fire_Weight/self_head_body.pt")

# ===== STRUCTS DO WINDOWS PARA MOVIMENTO REAL =====
PUL = ctypes.POINTER(ctypes.c_ulong)

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class Input_I(ctypes.Union):
    _fields_ = [("mi", MouseInput)]

class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I)
    ]

def mover_mouse_relativo(dx, dy):
    extra = ctypes.c_ulong(0)
    mi = MouseInput(dx, dy, 0, 0x0001, 0, ctypes.pointer(extra))  # MOUSEEVENTF_MOVE
    input_struct = Input(ctypes.c_ulong(0), Input_I(mi))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(input_struct), ctypes.sizeof(input_struct))

# ===== LÓGICA DE DETECÇÃO E MOVIMENTO =====
def detectar_e_mirar():
    print("Chamando o print")
    img = get_screenshot()
    results = model(img, imgsz=256)

    for result in results:
        boxes = result.boxes.xywh
        classes = result.boxes.cls
        names = result.names

        if boxes is not None and len(boxes) > 0:
            for box, cls in zip(boxes, classes):
                x_center, y_center, _, _ = box
                nome_classe = names[int(cls)]

                abs_x = int(x_center + monitor["left"])
                abs_y = int(y_center + monitor["top"])

                if nome_classe.lower() != 'you' and not dentro_zona_morta(abs_x, abs_y):
                    dx = int((abs_x - CENTRO_MIRA[0]) * SENSIBILIDADE)
                    dy = int((abs_y - CENTRO_MIRA[1]) * SENSIBILIDADE)
                    print(f"🎯 Alvo detectado: ({abs_x}, {abs_y}) | Δx={dx}, Δy={dy}")
                    mover_mouse_relativo(dx, dy)
                    return

# ===== LISTENER PARA CLIQUE DIREITO =====
def on_click(x, y, button, pressed):
    if button == Button.right and pressed:
        print("Detetando")
        detectar_e_mirar()

# ===== EXECUÇÃO =====
if __name__ == "__main__":
    print("✅ Sistema de auto-mira ativado. Clique com o botão direito para mirar.")
    with Listener(on_click=on_click) as listener:
        listener.join()
