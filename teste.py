import pyautogui
import win32gui
import time
from pynput.mouse import Listener
import random

def localizar_bluestacks():
    """Localiza a janela do BlueStacks"""
    janela = win32gui.FindWindow(None, "BlueStacks")
    if janela:
        rect = win32gui.GetWindowRect(janela)
        return rect
    return None

def fazer_swipe():
    coords = localizar_bluestacks()
    if coords:
        x1, y1, x2, y2 = coords
        centro_x = (x2 + x1) // 2
        centro_y = (y2 + y1) // 2
        
        # Definir pontos de início e fim do swipe
        inicio_x = centro_x
        inicio_y = centro_y + 100  # Começa um pouco abaixo do centro
        
        # Adiciona uma pequena variação aleatória para parecer mais natural
        fim_x = centro_x + random.randint(-50, 50)
        fim_y = centro_y - 200  # Termina acima do centro
        
        # Executa o movimento de swipe
        pyautogui.moveTo(inicio_x, inicio_y)
        pyautogui.mouseDown()
        pyautogui.moveTo(fim_x, fim_y, duration=0.4)  # Duração do swipe
        pyautogui.mouseUp()
        
        print(f"Swipe executado de ({inicio_x}, {inicio_y}) para ({fim_x}, {fim_y})")
    else:
        print("BlueStacks não encontrado!")

def on_click(x, y, button, pressed):
    if button.name == 'right' and pressed:
        print("Botão direito pressionado - Executando swipe")
        fazer_swipe()
        time.sleep(0.1)  # Pausa curta para reduzir frequência de eventos


if __name__ == "__main__":
    # Configurações do pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.4
    
    print("Programa iniciado")
    print("Clique com o botão esquerdo do mouse para fazer swipe")
    print("Pressione Ctrl+C para sair")
    
    # Inicia o listener para detectar cliques do mouse
    with Listener(on_click=on_click) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\nPrograma interrompido pelo usuário")
        except Exception as e:
            print(f"Erro: {e}")
    
    print("Programa finalizado")