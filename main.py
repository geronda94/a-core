# main.py
import time
import subprocess
from identity import get_config, update_config
from core.adb_client import ADBClient
from core.device import DeviceHardware
from core.vision import Vision
from network.monitor import get_external_ip, find_adb_port, is_port_open

def main():
    print("=== A-CORE: ACTIVE & SMART ===")
    config = get_config()
    adb = ADBClient()
    hw = DeviceHardware(adb)
    vision = Vision(adb)
    
    current_port = None

    while True:
        try:
            # 1. Поддержание связи (Оптимизировано)
            if not is_port_open(current_port):
                current_port = find_adb_port()
                if current_port:
                    adb.address = f"127.0.0.1:{current_port}"
                    subprocess.run(f"adb connect {adb.address}", shell=True, capture_output=True)
                    print(f"[V] Связь установлена: {current_port}")
                else:
                    print("[?] Ожидание порта...")
                    time.sleep(10)
                    continue

            # 2. Проверка 'паспорта' устройства
            if not config.get("model") or config.get("resolution") == "unknown":
                print("[*] Обновление характеристик...")
                update_config("model", hw.get_model())
                update_config("resolution", hw.get_resolution())
                config = get_config()

            # 3. Пример работы зрения: ищем что-то на экране
            # В будущем это будет приходить как команда от сервера
            target = "Sasha"
            coords = vision.find_by_text(target)
            if coords:
                print(f"[!] Вижу '{target}' в точке {coords}. Могу кликнуть.")
                # adb.run(f"input tap {coords[0]} {coords[1]}")

            print(f"[*] Статус ОК | IP: {get_external_ip()} | Port: {current_port}")

        except Exception as e:
            print(f"[!] Ошибка: {e}")
        
        time.sleep(15)

if __name__ == "__main__":
    main()