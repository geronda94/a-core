# network/monitor.py
import socket
import requests

def is_port_open(port):
    if not port or port == "None": return False
    try:
        # Проверяем порт один раз, очень аккуратно
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5) # Даем чуть больше времени на ответ
            return s.connect_ex(('127.0.0.1', int(port))) == 0
    except:
        return False

def find_adb_port(start_port=30000, end_port=49999):
    # Сначала проверяем стандартный 5555
    if is_port_open(5555): return "5555"
    
    print(f"[*] Глубокое сканирование...")
    for port in range(start_port, end_port + 1):
        # Сканируем только каждый 2-й порт или с чуть большим таймаутом, чтобы не вешать стек
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.01)
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return str(port)
    return None

def get_external_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text
    except:
        return "0.0.0.0"