# main.py
import time
import subprocess
from identity import get_config, update_config, update_runtime_info
from core.adb_client import ADBClient
from core.device import DeviceHardware
from network.monitor import get_external_ip, find_adb_port, is_port_open

def main():
    print("=== A-CORE: PERSISTENT SESSION ===")
    config = get_config()
    
    # Пытаемся начать с последнего порта, который был в JSON
    current_port = config.get("last_port", "5555")
    adb = ADBClient()
    hw = DeviceHardware(adb)

    while True:
        try:
            # 1. Проверяем: жив ли старый порт?
            if not is_port_open(current_port):
                print(f"[!] Порт {current_port} закрыт. Ищу новый...")
                new_port = find_adb_port()
                
                if new_port:
                    current_port = new_port
                    adb.address = f"127.0.0.1:{current_port}"
                    # Чистим старые зависшие коннекты и подключаемся к новому
                    subprocess.run(f"adb disconnect", shell=True, capture_output=True)
                    subprocess.run(f"adb connect {adb.address}", shell=True, capture_output=True)
                    # Сохраняем в JSON, чтобы не искать после перезагрузки
                    update_runtime_info(port=current_port)
                    print(f"[V] Переподключено к {current_port}")
                else:
                    print("[?] Свободных портов ADB не найдено. Жду...")
                    time.sleep(10)
                    continue

            # 2. Получаем IP и сохраняем его в JSON
            current_ip = get_external_ip()
            update_runtime_info(ip=current_ip)

            # 3. Дозаполняем железные данные (модель/разрешение) если нужно
            if config.get("model") == "Unknown" or config.get("resolution") == "unknown":
                model = hw.get_model()
                res = hw.get_resolution()
                if model and res != "unknown":
                    update_config("model", model)
                    update_config("resolution", res)
                    config = get_config() # Перечитываем конфиг

            print(f"[*] СТАТУС: {config['model']} | IP: {current_ip} | Port: {current_port}")

        except Exception as e:
            print(f"[!] Ошибка: {e}")
        
        time.sleep(10)

if __name__ == "__main__":
    main()