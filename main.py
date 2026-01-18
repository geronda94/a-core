import time
from identity import get_config, update_config
from core.adb_client import ADBClient
from core.device import DeviceHardware
from network.monitor import get_external_ip

def main():
    print("=== A-CORE: AUTONOMOUS START ===")
    config = get_config()
    adb = ADBClient()
    hw = DeviceHardware(adb)

    while True:
        try:
            # 1. Проверяем/чиним ADB
            if not adb.ensure_connection():
                print("[?] Ожидание включения отладки на телефоне...")
                time.sleep(10)
                continue

            # 2. Автозаполнение пустых полей в конфиге
            needs_update = False
            if not config.get("model") or config.get("model") == "Unknown":
                model = hw.get_model()
                if model:
                    config["model"] = model
                    update_config("model", model)
                    needs_update = True

            if not config.get("resolution") or config.get("resolution") == "unknown":
                res = hw.get_resolution()
                if res != "unknown":
                    config["resolution"] = res
                    update_config("resolution", res)
                    needs_update = True

            if needs_update:
                print(f"[V] Конфиг обновлен: {config['model']} | {config['resolution']}")

            # 3. Отправка Heartbeat на сервер
            print(f"[*] Статус: ID={config['device_id']} | IP={get_external_ip()} | ADB={adb.port}")
            
            # (Здесь будет твой requests.post)

        except Exception as e:
            print(f"[!] Критическая ошибка: {e}")
        
        time.sleep(20)

if __name__ == "__main__":
    main()