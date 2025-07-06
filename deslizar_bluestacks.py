import subprocess
import time

def simulate_swipe_adb(start_x, start_y, end_x, end_y, duration=300):
    """Simula um movimento de deslize na tela do BlueStacks usando ADB com sendevent"""
    try:
        # Comando ADB para iniciar o toque
        start_command = f"adb shell sendevent /dev/input/event1 3 57 0; " \
                        f"adb shell sendevent /dev/input/event1 3 53 {start_x}; " \
                        f"adb shell sendevent /dev/input/event1 3 54 {start_y}; " \
                        f"adb shell sendevent /dev/input/event1 0 0 0"
        
        # Comando ADB para mover o toque
        move_command = f"adb shell sendevent /dev/input/event1 3 53 {end_x}; " \
                       f"adb shell sendevent /dev/input/event1 3 54 {end_y}; " \
                       f"adb shell sendevent /dev/input/event1 0 0 0"
        
        # Comando ADB para finalizar o toque
        end_command = f"adb shell sendevent /dev/input/event1 3 57 -1; " \
                      f"adb shell sendevent /dev/input/event1 0 0 0"
        
        # Executa os comandos com um intervalo para simular a duração do swipe
        subprocess.run(start_command, shell=True)
        time.sleep(duration / 1000.0)  # Converte milissegundos para segundos
        subprocess.run(move_command, shell=True)
        subprocess.run(end_command, shell=True)
        
        print(f"Swipe realizado de ({start_x}, {start_y}) para ({end_x}, {end_y}) com duração de {duration}ms")
    except Exception as e:
        print(f"Erro ao realizar o swipe com ADB: {e}")
    time.sleep(2)

if __name__ == "__main__":
    # Exemplo de uso: deslize da parte superior esquerda para a parte inferior direita
    simulate_swipe_adb(100, 100, 400, 400)
