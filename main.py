import time
from identity import get_config, update_config
from core.adb_client import ADBClient
from core.device import DeviceInfo
from network.monitor import get_network_status

def main():
    config = get_config()
    # На ПК адрес берем из adb devices, в Termux обычно localhost:5555
    client = ADBClient(port="5555") 
    device = DeviceInfo(client)

    # 1. Дозаполняем конфиг, если он пустой (единоразово)
    if config.get("resolution") == "Unknown":
        res = device.get_resolution()
        update_config("resolution", res)
        config["resolution"] = res

    if config.get("model") == "Unknown":
        model = device.get_model()
        update_config("model", model)
        config["model"] = model

    print(f"=== A-CORE STARTED ===")
    print(f"ID: {config['device_id']} | Model: {config['model']} | Res: {config['resolution']}")

    while True:
        # Собираем динамические данные (IP, MAC)
        net = get_network_status()
        mac = device.get_mac()

        payload = {
            **config, # Включаем ID, дату старта, разрешение
            "current_ip": net['ip'],
            "current_mac": mac,
            "adb_port": net['adb_port'],
            "timestamp": time.time()
        }

        print(f"[*] Отправка данных: IP {payload['current_ip']}, MAC {payload['current_mac']}")
        # Здесь будет requests.post...
        
        time.sleep(15)

if __name__ == "__main__":
    main()