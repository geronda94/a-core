# main.py
import time
import subprocess
from identity import get_config, update_config, update_runtime_info
from core.adb_client import ADBClient
from core.device import DeviceHardware
from network.monitor import get_external_ip, find_adb_port

def is_adb_alive():
    """Проверяет, жива ли связь, не нагружая сеть."""
    try:
        # Просто смотрим список, не пытаясь подключиться
        res = subprocess.check_output("adb devices", shell=True, text=True)
        # Нам нужно, чтобы было слово 'device' и не было 'offline'
        return "device" in res and "offline" not in res and "unauthorized" not in res
    except:
        return False

def main():
    print("=== A-CORE: NMAP INTEGRATION ===")
    config = get_config()
    adb = ADBClient()
    hw = DeviceHardware(adb)

    # При старте сразу проверяем, может мы уже подключены через autoconnect.sh?
    if is_adb_alive():
        print("[V] ADB уже активен. Работаем.")
    
    while True:
        try:
            # 1. ПРОВЕРКА СВЯЗИ
            if is_adb_alive():
                # ВСЁ ХОРОШО. Не трогаем порты, не сканируем.
                # Просто обновляем IP раз в цикл и ждем задачи.
                
                # (Тут позже будет код получения задач с сервера)
                
                # Редкая проверка конфига (раз в минуту, не чаще)
                if config.get("model") == "Unknown":
                    m = hw.get_model()
                    if m: 
                        update_config("model", m)
                        config = get_config()
                        print(f"[+] Модель определена: {m}")

                # Лог для спокойствия (можно убрать)
                # print(f"[*] OK | {config['model']}")
                
            else:
                # СВЯЗИ НЕТ. Только сейчас запускаем поиск.
                print("[!] Связь потеряна. Ищу порт через Nmap...")
                
                port = find_adb_port() # Теперь это мгновенно и безопасно
                
                if port:
                    print(f"[*] Порт найден: {port}. Подключаюсь...")
                    # Очистка не нужна, если мы просто потеряли связь
                    subprocess.run(f"adb connect 127.0.0.1:{port}", shell=True, capture_output=True)
                    update_runtime_info(port=port)
                    # Даем 2 секунды на прогрузку
                    time.sleep(2)
                else:
                    print("[?] Порт не найден. Включена ли отладка?")
                    time.sleep(5)

        except Exception as e:
            print(f"[!] Ошибка цикла: {e}")
        
        # Пауза цикла. Мы не переподключаемся здесь!
        time.sleep(5)

if __name__ == "__main__":
    main()