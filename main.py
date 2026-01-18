# main.py
import time
import subprocess
from identity import get_config, update_runtime_info, update_config
from core.adb_client import ADBClient
from core.device import DeviceHardware
from network.monitor import get_external_ip, find_adb_port, is_port_open
def is_adb_ready():
    res = subprocess.run("adb devices", shell=True, capture_output=True, text=True).stdout
    # Если видим offline, значит ключи не подошли
    if "offline" in res or "unauthorized" in res:
        return "unauthorized"
    return "ok" if ("device" in res and "localhost" in res) else "disconnected"

def main():
    print("=== A-CORE: RECOVERY MODE ===")
    # ... (инициализация adb, hw и т.д.)

    while True:
        try:
            state = is_adb_ready()
            
            if state == "ok":
                # Всё отлично, работаем
                pass 
            elif state == "unauthorized":
                print("[!] Ошибка авторизации! Перезапуск сервера...")
                subprocess.run("adb kill-server", shell=True)
                subprocess.run("adb start-server", shell=True)
                # Порт берем из конфига или ищем заново
                current_port = find_adb_port() 
                if current_port:
                    subprocess.run(f"adb connect 127.0.0.1:{current_port}", shell=True)
                print("[?] ПОСМОТРИ НА ЭКРАН ТЕЛЕФОНА И НАЖМИ 'РАЗРЕШИТЬ'")
                time.sleep(5)
                continue
            else:
                # Порт закрыт или не подключен
                current_port = find_adb_port()
                if current_port:
                    subprocess.run(f"adb connect 127.0.0.1:{current_port}", shell=True)
                time.sleep(2)
            
            # Если наконец-то OK, собираем данные
            if is_adb_ready() == "ok":
                # Твой обычный код сбора данных...
                ip = get_external_ip()
                print(f"[*] СТАТУС: {config['model']} | IP: {ip} | Port: {current_port}")
            
        except Exception as e:
            print(f"[!] Ошибка: {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    main()