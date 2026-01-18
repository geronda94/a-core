import time
import subprocess
from identity import get_config, update_config
from core.adb_client import ADBClient
from core.device import DeviceHardware
from network.monitor import get_external_ip, find_adb_port

def main():
    print("=== A-CORE: AUTONOMOUS START ===")
    config = get_config()
    adb = ADBClient()
    hw = DeviceHardware(adb)

    while True:
        try:
            # 1. Поиск порта и подключение
            port = find_adb_port()
            if port:
                adb.port = port
                adb.address = f"127.0.0.1:{port}"
                # Пытаемся подключиться, если устройство offline
                subprocess.run(f"adb connect {adb.address}", shell=True, capture_output=True)
            else:
                print("[?] Порт не найден. Включи отладку!")
                time.sleep(10)
                continue

            # 2. Собираем данные ТОЛЬКО если они валидны
            model = hw.get_model()
            if model and model != "Android Device" and model != config.get("model"):
                update_config("model", model)
                config["model"] = model
                print(f"[V] Модель определена: {model}")

            res = hw.get_resolution()
            if res != "unknown" and res != config.get("resolution"):
                update_config("resolution", res)
                config["resolution"] = res
                print(f"[V] Разрешение определено: {res}")

            # 3. Отчет
            print(f"[*] Статус: ID={config['device_id']} | IP={get_external_ip()} | ADB={port}")

        except Exception as e:
            print(f"[!] Ошибка: {e}")
        
        time.sleep(20)

if __name__ == "__main__":
    main()