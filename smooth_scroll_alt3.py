from pynput import keyboard
from pynput.keyboard import Controller, Key
import time
import math
import threading
import Quartz
import os
import datetime
import mss
import cv2
import numpy as np
import platform
import subprocess
import shutil

keyboard_controller = Controller()

# Parâmetros do ease
total_steps = 10
duration = 0.5  # segundos para o scroll completo
ease_type = 'in_out'  # pode ser 'in', 'out', 'in_out'
total_steps_left = 5  # Número de steps para scroll à esquerda
total_steps_right = 5  # Número de steps para scroll à direita
pressed_keys = set()
scroll_lock = threading.Lock()

# Teclas para scroll lateral
LEFT_KEYS = [',', ';']
RIGHT_KEYS = ['.' ,"'"]
RIGHT_KEYCODES = [39]  # keycode para ' (aspas simples)

# Diretório para salvar o vídeo
#VIDEO_OUTPUT_DIR = "/Users/alexluna/Desktop/videos"  # <-- Altere para o diretório desejado
#VIDEO_OUTPUT_DIR = "/tmp"  # <-- Altere para o diretório desejado
VIDEO_OUTPUT_DIR = "/Users/alexluna/Library/CloudStorage/GoogleDrive-alex.luna.costa@gmail.com/My Drive/[02] Resources/[06] Images/Screenshot Funnel/Print_x/Snaps"  # <-- Altere para o diretório desejado

# Configurações de vídeo
VIDEO_DURATION = 3  # segundos de gravação (altere aqui)
VIDEO_FPS = 24      # frames por segundo (altere aqui)

def ease_in_out(t):
    # Ease in-out usando função seno
    return 0.5 * (1 - math.cos(math.pi * t))

def press_key_quartz(keycode):
    print(f"[LOG] Simulando tecla Quartz keycode={keycode}")
    event_down = Quartz.CGEventCreateKeyboardEvent(None, keycode, True)
    event_up = Quartz.CGEventCreateKeyboardEvent(None, keycode, False)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_down)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_up)

def press_alt_3():
    print("[LOG] Simulando Alt+3")
    # Alt = Option = keycode 58 (left), 61 (right); 3 = keycode 20
    # Press Alt down
    event_alt_down = Quartz.CGEventCreateKeyboardEvent(None, 58, True)
    Quartz.CGEventSetFlags(event_alt_down, Quartz.kCGEventFlagMaskAlternate)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_alt_down)
    # Press 3 down
    event_3_down = Quartz.CGEventCreateKeyboardEvent(None, 20, True)
    Quartz.CGEventSetFlags(event_3_down, Quartz.kCGEventFlagMaskAlternate)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_3_down)
    # Release 3
    event_3_up = Quartz.CGEventCreateKeyboardEvent(None, 20, False)
    Quartz.CGEventSetFlags(event_3_up, Quartz.kCGEventFlagMaskAlternate)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_3_up)
    # Release Alt
    event_alt_up = Quartz.CGEventCreateKeyboardEvent(None, 58, False)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_alt_up)

def press_cmd_s():
    print("[LOG] Simulando Command+S")
    # Command = keycode 55 (left), S = keycode 1
    event_cmd_down = Quartz.CGEventCreateKeyboardEvent(None, 55, True)
    Quartz.CGEventSetFlags(event_cmd_down, Quartz.kCGEventFlagMaskCommand)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_cmd_down)
    event_s_down = Quartz.CGEventCreateKeyboardEvent(None, 1, True)
    Quartz.CGEventSetFlags(event_s_down, Quartz.kCGEventFlagMaskCommand)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_s_down)
    event_s_up = Quartz.CGEventCreateKeyboardEvent(None, 1, False)
    Quartz.CGEventSetFlags(event_s_up, Quartz.kCGEventFlagMaskCommand)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_s_up)
    event_cmd_up = Quartz.CGEventCreateKeyboardEvent(None, 55, False)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_cmd_up)

def press_esc():
    print("[LOG] Simulando Esc")
    event_esc_down = Quartz.CGEventCreateKeyboardEvent(None, 53, True)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_esc_down)
    event_esc_up = Quartz.CGEventCreateKeyboardEvent(None, 53, False)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event_esc_up)

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

def smooth_scroll_custom(key, steps):
    # Mapear Key para keycode do Quartz
    if key == Key.down:
        keycode = 125
    elif key == Key.up:
        keycode = 126
    elif key == Key.left:
        keycode = 123
    elif key == Key.right:
        keycode = 124
    else:
        print(f"[LOG] Tecla não suportada para scroll: {key}")
        return
    print(f"[LOG] Iniciando scroll suave para key={key} (keycode={keycode}) com {steps} steps")
    with scroll_lock:
        for i in range(steps):
            t = i / (steps - 1) if steps > 1 else 1
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
                prev_t = (i - 1) / (steps - 1) if steps > 1 else 1
                if ease_type == 'in_out':
                    sleep_time = (ease_in_out(t) - ease_in_out(prev_t)) * duration
                elif ease_type == 'in':
                    sleep_time = (t * t - prev_t * prev_t) * duration
                elif ease_type == 'out':
                    sleep_time = ((1 - (1 - t) * (1 - t)) - (1 - (1 - prev_t) * (1 - prev_t))) * duration
                else:
                    sleep_time = (t - prev_t) * duration

            print(f"[LOG] Scroll step {i+1}/{steps}, sleep_time={sleep_time:.4f}s")
            time.sleep(sleep_time)
            press_key_quartz(keycode)
    print(f"[LOG] Scroll suave finalizado para key={key}")

def beep():
    # Sinal sonoro cross-platform
    if platform.system() == "Darwin":
        os.system('afplay /System/Library/Sounds/Glass.aiff')
    elif platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 200)
    else:
        os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || beep')

def record_screen_video(duration=VIDEO_DURATION, fps=VIDEO_FPS):
    beep()
    print(f"[LOG] Iniciando gravação de vídeo da tela... duração={duration}s, fps={fps}")
    now = datetime.datetime.now()
    base_filename = f"Vid_{now.strftime('%d_%m_%y-%H_%M')}"
    frames_dir = os.path.join("/tmp", base_filename + "_frames")
    os.makedirs(frames_dir, exist_ok=True)
    final_filename = base_filename + ".mp4"
    final_path = os.path.join(VIDEO_OUTPUT_DIR, final_filename)
    start_time = time.time()
    frame_count = 0
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while (time.time() - start_time) < duration:
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            frame_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
            cv2.imwrite(frame_path, frame)
            frame_count += 1
    elapsed = time.time() - start_time
    real_fps = frame_count / elapsed
    print(f"[DEBUG] Frames gravados: {frame_count} | Duração real: {elapsed:.2f}s | FPS real: {real_fps:.2f} | Pasta: {frames_dir}")
    if frame_count == 0:
        print(f"[ERRO] Nenhum frame foi salvo!")
        beep()
        return
    print(f"[LOG] Montando vídeo com ffmpeg...")
    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-framerate", f"{real_fps:.2f}",
            "-i", os.path.join(frames_dir, "frame_%04d.png"),
            "-r", str(fps),  # força o vídeo final a ter o FPS desejado
            "-vcodec", "libx264", "-pix_fmt", "yuv420p", final_path
        ], check=True)
        print(f"[LOG] Conversão concluída. Limpando frames temporários: {frames_dir}")
        shutil.rmtree(frames_dir)
    except Exception as e:
        print(f"[ERRO] Erro ao montar vídeo com ffmpeg: {e}")
        beep()
        return
    beep()
    print(f"[LOG] Gravação finalizada. Vídeo salvo em: {final_path}")

def on_press(key):
    print(f"[DEBUG] key: {key}, key.char: {getattr(key, 'char', None)}")
    pressed_keys.add(key)
    if key == keyboard.KeyCode.from_char('q'):
        print("Q detectado. Encerrando o programa.")
        return False  # Encerra o listener
    if key == keyboard.KeyCode.from_char('l'):
        if not scroll_lock.locked():
            print("[LOG] Detected L, iniciando scroll thread para baixo")
            threading.Thread(target=smooth_scroll, args=(Key.down,), daemon=True).start()
    elif key == keyboard.KeyCode.from_char('k'):
        if not scroll_lock.locked():
            print("[LOG] Detected K, iniciando scroll thread para cima")
            threading.Thread(target=smooth_scroll, args=(Key.up,), daemon=True).start()
    elif isinstance(key, keyboard.KeyCode) and key.char in LEFT_KEYS:
        if not scroll_lock.locked():
            print(f"[LOG] Detected {key.char} (scroll esquerda), iniciando scroll thread para esquerda")
            threading.Thread(target=smooth_scroll_custom, args=(Key.left, total_steps_left), daemon=True).start()
    elif (isinstance(key, keyboard.KeyCode) and key.char in RIGHT_KEYS) or (hasattr(key, 'vk') and key.vk in RIGHT_KEYCODES):
        if not scroll_lock.locked():
            print(f"[LOG] Detected {getattr(key, 'char', key)}, (scroll direita), iniciando scroll thread para direita")
            threading.Thread(target=smooth_scroll_custom, args=(Key.right, total_steps_right), daemon=True).start()
    elif key == keyboard.KeyCode.from_char('p'):
        print("[LOG] Detected P, simulando Alt+3")
        threading.Thread(target=press_alt_3, daemon=True).start()
    elif key == keyboard.KeyCode.from_char('o'):
        print("[LOG] Detected O, simulando Command+S")
        threading.Thread(target=press_cmd_s, daemon=True).start()
    elif key == keyboard.KeyCode.from_char('i'):
        print("[LOG] Detected I, simulando Esc")
        threading.Thread(target=press_esc, daemon=True).start()
    elif key == keyboard.KeyCode.from_char('g'):
        print("[LOG] Detected G, iniciando gravação de vídeo da tela")
        threading.Thread(target=record_screen_video, daemon=True).start()
    # Nunca retorna False aqui, para manter o listener ativo

def on_release(key):
    print(f"[LOG] on_release: {key}")
    if key in pressed_keys:
        pressed_keys.remove(key)

def main():
    print("Pressione K para cima, L para baixo, P para Alt+3, O para Command+S, I para Esc, Q para sair (Ctrl+C para sair)")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main() 