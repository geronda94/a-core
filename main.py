import time
import requests
from identity import get_device_id
from network.monitor import get_network_status
from core.adb_client import ADBClient

# Настройки сервера
SERVER_URL = "https://твой-сервер.com/api" 

def main():
    device_id = get_device_id()
    # Инициализируем клиента (на ПК это обычно 127.0.0.1:5555 или IP телефона)
    # Для теста на ПК укажи адрес, который видишь в `adb devices`
    net_info = get_network_status()
    client = ADBClient(port=net_info['adb_port'])

    print(f"=== A-CORE STARTED [ID: {device_id}] ===")

    while True:
        try:
            # 1. Собираем актуальные данные
            net = get_network_status()
            payload = {
                "device_id": device_id,
                "ip": net['ip'],
                "adb_port": net['adb_port'],
                "timestamp": time.time()
            }

            print(f"[*] Отправка статуса... IP: {payload['ip']}")
            
            # 2. Опрос сервера (закомментировано, пока нет сервера)
            # response = requests.post(f"{SERVER_URL}/poll", json=payload, timeout=10)
            # tasks = response.json().get("tasks", [])
            
            # Для теста: просто выведем данные в консоль
            print(f"Данные для сервера: {payload}")

        except Exception as e:
            print(f"[!] Ошибка: {e}")

        time.sleep(15) # Интервал опроса

if __name__ == "__main__":
    main()