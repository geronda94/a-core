import time
import subprocess
from identity import get_config, update_config
from core.adb_client import ADBClient
from core.device import DeviceHardware
from network.monitor import get_external_ip
from tasks.executor import TaskExecutor

# --- ТЕСТОВЫЙ ПАКЕТ ЗАДАЧ (Как будто пришел от AI/Сервера) ---
MOCK_TASK = {
  "batch_id": "test_flow_01",
  "actions": [
    {
      "command": "click",
      "target": {
        "description": "Кнопка настроек (пример)",
        "strategies": [
           {"type": "text", "value": "Settings"},
           {"type": "text", "value": "Настройки"},
           {"type": "desc", "value": "Settings"}
        ]
      }
    },
    {
      "command": "wait",
      "seconds": 2
    }
  ]
}

def is_adb_ready():
    try:
        res = subprocess.check_output("adb devices | grep 'device$'", shell=True, text=True)
        return bool(res.strip())
    except:
        return False

def main():
    print("=== A-CORE: WORKER WITH EXECUTOR ===")
    config = get_config()
    adb = ADBClient()
    hw = DeviceHardware(adb)
    
    # Инициализируем исполнителя
    executor = TaskExecutor(adb)

    while True:
        try:
            if is_adb_ready():
                if config.get("model") == "Unknown":
                    m = hw.get_model()
                    if m: 
                        update_config("model", m)
                        config = get_config()
                        print(f"[V] Устройство: {m}")

                # --- ТЕСТ ИСПОЛНИТЕЛЯ ---
                # Чтобы не спамить кликами, выполним задачу 1 раз и поставим флаг
                if not config.get("test_done"):
                    print("[!] Запускаю тестовую задачу...")
                    result = executor.execute_batch(MOCK_TASK)
                    if result:
                        print("[V] Тест завершен успешно!")
                    else:
                        print("[X] Тест провален.")
                    
                    # Чтобы не выполнять вечно - ставим паузу
                    time.sleep(10)
                else:
                    print("[*] Жду команды от сервера...")

            else:
                print("[...] Ожидаю Guardian...")

        except Exception as e:
            print(f"[!] Ошибка: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()