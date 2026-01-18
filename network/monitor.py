import subprocess
import requests

def get_adb_port():
    """Определяет порт беспроводной отладки."""
    try:
        # Пытаемся получить порт через настройки системы
        port = subprocess.check_output("adb shell getprop service.adb.tcp.port", shell=True, text=True).strip()
        if port and port != "-1":
            return port
    except:
        pass
    return "5555" # Стандартный порт, если другой не найден

def get_external_ip():
    """Получает внешний IP через мобильную сеть/текущий шлюз."""
    try:
        # Используем таймаут, чтобы скрипт не вис без интернета
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "0.0.0.0"

def get_network_status():
    return {
        "ip": get_external_ip(),
        "adb_port": get_adb_port()
    }