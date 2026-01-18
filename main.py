# main.py
import time
import subprocess
from identity import get_config, update_runtime_info, update_config
from core.adb_client import ADBClient
from core.device import DeviceHardware
from network.monitor import get_external_ip, find_adb_port, is_port_open

def is_adb_ready():
    """Проверяет, есть ли хоть одно устройство в статусе device."""
    res = subprocess.run("adb devices", shell=True, capture_output=True, text=True).stdout
    return "device" in res and "localhost" in res

def main():
    print("=== A-CORE: STABLE MODE ===")
    config = get_config()
    adb = ADBClient()
    hw = DeviceHardware(adb)
    
    current_port = config.get("last_port")

    while True:
        try:
            # 1. Если ADB уже подключен и работает - не трогаем его!
            if is_adb_ready() and is_port_open(current_port):
                pass 
            else:
                print(f"[!] Поиск связи...")
                # Пробуем старый порт
                if not is_port_open(current_port):
                    current_port = find_adb_port()
                
                if current_port:
                    # Подключаемся только если порта нет в adb devices
                    print(f"[*] Пробую подключиться к {current_port}")
                    subprocess.run(f"adb connect 127.0.0.1:{current_port}", shell=True, capture_output=True)
                    update_runtime_info(port=current_port)
                    time.sleep(2) # Даем время на авторизацию
                else:
                    print("[?] Порт не найден. Проверь настройки телефона.")
                    time.sleep(10)
                    continue

            # 2. Если связь есть, работаем
            if is_adb_ready():
                # Обновляем инфо о железе ТОЛЬКО если оно unknown
                if config.get("model") == "Unknown":
                    m = hw.get_model()
                    r = hw.get_resolution()
                    if m and r != "unknown":
                        update_config("model", m)
                        update_config("resolution", r)
                        config = get_config()

                ip = get_external_ip()
                print(f"[*] СТАТУС: {config['model']} | IP: {ip} | Port: {current_port}")
            else:
                print("[!] Устройство найдено, но статус 'offline' или 'unauthorized'")

        except Exception as e:
            print(f"[!] Ошибка: {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    main()