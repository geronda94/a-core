# main.py
import time
from identity import get_config, update_config
from core.adb_client import ADBClient
from core.device import DeviceHardware
from core.vision import Vision
from network.monitor import get_adb_port, get_external_ip

def main():
    config = get_config()
    port = get_adb_port()
    client = ADBClient(port=port)
    
    # 1. Проверка коннекта
    if not client.is_connected():
        print(f"[!] Устройство {client.address} не найдено. Попытка переподключения...")
        import subprocess
        subprocess.run(f"adb connect {client.address}", shell=True)

    hw = DeviceHardware(client)
    vision = Vision(client)

    # 2. Актуализация конфига
    if config.get("model") == "" or config.get("resolution") == "unknown":
        print("[*] Собираем данные об устройстве...")
        update_config("model", hw.get_model())
        update_config("resolution", hw.get_resolution())
        config = get_config()

    print(f"=== A-CORE ACTIVE [ID: {config['device_id']}] ===")
    print(f"[*] {config['model']} | {config['resolution']}")

    while True:
        # Тестовый поиск текста на экране (например, слова "Settings" или "Sasha")
        target = "Sasha"
        found = vision.find_element(target)
        
        if found:
            print(f"[+] Нашел '{target}' в координатах {found}")
        
        # Отчет для сервера
        status = {
            "id": config['device_id'],
            "ip": get_external_ip(),
            "adb_port": port
        }
        print(f"[*] Heartbeat: IP={status['ip']}")
        
        time.sleep(15)

if __name__ == "__main__":
    main()