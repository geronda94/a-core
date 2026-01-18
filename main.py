import time
import subprocess
from identity import get_config, update_config
from core.adb_client import ADBClient
from core.device import DeviceHardware
from network.monitor import get_external_ip, find_adb_port, is_port_open

def main():
    print("=== A-CORE: OPTIMIZED START ===")
    config = get_config()
    adb = ADBClient()
    hw = DeviceHardware(adb)
    
    current_port = None # Кэш порта

    while True:
        try:
            # 1. Проверяем старый порт, прежде чем сканировать всё
            if not is_port_open(current_port):
                print("[!] Связь потеряна или еще не установлена.")
                current_port = find_adb_port()
                
                if current_port:
                    adb.address = f"127.0.0.1:{current_port}"
                    subprocess.run(f"adb connect {adb.address}", shell=True, capture_output=True)
                    print(f"[V] Новый порт найден и подключен: {current_port}")
                else:
                    print("[?] Порт не найден. Сплю 10 сек...")
                    time.sleep(10)
                    continue
            
            # 2. Если мы здесь — порт активен. Выполняем полезную работу.
            # (Проверка данных в конфиге — теперь работает мгновенно)
            if config.get("model") == "M2101K7BNY" and config.get("resolution") != "unknown":
                # Если всё уже заполнено, просто шлем привет серверу
                print(f"[*] OK | IP: {get_external_ip()} | Port: {current_port}")
            else:
                # Если чего-то не хватает — обновляем
                update_config("model", hw.get_model())
                update_config("resolution", hw.get_resolution())
                config = get_config()

        except Exception as e:
            print(f"[!] Ошибка: {e}")
        
        # В проде здесь будет опрос сервера раз в 5-10 секунд
        time.sleep(10)

if __name__ == "__main__":
    main()