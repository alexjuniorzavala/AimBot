import win32gui
import win32api
import win32con
import time

def localizar_bluestacks():
    hwnd = win32gui.FindWindow(None, "BlueStacks")
    if hwnd == 0:
        print("❌ BlueStacks não encontrado.")
        return None
    return win32gui.GetWindowRect(hwnd)

def swipe_blustacks(rel_x1=0.5, rel_y1=0.5, rel_x2=0.55, rel_y2=0.5, duration=0.05):
    rect = localizar_bluestacks()
    if rect is None:
        return

    x1, y1, x2, y2 = rect
    w, h = x2 - x1, y2 - y1

    abs_start = (int(x1 + w * rel_x1), int(y1 + h * rel_y1))
    abs_end = (int(x1 + w * rel_x2), int(y1 + h * rel_y2))

    # Pressiona botão
    win32api.SetCursorPos(abs_start)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.01)

    # Move suavemente até destino
    steps = 10
    for i in range(1, steps + 1):
        ix = abs_start[0] + (abs_end[0] - abs_start[0]) * i // steps
        iy = abs_start[1] + (abs_end[1] - abs_start[1]) * i // steps
        win32api.SetCursorPos((ix, iy))
        time.sleep(duration / steps)

    # Solta botão
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

if __name__ == "__main__":
    swipe_blustacks(0.5, 0.5, 0.55, 0.5)  # pequeno deslize horizontal no meio da tela
