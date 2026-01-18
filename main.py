# ~/a-core/main.py
import time
from identity import get_config, update_config
from core.adb_client import ADBClient
from core.device import DeviceHardware
from network.monitor import get_adb_port, get_external_ip

def main():
    config = get_config()
    # Инициализируем ADB (в Termux подключаемся к localhost)
    adb = ADBClient(host="127.0.0.1", port=get_adb_port())
    hw = DeviceHardware(adb)

    # Единоразово заполняем данные о железе, если их нет
    if config.get("model") == "Unknown":
        print("[*] Собираем данные об устройстве...")
        update_config("model", hw.get_model())
        update_config("resolution", hw.get_resolution())
        config = get_config()

    print(f"=== A-CORE ACTIVE ===")
    print(f"ID: {config['device_id']} | {config['model']} | {config['resolution']}")

    while True:
        try:
            status = {
                "id": config['device_id'],
                "ip": get_external_ip(),
                "adb_port": get_adb_port(),
                "mac": hw.get_mac(),
                "uptime": time.monotonic()
            }
            
            print(f"[*] Отчет: IP={status['ip']} | ADB={status['adb_port']}")
            
            # Здесь будет отправка на сервер:
            # requests.post(SERVER_URL, json=status)
            
        except Exception as e:
            print(f"[!] Ошибка цикла: {e}")
        
        time.sleep(30)

if __name__ == "__main__":
    main()