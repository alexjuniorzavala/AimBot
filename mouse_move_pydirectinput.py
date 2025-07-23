import time
from pynput.mouse import Listener, Button
import pydirectinput as pyautogui

# Constantes
CENTRO_MIRA = (681, 382)      # Ponto fixo onde está a mira no centro da tela
ORIGEM_MOUSE = (937, 397)     # Ponto onde o mouse sempre começa o movimento

# Coordenadas do alvo (exemplo)
target_pos = (800, 500)

def mover_mira_ate_alvo(target_pos, velocidade=10):
    alvo_x, alvo_y = target_pos
    delta_x = alvo_x - CENTRO_MIRA[0]
    delta_y = alvo_y - CENTRO_MIRA[1]

    # Iniciar o movimento a partir da origem M
    pyautogui.moveTo(ORIGEM_MOUSE[0], ORIGEM_MOUSE[1])
    time.sleep(0.01)

    # Movimento relativo simulando arrasto
    pyautogui.mouseDown()
    pyautogui.moveRel(delta_x, delta_y, duration=2)
    pyautogui.mouseUp()

    print(f"🕹️ Moveu mira com delta ({delta_x}, {delta_y})")

def on_click(x, y, button, pressed):
    if button == Button.right and pressed:
        mover_mira_ate_alvo(target_pos)

if __name__ == "__main__":
    print("✅ Pressione o botão direito para detectar e enviar alvo")
    with Listener(on_click=on_click) as listener:
        listener.join()
