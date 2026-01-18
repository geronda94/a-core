import socket
import requests

def find_adb_port(start_port=30000, end_port=49999):
    """Более надежный поиск порта."""
    # Сначала проверим, не прописан ли порт уже в системе
    print(f"[*] Сканирую порты для ADB...")
    for port in [37239, 43087, 38037, 5555]: # Проверяем твои прошлые порты в приоритете
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1) # Увеличили таймаут до 0.1
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return str(port)

    # Если в списке нет, сканируем весь диапазон
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.05) 
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return str(port)
    return None

def get_external_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "0.0.0.0"