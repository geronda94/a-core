import time
import subprocess
from identity import get_config, update_config, update_runtime_info
from core.adb_client import ADBClient
from core.device import DeviceHardware
from network.monitor import get_external_ip, find_adb_port

def is_adb_alive():
    """Проверяет реальный статус: device - OK, offline/пусто - Bad."""
    try:
        res = subprocess.check_output("adb devices", shell=True, text=True)
        # Нам нужен именно статус 'device'. 'offline' нам не подходит.
        return "device" in res and "offline" not in res and "unauthorized" not in res
    except:
        return False

def main():
    print("=== A-CORE: STABLE CONNECTION FIX ===")
    config = get_config()
    adb = ADBClient()
    hw = DeviceHardware(adb)

    while True:
        try:
            # 1. ЕСТЬ ЛИ ЖИВАЯ СВЯЗЬ?
            if is_adb_alive():
                # --- БЛОК АКТИВНОЙ РАБОТЫ ---
                # Если связь есть, просто обновляем IP и радуемся жизни
                if config.get("model") == "Unknown":
                    print("[*] Дочитываю данные об устройстве...")
                    m = hw.get_model()
                    if m: 
                        update_config("model", m)
                        config = get_config()

                # Здесь позже будет executor.execute(...)
                
                # print(f"[V] Связь в норме. Порт: {config.get('last_port')}") # Раскомментируй для отладки

            else:
                # --- БЛОК ВОССТАНОВЛЕНИЯ ---
                print("[!] Связи нет. Ищу порт через Nmap...")
                
                port = find_adb_port()
                
                if port:
                    print(f"[*] Порт найден: {port}. Сброс и подключение...")
                    
                    # ВАЖНО: Сначала отключаем этот порт, чтобы убить "зомби"
                    subprocess.run(f"adb disconnect 127.0.0.1:{port}", shell=True, capture_output=True)
                    time.sleep(1) 
                    
                    # Теперь подключаемся начисто
                    res = subprocess.run(f"adb connect 127.0.0.1:{port}", shell=True, capture_output=True, text=True)
                    print(f"    > {res.stdout.strip()}") # Выводим ответ ADB
                    
                    update_runtime_info(port=port)
                    
                    # Ждем чуть дольше, чтобы авторизация прошла
                    time.sleep(3)
                    
                    # Если после подключения всё еще плохо - выводим статус
                    if not is_adb_alive():
                        print(f"[?] Подключился, но статус не 'device'. Проверь 'adb devices'.")
                else:
                    print("[?] Порт не найден (Nmap пусто). Отладка включена?")
                    time.sleep(5)

        except Exception as e:
            print(f"[!] Ошибка: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()