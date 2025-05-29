from pynput import keyboard
from pynput.keyboard import Controller, Key
import time
import math
import Quartz
import threading

keyboard_controller = Controller()

# Parâmetros do ease
total_steps = 10
duration = 0.5  # segundos para o scroll completo
ease_type = 'in_out'  # pode ser 'in', 'out', 'in_out'
pressed_keys = set()
scroll_lock = threading.Lock()

def ease_in_out(t):
    # Ease in-out usando função seno
    return 0.5 * (1 - math.cos(math.pi * t))

def press_key_quartz(keycode):
    print(f"[LOG] Simulando tecla Quartz keycode={keycode}")
    event_down = Quartz.CGEventCreateKeyboardEvent(None, keycode, True)
    event_up = Quartz.CGEventCreateKeyboardEvent(None, keycode, False)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_down)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_up)

def smooth_scroll(key):
    # Mapear Key para keycode do Quartz
    if key == Key.down:
        keycode = 125
    elif key == Key.up:
        keycode = 126
    else:
        print(f"[LOG] Tecla não suportada para scroll: {key}")
        return
    print(f"[LOG] Iniciando scroll suave para key={key} (keycode={keycode})")
    with scroll_lock:
        for i in range(total_steps):
            t = i / (total_steps - 1)
            if ease_type == 'in_out':
                delay = ease_in_out(t)
            elif ease_type == 'in':
                delay = t * t
            elif ease_type == 'out':
                delay = 1 - (1 - t) * (1 - t)
            else:
                delay = t

            # Normaliza o delay para o tempo total
            if i == 0:
                sleep_time = 0
            else:
                prev_t = (i - 1) / (total_steps - 1)
                if ease_type == 'in_out':
                    sleep_time = (ease_in_out(t) - ease_in_out(prev_t)) * duration
                elif ease_type == 'in':
                    sleep_time = (t * t - prev_t * prev_t) * duration
                elif ease_type == 'out':
                    sleep_time = ((1 - (1 - t) * (1 - t)) - (1 - (1 - prev_t) * (1 - prev_t))) * duration
                else:
                    sleep_time = (t - prev_t) * duration

            print(f"[LOG] Scroll step {i+1}/{total_steps}, sleep_time={sleep_time:.4f}s")
            time.sleep(sleep_time)
            press_key_quartz(keycode)
    print(f"[LOG] Scroll suave finalizado para key={key}")

def on_press(key):
    print(f"[LOG] on_press: {key}")
    pressed_keys.add(key)
    if (Key.shift in pressed_keys or Key.shift_r in pressed_keys) and (key == keyboard.KeyCode.from_char('k') or key == keyboard.KeyCode.from_char('l')):
        print("Shift + K/L detectado. Encerrando o programa.")
        return False  # Encerra o listener
    if key == keyboard.KeyCode.from_char('l'):
        if not scroll_lock.locked():
            print("[LOG] Detected L, iniciando scroll thread para baixo")
            threading.Thread(target=smooth_scroll, args=(Key.down,), daemon=True).start()
    elif key == keyboard.KeyCode.from_char('k'):
        if not scroll_lock.locked():
            print("[LOG] Detected K, iniciando scroll thread para cima")
            threading.Thread(target=smooth_scroll, args=(Key.up,), daemon=True).start()
    # Nunca retorna False aqui, para manter o listener ativo

def on_release(key):
    print(f"[LOG] on_release: {key}")
    if key in pressed_keys:
        pressed_keys.remove(key)

def main():
    print("Pressione K para cima ou L para baixo para testar o scroll suave (Shift+K/L para sair, Ctrl+C para sair)")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main() 