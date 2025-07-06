def detect_person(model, frame):
    if frame is None:
        return None, None
        
    results = model(frame)
    detections = results[0].boxes  # Acessa as caixas de detecção do primeiro resultado
    
    if detections is not None and len(detections) > 0:
        # Filtra as detecções para encontrar pessoas
        person_detections = [det for det in detections if det.cls == 0 and det.conf > 0.4]  # cls == 0 para 'person'
        
        if person_detections:
            frame_height, frame_width = frame.shape[:2]
            center_y = frame_height / 2
            
            # Pega a detecção mais próxima do topo da tela
            best_detection = None
            lowest_y = float('inf')
            
            for det in person_detections:
                y_center = (det.ymin + det.ymax) / 2
                
                if y_center < lowest_y:
                    lowest_y = y_center
                    x_center = (det.xmin + det.xmax) / 2
                    best_detection = (int(x_center), int(y_center))
            
            if best_detection:
                print(f"Detecção encontrada: {best_detection}")
                return best_detection

    print("Nenhuma detecção encontrada.")
    return None, None

def move_to_target(target_x, target_y, offset_x, offset_y):
    if target_x is not None and target_y is not None:
        try:
            # Calcula as coordenadas absolutas do alvo
            abs_x = offset_x + target_x
            abs_y = offset_y + target_y
            
            # Obtém a posição atual do mouse (ajustado para começar mais à direita)
            screen_width, screen_height = pyautogui.size()
            current_x = screen_width // 2 + 200  # Ajuste para começar mais à direita
            current_y = screen_height // 2
            
            # Calcula a diferença entre a posição do alvo e o ponto ajustado
            delta_x = abs_x - current_x
            delta_y = abs_y - current_y
            
            # Verifica se o delta é significativo para realizar o swipe
            if abs(delta_x) > 5 or abs(delta_y) > 5:
                print(f"Realizando swipe para alinhar mira: delta_x={delta_x}, delta_y={delta_y}")
                simulate_swipe(current_x, current_y, current_x + delta_x, current_y + delta_y, duration=0.05, sensitivity=3.5)
            else:
                print("Delta muito pequeno, swipe não necessário.")
            
        except Exception as e:
            print(f"Erro ao mover: {e}")
    else:
        print("Coordenadas do alvo não são válidas.") 