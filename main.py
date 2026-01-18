import time
import subprocess
import re
from identity import get_config, update_config, update_runtime_info
from core.adb_client import ADBClient
from core.device import DeviceHardware
from network.monitor import get_external_ip, find_adb_port

def get_adb_status():
    """
    Возвращает статус текущего подключения:
    'ok' - всё работает (device)
    'offline' - зависло (offline/unauthorized)
    'none' - нет соединений
    """
    try:
        output = subprocess.check_output("adb devices", shell=True, text=True).strip()
        if "offline" in output or "unauthorized" in output:
            return "offline"
        if "device" in output and "localhost" in output:
            return "ok"
    except:
        pass
    return "none"

def clean_zombie_connections():
    """Находит и убивает все offline подключения."""
    try:
        output = subprocess.check_output("adb devices", shell=True, text=True)
        # Ищем строки вида '127.0.0.1:35689 offline'
        zombies = re.findall(r"(127\.0\.0\.1:\d+)\s+offline", output)
        for zombie in zombies:
            print(f"[☠️] Убиваю зомби-соединение: {zombie}")
            subprocess.run(f"adb disconnect {zombie}", shell=True)
            time.sleep(1)
    except:
        pass

def main():
    print("=== A-CORE: ANTI-ZOMBIE MODE ===")
    config = get_config()
    adb = ADBClient()
    hw = DeviceHardware(adb)

    while True:
        try:
            status = get_adb_status()

            # СЦЕНАРИЙ 1: Всё работает
            if status == "ok":
                # Редкая проверка модели (раз в цикл)
                if config.get("model") == "Unknown":
                    m = hw.get_model()
                    if m: 
                        update_config("model", m)
                        config = get_config()
                        print(f"[+] Модель определена: {m}")
                
                # ТУТ БУДЕТ EXECUTOR ЗАДАЧ
                # ...
                
            # СЦЕНАРИЙ 2: Зависло (Offline)
            elif status == "offline":
                print("[!] Обнаружен статус OFFLINE. Зачистка...")
                clean_zombie_connections()
                # После зачистки сразу идем на новый круг поиска
                continue

            # СЦЕНАРИЙ 3: Нет соединения (None)
            else:
                print("[!] Связи нет. Ищу порт через Nmap...")
                port = find_adb_port()
                
                if port:
                    print(f"[*] Порт найден: {port}. Подключаюсь...")
                    # На всякий случай делаем disconnect перед connect
                    subprocess.run(f"adb disconnect 127.0.0.1:{port}", shell=True, capture_output=True)
                    
                    res = subprocess.run(f"adb connect 127.0.0.1:{port}", shell=True, capture_output=True, text=True)
                    print(f"    > {res.stdout.strip()}")
                    
                    update_runtime_info(port=port)
                    time.sleep(3) # Даем время на авторизацию
                else:
                    print("[?] Порт не найден. Включи отладку!")
                    time.sleep(5)

        except KeyboardInterrupt:
            print("\n[x] Остановка.")
            break
        except Exception as e:
            print(f"[!] Ошибка: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()