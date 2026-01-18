# network/monitor.py
import socket
import requests

def is_port_open(port):
    """Быстрая проверка доступности порта."""
    if not port: return False
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            return s.connect_ex(('127.0.0.1', int(port))) == 0
    except:
        return False

def find_adb_port(start_port=30000, end_port=49999):
    """Поиск активного порта ADB (тяжелая операция)."""
    print(f"[*] Сканирование портов {start_port}-{end_port}...")
    # Приоритетные порты для ускорения
    for port in [5555, 37239, 43087, 38037]:
        if is_port_open(port): return str(port)
        
    for port in range(start_port, end_port + 1):
        if is_port_open(port): return str(port)
    return None

def get_external_ip():
    """Получение текущего внешнего IP."""
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "0.0.0.0"